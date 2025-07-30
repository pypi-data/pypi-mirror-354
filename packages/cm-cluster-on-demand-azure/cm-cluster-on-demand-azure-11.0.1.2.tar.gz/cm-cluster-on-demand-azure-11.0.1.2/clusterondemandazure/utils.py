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

log = logging.getLogger("cluster-on-demand")

COD_RESOURCE_GROUP_SUFFIX = "_cod_resource_group"


def name_from_r_group(r_group_name):
    """
    Obtain name of resource group.

    :param r_group_name: resource group name
    :return: extracted cluster name from group name
    """
    return r_group_name.removesuffix(COD_RESOURCE_GROUP_SUFFIX)


def get_detailed_vm(azure_api_client, resource_group_name, vm):
    """
    Unless explicitely requested, Azure API returns a VM object without "instanceView" data.
    Since we don't always need this data, we don't get it by default,
    but provide a helper function to fetch it here.
    """
    return azure_api_client.compute_client.virtual_machines.get(
        resource_group_name=resource_group_name,
        vm_name=vm.name,
        expand="instanceView",
    )


def get_vm_power_state(azure_api_client, resource_group_name, vm):
    if not vm.instance_view:
        vm = get_detailed_vm(azure_api_client, resource_group_name, vm)

    power_state = next(
        (
            status
            for status in vm.instance_view.statuses
            if status.code.startswith("PowerState")
        ),
        None,
    )
    if not power_state:
        # API may not fetch the power state of a VM that just changed the state VM, retrying virtual_machines.get()
        # is excessive for this use-case. Let's just warn the user instead
        log.warning(
            f"Unable to determine power state of VM {vm.name}."
            f"if trying to start/stop the cluster, try using --force flag."
        )
        return None

    return power_state.code.split("/")[1].lower()


def filter_vms_by_state(azure_api_client, vms, resource_group_name, power_states):
    # We determine the power state based on VM -> instance_view -> statuses. There are 2 elements,
    # [PowerState, ProvisioningState]. Those states are found using list(), then get() methods.
    # Another method list_all() does not find all the information,
    # list_all(status_only=True) doesn't find tags, status_only=False doesn't find power state.
    detailed_vms = [  # next(detailed_vms).as_dict() has all VM properties
        get_detailed_vm(azure_api_client, resource_group_name, vm) for vm in vms
    ]

    filtered_vms = []
    for vm in detailed_vms:
        power_state_name = get_vm_power_state(azure_api_client, resource_group_name, vm)

        if power_state_name in power_states:
            filtered_vms.append(vm)
        else:
            log.debug(f"VM {vm.name} is in state '{power_state_name}', ignoring")

    if not filtered_vms:
        log.debug(
            f"Didn't find any VMs in resource group {resource_group_name} "
            f"in requested power states: {', '.join(power_states)}"
        )
        return []

    return filtered_vms
