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
from itertools import count

from cephlm.common.exceptions import CephCommandException

from cephlm.tests.cephmetrics.ceph.test_data import *   # noqa
from cephlm.cephmetrics.ceph import cluster
from cephlm.utils.values import Severity


class TestCluster(unittest.TestCase):
    def setUp(self):
        self.monitors = ClusterStatusData.HEALTH_OK['quorum_names']

    @mock.patch(
        'cephlm.cephmetrics.ceph.cluster.Cluster._verify_monitor_connectivity')
    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_monitors')
    def test_connectivity_ok(self, mock_get_mon, mock_conn_status):
        mock_get_mon.return_value = self.monitors
        mock_conn_status.return_value = (self.monitors, [])
        result = cluster.Cluster.check_monitor_connectivity()
        self.assertEqual(str(result),
                         'Monitors %s are reachable.' %
                         ', '.join(mock_conn_status.return_value[0]))
        self.assertEqual(result.value, Severity.ok)

    @mock.patch(
        'cephlm.cephmetrics.ceph.cluster.Cluster._verify_monitor_connectivity')
    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_monitors')
    def test_connectivity_warn(self, mock_get_mon, mock_conn_status):
        mock_get_mon.return_value = self.monitors
        mock_conn_status.return_value = (self.monitors[:2], self.monitors[2:])
        result = cluster.Cluster.check_monitor_connectivity()
        self.assertEqual(str(result),
                         'Monitor(s) %s is/are unreachable.' %
                         ', '.join(mock_conn_status.return_value[1]))
        self.assertEqual(result.value, Severity.warn)

    @mock.patch(
        'cephlm.cephmetrics.ceph.cluster.Cluster._verify_monitor_connectivity')
    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_monitors')
    def test_connectivity_failure(self, mock_get_mon, mock_conn_status):
        mock_get_mon.return_value = self.monitors
        mock_conn_status.return_value = ([], self.monitors)
        result = cluster.Cluster.check_monitor_connectivity()
        self.assertEqual(str(result),
                         'Monitor(s) %s is/are unreachable.' %
                         ', '.join(mock_conn_status.return_value[1]))
        self.assertEqual(result.value, Severity.fail)

    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_monitors')
    def test_connectivity_unknown_error_cmd(self, mock_get_mon):
        msg = "No such file or directory"
        mock_get_mon.side_effect = CephCommandException(msg)
        result = cluster.Cluster.check_monitor_connectivity()
        self.assertEqual(str(result), 'Probe error: %s.' % msg)
        self.assertEqual(result.value, Severity.unknown)

    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster._get_ceph_config')
    @mock.patch.object(cluster, 'rados')
    def test_verify_connectivity_ok(self, mock_rados, mock_get_ceph_config):
        class DummyRados:
            def __init__(self, clustername, conffile):
                pass

            def __enter__(self):
                return self

            def __exit__(self, type_, value, traceback):
                return False

            def mon_command(self, cmd, inbuf, timeout, target):
                return 0, '', ''

        mock_get_ceph_config.return_value = ('ceph', 'config',
                                             '/etc/ceph/ceph.conf')
        mock_rados.Rados = DummyRados
        result = cluster.Cluster._verify_monitor_connectivity(self.monitors)
        self.assertEqual(result[0], self.monitors)
        self.assertEqual(len(result[1]), 0)

    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster._get_ceph_config')
    @mock.patch.object(cluster, 'rados')
    def test_verify_connectivity_error_all(self, mock_rados,
                                           mock_get_ceph_config):
        class DummyRados:
            def __init__(self, clustername, conffile):
                pass

            def __enter__(self):
                return self

            def __exit__(self, type_, value, traceback):
                return False

            def mon_command(self, cmd, inbuf, timeout, target):
                return -4, '', ''

        mock_get_ceph_config.return_value = ('ceph', 'config',
                                             '/etc/ceph/ceph.conf')
        mock_rados.Rados = DummyRados
        result = cluster.Cluster._verify_monitor_connectivity(self.monitors)
        self.assertEqual(len(result[0]), 0)
        self.assertEqual(result[1], self.monitors)

    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster._get_ceph_config')
    @mock.patch.object(cluster, 'rados')
    def test_verify_connectivity_error_one(self, mock_rados,
                                           mock_get_ceph_config):
        class DummyRados:
            _ids = count(0)

            def __init__(self, clustername, conffile):
                self.id = DummyRados._ids.next()

            def __enter__(self):
                return self

            def __exit__(self, type_, value, traceback):
                return False

            def mon_command(self, cmd, inbuf, timeout, target):
                if self.id == 0:
                    return (-4, '', '')
                else:
                    return (0, '', '')

        mock_get_ceph_config.return_value = ('ceph', 'config',
                                             '/etc/ceph/ceph.conf')
        mock_rados.Rados = DummyRados
        result = cluster.Cluster._verify_monitor_connectivity(self.monitors)
        self.assertEqual(result[0], self.monitors[1:])
        self.assertEqual(result[1], [self.monitors[0]])
