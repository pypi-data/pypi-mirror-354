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

import fnmatch
import logging
import re

from clusterondemand.clusternameprefix import clusterprefix_ns, ensure_cod_prefix
from clusterondemand.utils import confirm, confirm_ns, log_no_clusters_found
from clusterondemandconfig import ConfigNamespace, config

from . import clientutils
from .configuration import gcpcommon_ns

BCM_MAX_LIST_INSTANCES = 8

log = logging.getLogger("cluster-on-demand")


config_ns = ConfigNamespace("gcp.cluster.delete", help_section="cluster delete parameters")
config_ns.import_namespace(gcpcommon_ns)
config_ns.import_namespace(clusterprefix_ns)
config_ns.import_namespace(confirm_ns)

config_ns.add_switch_parameter(
    "dry_run",
    help="Do not actually delete the resources."
)
config_ns.add_repeating_positional_parameter(
    "filters",
    require_value=True,
    help="Cluster names or patterns. Wildcards are supported (e.g: \\*)",
)


def run_command() -> None:
    project = config["project_id"]
    bcm_instances = []
    bcm_addresses = []
    bcm_networks = []
    bcm_subnetworks = []
    bcm_nat_gateways = []
    bcm_firewalls = []
    bcm_forwarding_rules = []
    bcm_service_accounts = []
    bcm_target_instances = []
    bcm_filestores = []
    cluster_name_patterns = [ensure_cod_prefix(name) for name in config["filters"]]

    client = clientutils.GCPClient.from_config()
    cluster_tag_key = client.get_tagkey_id(config["project_id"], clientutils.BCM_TAG_CLUSTER)
    if cluster_tag_key is None:
        raise RuntimeError(f"Cannot find tag key: {clientutils.BCM_TAG_CLUSTER}")
    all_cluster_tag_values = client.list_tag_values(cluster_tag_key)
    cluster_name_regexes = [fnmatch.translate(pattern) for pattern in cluster_name_patterns]
    cluster_names = [
        cluster_name
        for cluster_name in [tagvalue.short_name for tagvalue in all_cluster_tag_values]
        if any(re.match(regex, cluster_name) for regex in cluster_name_regexes)
    ]
    cluster_tag_values = [t for t in all_cluster_tag_values if t.short_name in cluster_names]

    for cluster_name in cluster_names:
        bcm_resources = client.get_resources_for_cluster(project=project, cluster_name=cluster_name)
        log.info(f"For cluster {cluster_name} the following will be deleted:")
        if bcm_resources:
            bcm_cluster_instances = client.get_res_instances(reslist=bcm_resources)
            if bcm_cluster_instances:
                num_bcm_instances = len(bcm_cluster_instances)
                if num_bcm_instances >= BCM_MAX_LIST_INSTANCES and not config["verbose"]:
                    short_instance_list = ', '.join(instance.name for instance in
                                                    bcm_cluster_instances[0:BCM_MAX_LIST_INSTANCES])
                    log.info(f" - Instances        : {short_instance_list}... "
                             f"and {num_bcm_instances - BCM_MAX_LIST_INSTANCES} more")
                    log.info(f" *** Run with -v to display the full list of {num_bcm_instances} instances")
                else:
                    log.info(f" - Instances        : {', '.join(instance.name for instance in bcm_cluster_instances)}")
                bcm_instances += bcm_cluster_instances

            bcm_cluster_addresses = client.list_cluster_addresses(
                project=project, cluster_name=cluster_name
            )
            if bcm_cluster_addresses:
                log.info(f" - Addresses        : {', '.join(address.name for address in bcm_cluster_addresses)}")
                bcm_addresses += bcm_cluster_addresses

            bcm_cluster_subnetworks = client.get_res_subnetworks(reslist=bcm_resources)
            if bcm_cluster_subnetworks:
                log.info(f" - Subnetworks      : {', '.join(subnet.name for subnet in bcm_cluster_subnetworks)}")
                bcm_subnetworks += bcm_cluster_subnetworks

            bcm_cluster_networks = client.get_res_networks(reslist=bcm_resources)
            if bcm_cluster_networks:
                log.info(f" - Networks         : {', '.join(network.name for network in bcm_cluster_networks)}")
                bcm_networks += bcm_cluster_networks

            bcm_cluster_nat_gateways = client.get_res_nat_gateways(reslist=bcm_resources)
            if bcm_cluster_nat_gateways:
                log.info(
                    " - NAT Gateways     : " +
                    ', '.join(nat_gateway.name for nat_gateway in bcm_cluster_nat_gateways)
                )
                bcm_nat_gateways += bcm_cluster_nat_gateways

            bcm_cluster_firewalls = client.get_res_firewalls(reslist=bcm_resources)
            if bcm_cluster_firewalls:
                log.info(f" - Firewalls        : {', '.join(firewall.name for firewall in bcm_cluster_firewalls)}")
                bcm_firewalls += bcm_cluster_firewalls

            bcm_cluster_forwarding_rules = client.list_cluster_forwarding_rules(
                project=project, cluster_name=cluster_name
            )
            if bcm_cluster_forwarding_rules:
                log.info(f" - Forwarding Rules : {', '.join(fr.name for fr in bcm_cluster_forwarding_rules)}")
                bcm_forwarding_rules += bcm_cluster_forwarding_rules

            bcm_cluster_service_accounts = client.get_res_service_accounts(reslist=bcm_resources)
            if bcm_cluster_service_accounts:
                log.info(f" - Service Accounts : {', '.join(sa.email for sa in bcm_cluster_service_accounts)}")
                bcm_service_accounts += bcm_cluster_service_accounts

            bcm_cluster_target_instances = [r for r in bcm_resources if r.klass == "targetInstances"]
            if bcm_cluster_target_instances:
                log.info(f" - Target Instances : {', '.join(r.name for r in bcm_cluster_target_instances)}")
                bcm_target_instances += bcm_cluster_target_instances

            bcm_cluster_filestores = [r for r in bcm_resources if r.klass == "filestores"]
            if bcm_cluster_filestores:
                log.info(f" - Filestores       : {', '.join(r.name for r in bcm_cluster_filestores)}")
                bcm_filestores += bcm_cluster_filestores
        else:  # not bcm_resources -- a half-created/half-deleted cluster?
            log.info(f" - Tag value     : {clientutils.BCM_TAG_CLUSTER}={cluster_name}")

    if cluster_names:
        log.info("")
        log.info("This will delete the following clusters: {} and their resources listed above.".format(
            ', '.join(cluster_names)
        ))
        if not confirm("Would you like to continue?"):
            return
    else:
        log_no_clusters_found("delete")
        return

    resource_tags_values = {}
    if bcm_instances:
        resource_tags_values = client.get_bcm_instances_tagvalues(project=project, cluster_name=cluster_name)
    elif bcm_networks:
        resource_tags_values = client.get_bcm_networks_tagvalues(bcm_networks)

    client.delete_bcm_resources(
        project=project,
        forwarding_rules=bcm_forwarding_rules,
        target_instances=bcm_target_instances,
        instances=bcm_instances,
        filestores=bcm_filestores,
        addresses=bcm_addresses,
        service_accounts=bcm_service_accounts,
        firewalls=bcm_firewalls,
        nat_gateways=bcm_nat_gateways,
        subnetworks=bcm_subnetworks,
        networks=bcm_networks,
    )

    client.await_resources_deletion(project=project, cluster_name=cluster_name)
    client.delete_tagvalues(tag_values=resource_tags_values)
    client.cleanup_tagvalues(tag_values=cluster_tag_values)
    log.info("Done")
