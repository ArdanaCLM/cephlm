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
import ConfigParser

from cephlm.common.exceptions import *   # noqa
from cephlm.tests.cephmetrics.ceph.test_data import *   # noqa
from cephlm.cephmetrics.ceph.monitor_quorum import Monitor
from cephlm.utils.values import Severity


class TestMonitors(unittest.TestCase):

    @mock.patch('cephlm.cephmetrics.ceph.monitor_quorum.'
                'Monitor.get_quorum_status')
    def test_status_ok(self, mock_status):
        mock_status.return_value = MonitorQuorumData.QUORUM_OK
        result = Monitor.quorum_status()
        self.assertEqual(str(result), 'Monitors are in quorum.')
        self.assertEqual(result.value, Severity.ok)

    @mock.patch('cephlm.cephmetrics.ceph.monitor_quorum.'
                'Monitor.get_quorum_status')
    def test_status_warn(self, mock_status):
        mock_status.return_value = MonitorQuorumData.QUORUM_WARN
        result = Monitor.quorum_status()
        self.assertEqual(str(result), 'Monitors (mcloud-ccp1-c1-m3-osd-client)'
                                      ' is/are not in quorum.')
        self.assertEqual(result.value, Severity.warn)

    @mock.patch('cephlm.cephmetrics.ceph.monitor_quorum.'
                'Monitor.get_quorum_status')
    @mock.patch('cephlm.cephmetrics.common.ceph_common.Ceph._get_ceph_config')
    def test_status_error(self, mock_config, mock_status):
        config = mock.Mock()
        config.get.return_value = MonitorQuorumData.Monitors
        mock_config.return_value = ('ceph', config, '/etc/ceph/ceph.conf')
        mock_status.side_effect = \
            CephCommandTimeoutException("Connecting to cluster timed out")
        result = Monitor.quorum_status()
        self.assertEqual(str(result), 'Monitors (mcloud-ccp1-c1-m1-osd-client,'
                                      'mcloud-ccp1-c1-m2-osd-client,'
                                      'mcloud-ccp1-c1-m3-osd-client)'
                                      ' have not formed quorum.')
        self.assertEqual(result.value, Severity.fail)

    @mock.patch('cephlm.cephmetrics.ceph.monitor_quorum.'
                'Monitor.get_quorum_status')
    def test_status_command_failure(self, mock_status):
        mock_status.side_effect = \
            CephCommandException("Failed to run command 'quorum_status'")
        result = Monitor.quorum_status()
        self.assertTrue("Probe error: Failed to run command 'quorum_status'"
                        in str(result))
        self.assertEqual(result.value, Severity.unknown)
