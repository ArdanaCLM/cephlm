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

from cephlm.common.exceptions import CephCommandException

from cephlm.tests.cephmetrics.ceph.test_data import *   # noqa
from cephlm.cephmetrics.ceph.cluster import Cluster
from cephlm.utils.values import Severity


class TestCluster(unittest.TestCase):
    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_status')
    def test_status_ok(self, mock_status):
        mock_status.return_value = ClusterStatusData.HEALTH_OK
        result = Cluster.check_status()
        self.assertEqual(str(result), 'Cluster is in healthy state.')
        self.assertEqual(result.value, Severity.ok)

    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_status')
    def test_status_warn(self, mock_status):
        mock_status.return_value = ClusterStatusData.HEALTH_WARN
        result = Cluster.check_status()
        self.assertTrue('Cluster is in warning state: ' in str(result))
        self.assertEqual(result.value, Severity.warn)

    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_status')
    def test_status_error(self, mock_status):
        mock_status.return_value = ClusterStatusData.HEALTH_ERR
        result = Cluster.check_status()
        self.assertTrue('Cluster is in error state: ' in str(result))
        self.assertEqual(result.value, Severity.fail)

    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_status')
    def test_status_unknown_error(self, mock_status):
        mock_status.return_value = ClusterStatusData.HEALTH_NULL
        result = Cluster.check_status()
        self.assertTrue('Probe error: ' in str(result))
        self.assertEqual(result.value, Severity.unknown)

    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_status')
    def test_status_command_failure(self, mock_status):
        mock_status.side_effect = \
            CephCommandException("Failed to run command 'ceph-disk list'")
        result = Cluster.check_status()
        self.assertTrue("Probe error: Failed to run command 'ceph-disk list'"
                        in str(result))
        self.assertEqual(result.value, Severity.unknown)
