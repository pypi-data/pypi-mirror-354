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

from azure.core.exceptions import ClientAuthenticationError

from clusterondemand.exceptions import UserReportableException
from clusterondemand.paramvalidation import ParamValidator
from clusterondemandazure.azure_actions.credentials import AzureApiHelper
from clusterondemandazure.paramvalidation import AZUREParamValidator
from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")


class ClusterCommand:
    """Base class for all Azure cluster commands.

    This class only contains non-public validator methods that are intended to be used by
    descendant classes to validate user input. The general contract for all these methods is
    to perform various input sanitization checks, raising an Exception in the case of a failed
    check. If the check passes the _validate_xxx methods will simply return control to the
    caller with no return value.
    """

    def __init__(self):
        self.azure_api = AzureApiHelper.from_config(config)

    @property
    def vm_skus(self):
        return self._get_vm_skus(config["azure_location"])

    def _get_vm_skus(self, location):
        location_filter = f"location eq '{location}'" if location else None
        resource_skus = self.azure_api.compute_client.resource_skus.list(filter=location_filter)
        vm_skus = [sku for sku in resource_skus if sku.resource_type == "virtualMachines"]

        return vm_skus

    def _validate_cluster_name(self):
        validate_max_name_len = config["validate_max_cluster_name_length"]
        ParamValidator.validate_cluster_name(config["name"], validate_max_name_len)

    def _validate_cluster_password(self):
        if (isinstance(config["cluster_password"], str) and
                not AZUREParamValidator.validate_password(config["cluster_password"])):
            raise UserReportableException(
                "Cluster Password '%s' does not match proper format, the password should "
                "be at least 8 characters long." % config["cluster_password"]
            )

    def _validate_access_credentials(self):
        ParamValidator.validate_uuid_format(config["azure_tenant_id"], "Tenant ID does not match the proper format")
        ParamValidator.validate_uuid_format(config["azure_client_id"], "Client ID does not match the proper format")

        try:
            self.azure_api.get_credential()
            # We only validate the credentials once we call the API.
            # This means that we need to make an actual API call in which we use the results.
            list(self.azure_api.subscription_client.subscriptions.list())
        except ClientAuthenticationError:
            raise UserReportableException(
                "Azure API Authentication failed: provided credentials are invalid."
            )

    def _validate_location(self):
        if not AZUREParamValidator.validate_location(
                self.azure_api,
                config["azure_location"]
        ):
            raise UserReportableException(
                "Region %s does not exist." % config["azure_location"]
            )

    def _validate_vmsizes_in_region(self, head_node_type, node_type):
        vm_sizes = [sku.name.lower() for sku in self.vm_skus]

        if head_node_type.lower() not in vm_sizes:
            raise UserReportableException(
                "VMSize %s does not exist in location %s." %
                (head_node_type, config["azure_location"]))

        if node_type.lower() not in vm_sizes:
            raise UserReportableException(
                "VMSize %s does not exist in location %s." %
                (node_type, config["azure_location"])
            )

    def _validate_vmsizes_in_az(self, head_node_type, node_type):
        vm_sizes = []
        for sku in self.vm_skus:
            if len(sku.location_info) != 1:
                log.debug(f"Received unexpected location info for SKU {sku.name}, ignoring")

            if config["azure_availability_zone"] in sku.location_info[0].zones:
                vm_sizes.append(sku.name.lower())

        if head_node_type.lower() not in vm_sizes:
            raise UserReportableException(
                "VMSize %s does not exist in availability zone %s." %
                (head_node_type, config["azure_availability_zone"]))

        if node_type.lower() not in vm_sizes:
            raise UserReportableException(
                "VMSize %s does not exist in availability zone %s." %
                (head_node_type, config["azure_availability_zone"]))

    @staticmethod
    def _validate_vm_gen(head_node_vm_gen, node_vm_gen):

        def is_valid_hyperv_gen(g):
            return g.upper() in ("V1", "V2")

        if not is_valid_hyperv_gen(head_node_vm_gen):
            raise UserReportableException(
                "Invalid head node Hyper-V generation: %r. Supported values: 'V1', 'V2'." % head_node_vm_gen)
        if not is_valid_hyperv_gen(node_vm_gen):
            raise UserReportableException(
                "Invalid node Hyper-V generation: %r. Supported values: 'V1', 'V2'." % node_vm_gen)

    def _validate_blob(self):
        if (config["head_node_image"] and config["head_node_image"].startswith("http") and
                not AZUREParamValidator.validate_custom_blob(config["head_node_image"])):
            raise UserReportableException("VHD Blob specified does not exist or is unreachable.")

    @staticmethod
    def _validate_az_number():
        if az := config["azure_availability_zone"]:
            # There is no Azure region with more than 3 AZ-s
            if az not in ["1", "2", "3"]:
                raise UserReportableException(f"'{az}' is not a valid Azure availability zone")
