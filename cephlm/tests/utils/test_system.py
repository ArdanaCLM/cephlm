#!/usr/bin/python

# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
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

from cephlm.tests.utils.test_data import *   # noqa

from cephlm.utils.system import *   # noqa


class TestUtility(unittest.TestCase):

    def test_run_cmd(self):
        with mock.patch('subprocess.Popen') as mocked:
            mocked.return_value = mock.MagicMock(
                spec=subprocess.Popen,
                returncode=0,
                communicate=lambda: ("Mock Stdout",
                                     None))
            result = run_cmd("Mock Command")
        self.assertEqual(result, "Mock Stdout")

    def test_run_cmd_error(self):
        with mock.patch('subprocess.Popen') as mocked:
            mocked.return_value = mock.MagicMock(
                spec=subprocess.Popen,
                returncode=1,
                communicate=lambda: ("Mock Stdout",
                                     "Mock Stderr"))
            regexp = "Failed to run command 'Mock Command'"
            self.assertRaisesRegexp(ShellCommandException, regexp,
                                    lambda: run_cmd("Mock Command"))

    def test_run_cmd_failure(self):
        with mock.patch('subprocess.Popen') as mocked:
            mocked.side_effect = OSError("No such file or directory")
            regexp = "Failed to run command 'Mock Command'"
            self.assertRaisesRegexp(ShellCommandException, regexp,
                                    lambda: run_cmd("Mock Command"))

    @mock.patch('cephlm.utils.system.run_cmd')
    def test_get_system_memory_info(self, mock_cmd):
        mock_cmd.return_value = SystemData.MEM_INFO_STDOUT
        result = get_system_memory_info()
        self.assertEqual(result['MemTotal'], 7917952)

    @mock.patch('cephlm.utils.system.run_cmd')
    def test_get_system_disks_size(self, mock_cmd):
        mock_cmd.return_value = SystemData.DISKS_STDOUT
        result = get_system_disks_size()
        self.assertEqual(result['/dev/sda'], 42949672960)

    @mock.patch('cephlm.common.config.cfg.get')
    def test_get_ceph_bind_ips(self, mock_config):
        mock_config.side_effect = [
            CephLmConfigData.BIND_IPS['public_ip'],
            CephLmConfigData.BIND_IPS['private_ip']]
        ceph_bind_ips = get_ceph_bind_ips()
        self.assertEqual(ceph_bind_ips, CephLmConfigData.BIND_IPS)

    @mock.patch('cephlm.utils.system.run_cmd')
    def test_get_interface_speed(self, mock_run_cmd):
        mock_run_cmd.return_value = SystemData.IFACE_DATA
        self.assertEqual(get_interface_speed('eth0'), 1000)

    @mock.patch('netifaces.interfaces')
    @mock.patch('netifaces.ifaddresses')
    @mock.patch('cephlm.utils.system.get_interface_speed')
    def test_get_nic_info(self, mock_speed, mock_addresss, mock_ifaces):
        mock_speed.return_value = 1000
        mock_ifaces.return_value = SystemData.NET_IFACES
        mock_addresss.side_effect = SystemData.IF_ADDRESS
        nic_info = get_nic_info()
        self.assertEqual(sorted(nic_info), sorted(SystemData.NIC_INFO))
