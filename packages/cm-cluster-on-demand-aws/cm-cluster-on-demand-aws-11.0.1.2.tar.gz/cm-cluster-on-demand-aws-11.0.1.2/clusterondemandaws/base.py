# Copyright (c) 2004-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import logging
import socket

from clusterondemand.clustercreate import check_client_ssh_access
from clusterondemand.exceptions import CODException, UserReportableException, ValidationException
from clusterondemand.inbound_traffic_rule import ALL_PROTOCOL_NUMBER, InboundNetworkACLRule
from clusterondemand.paramvalidation import ParamValidator
from clusterondemandaws.instancetype import get_available_instance_types
from clusterondemandaws.paramvalidation import AWSParamValidator
from clusterondemandconfig import config

from .clientutils import list_volume_types

log = logging.getLogger("cluster-on-demand")


class ClusterCommandBase:
    """Base class for all AWS cluster commands.

    This class only contains non-public validator methods that are intended to be used by
    descendant classes to validate user input. The general contract for all these methods is
    to perform various input sanitization checks, raising an Exception in the case of a failed
    check. If the check passes the _validate_xxx methods will simply return control to the
    caller with no return value.
    """
    def _validate_cluster_names_len_and_regex(self, names):
        validate_max_name_len = config["validate_max_cluster_name_length"]
        for name in names:
            ParamValidator.validate_cluster_name(name, validate_max_name_len)

    def _validate_aws_access_credentials(self):
        if not AWSParamValidator.validate_region(config["aws_region"]):
            raise ValidationException(
                "Region {region} does not exist.".format(
                    region=config["aws_region"]))

        if ("ssh_key_pair" in config and config["ssh_key_pair"] and not
            AWSParamValidator.validate_ssh_key_pair(
                config["ssh_key_pair"],
                config["aws_region"],
                config["aws_access_key_id"],
                config["aws_secret_key"])):
            raise ValidationException(
                "SSH Key pair '{keypair}' does not exist in region '{region}'".format(
                    keypair=config["ssh_key_pair"],
                    region=config["aws_region"]))

        if ("aws_availability_zone" in config and config["aws_availability_zone"] and not
                AWSParamValidator.validate_availability_zone(
                    config["aws_availability_zone"],
                    config["aws_region"],
                    config["aws_access_key_id"],
                    config["aws_secret_key"])):
            raise ValidationException(
                "Availability zone '{zone}' does not exist in region '{region}'".format(
                    zone=config["aws_availability_zone"],
                    region=config["aws_region"]))

    def _validate_instance_types(self):
        if not AWSParamValidator.validate_instance_type(
                config["aws_region"],
                config["head_node_type"]):
            raise UserReportableException(
                "Instance type '{itype}' does not exist in region '{region}'".format(
                    itype=config["head_node_type"],
                    region=config["aws_region"]))

        if not AWSParamValidator.validate_instance_type(
                config["aws_region"],
                config["node_type"]):
            raise UserReportableException(
                "Instance type '{itype}' does not exist in region '{region}'" .format(
                    itype=config["node_type"],
                    region=config["aws_region"]))

    def _validate_instance_types_arch(self) -> None:
        def get_supported_archs(instance_type: str) -> set[str]:
            instance_types = get_available_instance_types(config["aws_region"])
            archs = instance_types[instance_type].get("ProcessorInfo", {}).get("SupportedArchitectures", [])
            supported_archs = set()
            if "x86_64" in archs:
                supported_archs.add("x86_64")
            if "arm64" in archs:
                supported_archs.add("aarch64")
            if not supported_archs:
                raise UserReportableException(
                    f"Instance type {instance_type!r} CPU architectures are not supported: " +
                    f"{', '.join(archs)}. Expected: x86_64, arm64"
                )
            return supported_archs

        head_type = config["head_node_type"]
        node_type = config["node_type"]
        head_type_supported_archs = get_supported_archs(head_type)
        node_type_supported_archs = get_supported_archs(node_type)

        # Select image arch based on head node instance type.
        if config["arch"] not in head_type_supported_archs:
            if config.is_item_set_from_defaults("arch"):
                supported_arch = next(iter(head_type_supported_archs))
                log.debug(
                    f"Head node instance type {head_type!r} doesn't support default arch {config['arch']!r}. "
                    f"Selecting one of supported archs: {supported_arch!r}."
                )
                config["arch"] = supported_arch
            else:
                raise UserReportableException(
                    f"Head node instance type {head_type!r} doesn't support selected architecture {config['arch']!r}. "
                    f"Supported architectures: {', '.join(head_type_supported_archs)}"
                )

        # Make sure that image arch selected above is compatible with node instance type.
        if config["arch"] not in node_type_supported_archs:
            if config.is_item_set_from_defaults("node_type"):
                log.debug(
                    "Default compute node instance type has different CPU arch than head node. "
                    f"Falling back to head node's instance type {head_type!r}"
                )
                config["node_type"] = head_type
            else:
                raise UserReportableException(
                    f"Compute node instance type {node_type!r} and head node instance type {head_type!r} "
                    "have different CPU architectures. Mixed architectures are currently not supported, please choose "
                    "different node type using --node-type parameter."
                )

    @staticmethod
    def _validate_volume_types():
        volume_types = list_volume_types(
            region=config["aws_region"],
            aws_key_id=config["aws_access_key_id"],
            aws_secret=config["aws_secret_key"],
        )

        if config["head_node_root_volume_type"] not in volume_types:
            raise ValidationException(f"Requested root volume type {config['head_node_root_volume_type']!r} does not "
                                      f"exist in the region {config['aws_region']}. Please choose a valid volume type "
                                      f"from the following options: {', '.join(volume_types)}")

    @staticmethod
    def _validate_inbound_network_acl_rule(
        inbound_acl_rules: list[InboundNetworkACLRule] | None, configure_acl_rules: bool
    ) -> None:
        message = (
            "Cluster is created in a dedicated VPC and requires network ACL rules to be accessed, but "
            "insufficient ACL rules were requested. Cluster cannot be managed from the internet after creation. "
            "Please configure ACL rules to allow TCP port 22 or 8081 from at least one public CIDR block. "
            "Refer to '--inbound-network-acl-rule' help for examples and more information"
        )
        if configure_acl_rules:
            if inbound_acl_rules:
                if not check_client_ssh_access(inbound_acl_rules):
                    log.warning(
                        "SSH access is not allowed from the client IP address due to missing inbound network ACL "
                        "rules. Cluster creation will proceed, but waiting for SSH access is disabled "
                        "(wait_ssh set to 0)."
                    )
                    config["wait_ssh"] = 0
                else:
                    return

                access_ports = [22, 8081]
                for rule in inbound_acl_rules:
                    if rule.protocol_number == ALL_PROTOCOL_NUMBER:
                        return

                    # At least ssh or Base view ports should be open.
                    if (
                        rule.protocol_number == socket.IPPROTO_TCP and (
                            int(rule.dst_first_port) <= access_ports[0] <= int(rule.dst_last_port)
                            or int(rule.dst_first_port) <= access_ports[1] <= int(rule.dst_last_port)
                        )
                    ):
                        return

            raise CODException(message)
