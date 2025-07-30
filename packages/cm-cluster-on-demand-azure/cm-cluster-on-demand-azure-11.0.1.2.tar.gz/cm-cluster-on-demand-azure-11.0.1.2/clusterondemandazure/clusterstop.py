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

from clusterondemand.bcm_version import BcmVersion
from clusterondemand.clusternameprefix import clusterprefix_ns
from clusterondemand.utils import confirm, confirm_ns, log_no_clusters_found, multithread_run
from clusterondemandazure.azure_actions.credentials import AzureApiHelper
from clusterondemandazure.cluster import Cluster
from clusterondemandazure.utils import filter_vms_by_state
from clusterondemandconfig import ConfigNamespace, config
from clusterondemandconfig.configuration_validation import cannot_use_together

from .configuration import azurecommon_ns

config_ns = ConfigNamespace("azure.cluster.stop")
config_ns.import_namespace(azurecommon_ns)
config_ns.import_namespace(clusterprefix_ns)
config_ns.import_namespace(confirm_ns)

config_ns.add_repeating_positional_parameter(
    "filters",
    help="Cluster names or patterns. Wildcards are supported (e.g: \\*)",
)
config_ns.add_parameter(
    "resource_group",
    help="Name of resource group where cluster VMs will be stopped. Only the VMs created by COD will be stopped",
)
config_ns.add_switch_parameter("dry_run", help="Do not actually stop the resources")
config_ns.add_switch_parameter(
    "force",
    help="Stop cluster VMs disregarding their power state. Useful if VM power state cannot be determined, "
    "or unexpected state found",
)

config_ns.add_validation(cannot_use_together("filters", "resource_group"))

log = logging.getLogger("cluster-on-demand")

# https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing
STATES_TO_STOP = [
    "creating",
    "starting",
    "stopping",
    "stopped",
    "running",
]


def run_command():
    azure_api_client = AzureApiHelper.from_config(config)

    clusters = list(Cluster.find_clusters(azure_api_client, config["filters"]))

    if not clusters:
        log_no_clusters_found("stop")
        return

    if not confirm(
        f"This will stop (deallocate) all cluster VMs in resource groups: "
        f"{', '.join(cluster.name for cluster in clusters)}. Continue?"
    ):
        return

    clusters_to_stop = []
    vms_to_stop = []
    if config["force"]:
        vms_to_stop = [vm for cluster in clusters for vm in cluster.head_nodes + cluster.compute_nodes]
    else:
        for cluster in clusters:
            vms = filter_vms_by_state(
                azure_api_client=azure_api_client,
                vms=cluster.head_nodes + cluster.compute_nodes,
                resource_group_name=cluster.resource_group.name,
                power_states=STATES_TO_STOP,
            )
            if not vms:
                log.info(
                    f"No running VMs were found for cluster: {cluster.name}"
                )
                continue
            vms_to_stop += vms
            clusters_to_stop.append(cluster)

    # Warn users trying to stop pre-v11 clusters, deployed in pre-existing RGs. Cnodes of such clusters
    # are not tagged with "BCM Cluster" tag
    pre_v11_clusters = [cluster for cluster in clusters_to_stop if BcmVersion(cluster.version).release < (11, 0)]
    for cluster in pre_v11_clusters:
        if any(vm for vm in vms_to_stop if vm.id.split("/")[4].lower() == cluster.resource_group.name.lower()):
            log.warning(
                f"Cluster {cluster.name} seems to be running an older version of BCM. "
                f"Since older clusters were not fully tagged, we "
                f"can't reliably link all BCM resources to the cluster, so *all* compute nodes in "
                f"the resource group {cluster.resource_group.name!r} (including other clusters' nodes in any)"
                f" will be stopped"
            )

    if vms_to_stop:
        log.info(
            f"Stopping all VMs for clusters: "
            f" {', '.join(cluster.name for cluster in clusters_to_stop)}"
        )
        deallocate_vms(azure_api_client, vms_to_stop, dry_run=config["dry_run"])


def deallocate_vms(azure_api_client, vms, dry_run):
    log.debug(f"Deallocating VMs {', '.join(vm.name for vm in vms)}")
    if dry_run:
        return

    async_deallocate_promises = [
        azure_api_client.compute_client.virtual_machines.begin_deallocate(
            resource_group_name=vm.id.split("/")[4],
            vm_name=vm.name,
        )
        for vm in vms
    ]

    multithread_run(lambda p: p.wait(), async_deallocate_promises, config["max_threads"])

    log.debug(f"Deallocated VMs {', '.join(vm.name for vm in vms)}")
