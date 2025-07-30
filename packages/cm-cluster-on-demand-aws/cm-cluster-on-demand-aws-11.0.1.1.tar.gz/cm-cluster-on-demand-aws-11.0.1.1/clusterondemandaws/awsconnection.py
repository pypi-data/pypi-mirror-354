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
import typing
from functools import cache

import boto3

from clusterondemandconfig import config

if typing.TYPE_CHECKING:
    from mypy_boto3_ec2.client import EC2Client
    from mypy_boto3_ec2.service_resource import EC2ServiceResource

log = logging.getLogger("cluster-on-demand")


@cache
def _establish_connection_to_aws() -> boto3.session.Session:
    log.debug("Establish session with AWS region '%s'" % config["aws_region"])
    if config["aws_profile"]:
        log.debug(
            "Using AWS profile name '%s', ignoring other credentials" % config["aws_profile"]
        )
        return boto3.session.Session(
            profile_name=config["aws_profile"],
            region_name=config["aws_region"],
        )

    return boto3.session.Session(
        config["aws_access_key_id"],
        config["aws_secret_key"],
        config["aws_session_token"],
        region_name=config["aws_region"],
    )


@cache
def create_aws_service_resource(
        service_name: str,
        api_version: str = "2016-11-15",
        **kwargs: typing.Any
) -> EC2ServiceResource:
    # TODO: api_version is set to 2016-11-15, for backwards compatibility.
    # Need to investigate if we need to hardcode it, or if we can use the latest one.
    session = _establish_connection_to_aws()

    return session.resource(**kwargs, service_name=service_name, api_version=api_version)  # type: ignore[call-overload]


@cache
def create_aws_service_client(
        service_name: str,
        **kwargs: typing.Any
) -> EC2Client:
    session = _establish_connection_to_aws()

    return session.client(**kwargs, service_name=service_name)  # type: ignore[call-overload]
