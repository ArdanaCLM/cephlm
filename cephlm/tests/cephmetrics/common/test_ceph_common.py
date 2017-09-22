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


import json
import mock
import subprocess
import unittest

import ConfigParser

from cephlm.common.exceptions import \
    CephCommandException, CephLMException, ShellCommandException

from cephlm.cephmetrics.common.ceph_common import Ceph
from cephlm.tests.cephmetrics.ceph.test_data import *   # noqa
from cephlm.tests.cephmetrics.usage.test_data import *   # noqa


class TestCeph(unittest.TestCase):
    @mock.patch('os.listdir')
    @mock.patch('os.path.exists')
    def test_get_ceph_config(self, mock_path, mock_listdir):
        mock_path.return_value = True
        mock_listdir.return_value = ["ceph1.conf", "ceph.mon.keyring",
                                     "ceph.client.admin.keyring"]
        with mock.patch('ConfigParser.RawConfigParser') as mocked:
            mocked.return_value = mock.MagicMock(
                spec=ConfigParser.RawConfigParser)
        cluster_name, config, config_file = Ceph._get_ceph_config()
        self.assertEqual(cluster_name, 'ceph1')

    @mock.patch('os.listdir')
    @mock.patch('os.path.exists')
    def test_get_ceph_config_error(self, mock_path, mock_listdir):
        mock_path.return_value = False
        mock_listdir.return_value = []
        regexp = "Could not find ceph configuration directory /etc/ceph"
        self.assertRaisesRegexp(CephLMException, regexp,
                                lambda: Ceph._get_ceph_config())

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_status(self, mock_cmd):
        Ceph._get_ceph_config = mock.Mock(
                return_value=('ceph1', dict(), '/etc/ceph/ceph.conf'))
        mock_cmd.return_value = json.dumps(ClusterStatusData.HEALTH_OK)
        result = Ceph.get_status()
        self.assertEqual(ClusterStatusData.HEALTH_OK, result)

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_status_error(self, mock_cmd):
        Ceph._get_ceph_config = mock.Mock(
                return_value=('ceph1', dict(), '/etc/ceph/ceph.conf'))
        regexp = "Failed to run command 'ceph -s'"
        mock_cmd.side_effect = ShellCommandException(regexp)
        self.assertRaisesRegexp(CephCommandException, regexp,
                                lambda: Ceph.get_status())

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_ceph_disk_list(self, mock_cmd):
        mock_cmd.return_value = CephDisksData.DISK_LIST_STDOUT_OK
        result = Ceph.get_ceph_disk_list()
        self.assertEqual(CephDisksData.DISK_LIST_OK, result)

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_ceph_disk_list_error(self, mock_cmd):
        regexp = "Failed to run command 'ceph-disk list'"
        mock_cmd.side_effect = ShellCommandException(regexp)
        self.assertRaisesRegexp(CephCommandException, regexp,
                                lambda: Ceph.get_ceph_disk_list())

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_osd_tree(self, mock_cmd):
        Ceph._get_ceph_config = mock.Mock(
                return_value=('ceph1', dict(), '/etc/ceph/ceph.conf'))
        mock_cmd.return_value = json.dumps(OSDData.TEST_OSD_TREE)
        result = Ceph.get_osd_tree()
        self.assertEqual(OSDData.TEST_OSD_TREE, result)

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_osd_tree_error(self, mock_cmd):
        Ceph._get_ceph_config = mock.Mock(
                return_value=('ceph1', dict(), '/etc/ceph/ceph.conf'))
        regexp = "Failed to run command 'ceph osd tree'"
        mock_cmd.side_effect = ShellCommandException(regexp)
        self.assertRaisesRegexp(CephCommandException, regexp,
                                lambda: Ceph.get_osd_tree())

    @mock.patch('cephlm.cephmetrics.common.ceph_common.Ceph.get_status')
    def test_get_monitors(self, mock_status):
        mock_status.return_value = ClusterStatusData.HEALTH_OK
        result = Ceph.get_monitors()
        expected_monitors = ["ceph3ntw-cp1-ceph-mon0001-osd-client",
                             "ceph3ntw-cp1-ceph-mon0002-osd-client",
                             "ceph3ntw-cp1-ceph-mon0003-osd-client"]
        self.assertEqual(result.sort(), expected_monitors.sort())

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_ceph_df(self, mock_cmd):
        Ceph._get_ceph_config = mock.Mock(
                return_value=('ceph1', dict(), '/etc/ceph/ceph1.conf'))
        mock_cmd.return_value = json.dumps(PoolData.test_pool_df)
        result = Ceph.get_ceph_df()
        self.assertEqual(PoolData.test_pool_df, result)

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_ceph_df_error(self, mock_cmd):
        Ceph._get_ceph_config = mock.Mock(
                return_value=('ceph1', dict(), '/etc/ceph/ceph1.conf'))
        regexp = "Failed to run command 'ceph df'"
        mock_cmd.side_effect = ShellCommandException(regexp)
        self.assertRaisesRegexp(CephCommandException, regexp,
                                lambda: Ceph.get_ceph_df())

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_quorum_status(self, mock_cmd):
        Ceph._get_ceph_config = mock.Mock(
                return_value=('ceph1', dict(), '/etc/ceph/ceph1.conf'))
        mock_cmd.return_value = json.dumps(MonitorQuorumData.QUORUM_OK)
        result = Ceph.get_quorum_status()
        self.assertEqual(MonitorQuorumData.QUORUM_OK, result)

    @mock.patch('cephlm.cephmetrics.common.ceph_common.run_cmd')
    def test_get_quorum_status_error(self, mock_cmd):
        Ceph._get_ceph_config = mock.Mock(
                return_value=('ceph1', dict(), '/etc/ceph/ceph1.conf'))
        regexp = "Failed to run command 'ceph quorum_status'"
        mock_cmd.side_effect = ShellCommandException(regexp)
        self.assertRaisesRegexp(CephCommandException, regexp,
                                lambda: Ceph.get_quorum_status())
