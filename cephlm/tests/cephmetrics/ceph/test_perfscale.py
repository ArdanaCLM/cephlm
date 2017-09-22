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

import mock
import unittest

from cephlm.common.exceptions import \
    CephCommandException, ShellCommandException

from cephlm.tests.cephmetrics.ceph.test_data import *   # noqa
from cephlm.cephmetrics.ceph.perfscale import PerfScale
from cephlm.utils.values import Severity


class TestPerfScale(unittest.TestCase):
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_disks_size')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_memory_info')
    @mock.patch('cephlm.cephmetrics.common.ceph_common.'
                'Ceph.get_ceph_disk_list')
    def test_memory_ok(self, mock_list, mock_mem, mock_disks):
        mock_disks.return_value = HardwareData.DISK_SIZE_MAP
        mock_mem.return_value = HardwareData.MEMINFO_OK
        mock_list.return_value = CephDisksData.DISK_LIST_OK
        result = PerfScale.check_osd_node_ram()
        regexp = 'Host RAM\(.*\) meets \d+ GiB per TiB of data disk\(.*\)' \
                 ' guideline.'
        self.assertRegexpMatches(str(result), regexp)
        self.assertEqual(result.value, Severity.ok)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_disks_size')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_memory_info')
    @mock.patch('cephlm.cephmetrics.common.ceph_common.'
                'Ceph.get_ceph_disk_list')
    def test_memory_ok_min_ram(self, mock_list, mock_mem, mock_disks):
        mock_disks.return_value = HardwareData.DISK_SIZE_MAP_LOW_END
        mock_mem.return_value = HardwareData.MEMINFO_OK
        mock_list.return_value = CephDisksData.DISK_LIST_OK
        result = PerfScale.check_osd_node_ram()
        regexp = 'Host RAM\(.*\) meets \d+ GiB per TiB of data disk\(.*\)' \
                 ' guideline.'
        self.assertRegexpMatches(str(result), regexp)
        self.assertEqual(result.value, Severity.ok)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_disks_size')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_memory_info')
    @mock.patch('cephlm.cephmetrics.common.ceph_common.'
                'Ceph.get_ceph_disk_list')
    def test_memory_warn_min_ram(self, mock_list, mock_mem, mock_disks):
        mock_disks.return_value = HardwareData.DISK_SIZE_MAP_LOW_END
        mock_mem.return_value = HardwareData.MEMINFO_LOW_END
        mock_list.return_value = CephDisksData.DISK_LIST_OK
        result = PerfScale.check_osd_node_ram()
        regexp = 'Host RAM\(.*\) violates \d+ GiB per TiB of data disk\(.*\)' \
                 ' guideline.'
        self.assertRegexpMatches(str(result), regexp)
        self.assertEqual(result.value, Severity.warn)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_disks_size')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_memory_info')
    @mock.patch('cephlm.cephmetrics.common.ceph_common.'
                'Ceph.get_ceph_disk_list')
    def test_memory_warn(self, mock_list, mock_mem, mock_disks):
        mock_disks.return_value = HardwareData.DISK_SIZE_MAP
        mock_mem.return_value = HardwareData.MEMINFO_WARN
        mock_list.return_value = CephDisksData.DISK_LIST_OK
        result = PerfScale.check_osd_node_ram()
        regexp = 'Host RAM\(.*\) violates \d+ GiB per TiB of data disk\(.*\)' \
                 ' guideline.'
        self.assertRegexpMatches(str(result), regexp)
        self.assertEqual(result.value, Severity.warn)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_disks_size')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_memory_info')
    @mock.patch('cephlm.cephmetrics.common.ceph_common.'
                'Ceph.get_ceph_disk_list')
    def test_memory_unknown_error(self, mock_list, mock_mem, mock_disks):
        mock_disks.side_effect = ShellCommandException(
                "Failed to run command 'fdisk -l'")
        mock_mem.return_value = HardwareData.MEMINFO_WARN
        mock_list.return_value = CephDisksData.DISK_LIST_OK
        result = PerfScale.check_osd_node_ram()
        regexp = "Probe error: Failed to run command 'fdisk -l'"
        self.assertEqual(str(result), regexp)
        self.assertEqual(result.value, Severity.unknown)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_disks_size')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_system_memory_info')
    @mock.patch('cephlm.cephmetrics.common.ceph_common.'
                'Ceph.get_ceph_disk_list')
    def test_memory_ceph_error(self, mock_list, mock_mem, mock_disks):
        mock_disks.return_value = HardwareData.DISK_SIZE_MAP
        mock_mem.return_value = HardwareData.MEMINFO_WARN
        mock_list.side_effect = \
            CephCommandException("Failed to run command 'ceph-disk list'")
        result = PerfScale.check_osd_node_ram()
        regexp = "Probe error: Failed to run command 'ceph-disk list'"
        self.assertEqual(str(result), regexp)
        self.assertEqual(result.value, Severity.unknown)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_ceph_bind_ips')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_nic_info')
    def test_dedicated_nic_speed_ok(self, mock_nics, mock_bind):
        mock_bind.return_value = CephLmConfigData.BIND_IPS
        mock_nics.return_value = HardwareData.CEPH_DEDICATED_NIC_OK
        result = PerfScale.check_nic_speed()
        self.assertEqual(len(result),
                         len(CephLmConfigData.BIND_IPS))
        for entry in result:
            regexp = 'Logical NIC (.*) with ip (.*) supports' \
                     ' recommended minimum speed of (.*) Mb/s'
            self.assertRegexpMatches(str(entry), regexp)
            self.assertEqual(entry.value, Severity.ok)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_ceph_bind_ips')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_nic_info')
    def test_dedicated_nic_speed_warn(self, mock_nics, mock_bind):
        mock_bind.return_value = CephLmConfigData.BIND_IPS
        mock_nics.return_value = HardwareData.CEPH_DEDICATED_NIC_WARN
        result = PerfScale.check_nic_speed()
        self.assertEqual(len(result),
                         len(CephLmConfigData.BIND_IPS))
        for entry in result:
            regexp = 'Logical NIC (.*) with ip (.*) violates' \
                     ' recommended minimum speed of (.*) Mb/s'
            self.assertRegexpMatches(str(entry), regexp)
            self.assertEqual(entry.value, Severity.warn)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_ceph_bind_ips')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_nic_info')
    def test_shared_nic_speed_ok(self, mock_nics, mock_bind):
        mock_bind.return_value = CephLmConfigData.BIND_IPS
        mock_nics.return_value = HardwareData.CEPH_SHARED_NIC_OK
        result = PerfScale.check_nic_speed()
        self.assertEqual(len(result),
                         len(CephLmConfigData.BIND_IPS))
        for entry in result:
            regexp = 'Logical NIC (.*) with ip (.*) supports' \
                     ' recommended minimum speed of (.*) Mb/s'
            self.assertRegexpMatches(str(entry), regexp)
            self.assertEqual(entry.value, Severity.ok)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_ceph_bind_ips')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_nic_info')
    def test_shared_nic_speed_warn(self, mock_nics, mock_bind):
        mock_bind.return_value = CephLmConfigData.BIND_IPS
        mock_nics.return_value = HardwareData.CEPH_SHARED_NIC_WARN
        result = PerfScale.check_nic_speed()
        self.assertEqual(len(result),
                         len(CephLmConfigData.BIND_IPS))
        for entry in result:
            regexp = 'Logical NIC (.*) with ip (.*) violates' \
                     ' recommended minimum speed of (.*) Mb/s'
            self.assertRegexpMatches(str(entry), regexp)
            self.assertEqual(entry.value, Severity.warn)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_ceph_bind_ips')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_nic_info')
    def test_shared_nic_external_net_warn(self, mock_nics, mock_bind):
        mock_bind.return_value = CephLmConfigData.BIND_IPS
        mock_nics.return_value = HardwareData.CEPH_SHARED_EXTERNAL_NET
        result = PerfScale.check_nic_speed()
        self.assertEqual(len(result),
                         len(CephLmConfigData.BIND_IPS))
        for entry in result:
            regexp = 'WARN: Ceph and non-ceph networks detected' \
                     ' on same physical NIC'
            self.assertRegexpMatches(str(entry), regexp)
            self.assertEqual(entry.value, Severity.warn)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_ceph_bind_ips')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_nic_info')
    def test_shared_vcp_nic_ok(self, mock_nics, mock_bind):
        mock_bind.return_value = CephLmConfigData.BIND_IPS
        mock_nics.return_value = HardwareData.CEPH_SHARED_NIC_OK_VCP
        result = PerfScale.check_nic_speed()
        self.assertEqual(len(result),
                         len(CephLmConfigData.BIND_IPS))
        for entry in result:
            regexp = 'NIC speed monitoring is not supported on this host'
            self.assertRegexpMatches(str(entry), regexp)
            self.assertEqual(entry.value, Severity.ok)

    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_ceph_bind_ips')
    @mock.patch('cephlm.cephmetrics.ceph.perfscale.get_nic_info')
    def test_vcp_nic_external_net_warn(self, mock_nics, mock_bind):
        mock_bind.return_value = CephLmConfigData.BIND_IPS
        mock_nics.return_value = HardwareData.CEPH_SHARED_EXTERNAL_NET_VCP
        result = PerfScale.check_nic_speed()
        self.assertEqual(len(result),
                         len(CephLmConfigData.BIND_IPS))
        for entry in result:
            regexp = 'NIC speed monitoring is not supported on this host. ' \
                     'WARN: Ceph and non-ceph networks detected on same ' \
                     'physical NIC'
            self.assertRegexpMatches(str(entry), regexp)
            self.assertEqual(entry.value, Severity.warn)
