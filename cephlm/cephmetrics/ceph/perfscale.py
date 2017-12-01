#!/usr/bin/python

# (c) Copyright 2016-2017 Hewlett Packard Enterprise Development LP
# (c) Copyright 2017 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from cephlm.common.config import cfg
from cephlm.cephmetrics.common.ceph_common import Ceph
from cephlm.common.exceptions import \
    CephCommandException,\
    CephLMException
from cephlm.utils.metricdata import MetricData
from cephlm.utils.values import Severity
from cephlm.utils.system import \
    get_system_disks_size, \
    get_system_memory_info, \
    get_ceph_bind_ips, \
    get_nic_info


class PerfScale:
    # Default memory recommendations
    MIN_RAM_GiB = int(cfg.get('perfscale', 'min_ram_gib'))
    GiB_PER_TiB_DATA = int(cfg.get('perfscale', 'ram_gib_per_tib'))
    # Default NIC speed recommendations
    PUB_NIC_SPEED = int(cfg.get('perfscale', 'public_nic_speed'))
    PVT_NIC_SPEED_MUL = \
        int(cfg.get('perfscale', 'private_nic_speed_multiplier'))
    PVT_NIC_SPEED = PUB_NIC_SPEED * PVT_NIC_SPEED_MUL

    @staticmethod
    def check_osd_node_ram():
        """
        Checks for optimal memory requirement in a Ceph OSD node [Run as root]
        """
        base_result = MetricData(
            name='cephlm.perfscale.osd_node_ram',
            messages={
                'ok': 'Host RAM({ram}GiB) meets %s GiB per TiB of data disk'
                      '({total_osd_size}TiB) guideline.'
                      % PerfScale.GiB_PER_TiB_DATA,
                'warn': 'Host RAM({ram}GiB) violates %s GiB per TiB of data disk'    # noqa
                        '({total_osd_size}TiB) guideline.'
                        % PerfScale.GiB_PER_TiB_DATA,
                'unknown': 'Probe error: {msg}'
            }
        )

        try:
            journal_disks, data_disks = Ceph.get_ceph_disk_list()
            mem_info = get_system_memory_info()
            disks_info = get_system_disks_size()
        except (CephLMException, CephCommandException) as e:
            result = base_result.child(msgkeys={'msg': str(e)})
            result.value = Severity.unknown
            return result

        total_osd_size, ram = PerfScale._process_osd_ram_data(
            data_disks, disks_info, mem_info)

        if not data_disks:
            # Ideally this check will not be run on non OSD nodes, but in case
            # it does, we return an empty list
            return list()

        result = base_result.child(
            msgkeys={'ram': '%s' % ram,
                     'total_osd_size': '%s' % total_osd_size})
        result.value = PerfScale._process_osd_ram_status(
            total_osd_size, ram)
        return result

    @staticmethod
    def _process_osd_ram_data(data_disks, disks_info, mem_info):
        """
        :param data_disks: A list or dict of data disks
        :param disks_info: A dict containing info of all system disks
        :param mem_info: A dict containing system memory parameters
        :return:
        """
        total_osd_size = 0
        for entry in data_disks:
            total_osd_size += disks_info[entry]

        # Convert Bytes to TiB
        total_osd_size = \
            round(float(total_osd_size) / (1024 * 1024 * 1024 * 1024), 1)
        # Convert KiB to GiB
        ram = round(float(mem_info['MemTotal']) / (1024 * 1024), 1)

        return total_osd_size, ram

    @staticmethod
    def _process_osd_ram_status(total_osd_size, ram):
        """
        :param ram: RAM in GiB
        :param total_osd_size:  Total OSD size in TiB
        :return: Severity class
        """
        # If the total OSD size is very less in the order of GiBs then, in TiB
        # it will virtually be 0.0 TiB. In such cases we check for a minimum
        # RAM criteria
        if not total_osd_size:
            severity = Severity.ok \
                if ram >= float(PerfScale.MIN_RAM_GiB) else Severity.warn
        else:
            severity = Severity.ok \
                if ram / total_osd_size >= float(PerfScale.GiB_PER_TiB_DATA) \
                else Severity.warn
        return severity

    @staticmethod
    def check_nic_speed():
        """
        Checks for optimal nic speed requirement in a ceph node [Run as root]
        """
        base_result = MetricData(
            name='cephlm.perfscale.nic_speed',
            messages={
                'ok': '{msg}',
                'warn': '{msg}',
                'unknown': 'Probe error: {msg}'
            }
        )
        try:
            nic_info = get_nic_info()
            ceph_bindings = get_ceph_bind_ips()
        except CephCommandException as e:
            result = base_result.child(msgkeys={'msg': str(e)})
            result.value = Severity.unknown
            return result

        # Public IP will always exist for a ceph node irrespective of the
        # network model. It is the network on which ceph client calls are made
        public_ip = ceph_bindings.get('public_ip', None)

        # Private IP or Cluster IP will exist only for OSD nodes provided the
        # deployment follows multi-network model
        private_ip = ceph_bindings.get('private_ip', None)

        nic_speeds = PerfScale._process_nic_speed(
            public_ip, private_ip, nic_info)

        shared_external_net = PerfScale._has_shared_external_networks(
            public_ip, private_ip, nic_info)

        metrics = list()
        for entry in ceph_bindings:
            ip = ceph_bindings[entry]
            severity, msg = PerfScale._format_nic_speed_status(
                ip, nic_speeds[ip], shared_external_net)
            metric = base_result.child(msgkeys={'msg': msg})
            metric.name = 'cephlm.perfscale.nic_speed_%s' \
                          % entry.replace('_ip', '')
            metric.value = severity
            metrics.append(metric)

        return metrics

    @staticmethod
    def _has_shared_external_networks(public_ip, private_ip, nic_info):
        ip_mac_map = {nic['ip']: nic['mac'] for nic in nic_info}
        ceph_ips = [public_ip, private_ip] if private_ip else [public_ip]
        ceph_macs = [ip_mac_map[ip] for ip in ceph_ips]

        for ip in ip_mac_map:
            if ip not in ceph_ips:
                if ip_mac_map[ip] in ceph_macs:
                    return True
        return False

    @staticmethod
    def _process_nic_speed(public_ip, private_ip, nic_info):
        ip_nic_map = {nic['ip']: nic for nic in nic_info}
        public_mac = ip_nic_map.get(public_ip)['mac']
        private_mac = ip_nic_map.get(private_ip)['mac'] if private_ip else None
        nic_speed = dict()

        # Evaluate the speed criteria for public network NIC
        # NOTE: This will be overwritten if it is found to be sharing the same
        # physical network interface with private network
        nic_speed[public_ip] = {
            'type': 'public',
            'speed': ip_nic_map[public_ip]['speed'],
            'intf': ip_nic_map.get(public_ip)['intf'],
            'recommended_speed':
                PerfScale.PUB_NIC_SPEED,
        }

        # Check the speed criteria for private network NIC
        if private_ip:
            nic_speed[private_ip] = {
                'type': 'private',
                'speed': ip_nic_map[private_ip]['speed'],
                'intf': ip_nic_map.get(private_ip)['intf'],
                'recommended_speed':
                    PerfScale.PVT_NIC_SPEED,
            }
            # If the private & public network are using the same physical
            # network interface, re-evaluate the recommended speed criteria
            if public_mac == private_mac:
                for entry in [public_ip, private_ip]:
                    nic_speed[entry]['recommended_speed'] = \
                        PerfScale.PUB_NIC_SPEED + PerfScale.PVT_NIC_SPEED
        return nic_speed

    @staticmethod
    def _format_nic_speed_status(ip, nic_detail, shared_external_net):
        if nic_detail['speed'] != 'NA':
            status = 'supports'
            severity = Severity.ok
            if nic_detail['speed'] < nic_detail['recommended_speed']:
                status = 'violates'
                severity = Severity.warn
            # Format NIC speed message
            msg = "Logical NIC {intf}({speed} Mb/s) with ip {ip} {status} " \
                  "recommended minimum speed of {recommended_speed} Mb/s"\
                .format(ip=ip, status=status, **nic_detail)
        else:
            severity = Severity.ok
            msg = "NIC speed monitoring is not supported on this host"

        # If non ceph networks are detected on samce cep
        if shared_external_net:
            msg = '%s. WARN: Ceph and non-ceph networks detected ' \
                  'on same physical NIC' % msg
            severity = Severity.warn
        return severity, msg
