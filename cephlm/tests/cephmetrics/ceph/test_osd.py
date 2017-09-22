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

import re
import mock
import unittest

from cephlm.common.exceptions import CephCommandException

from cephlm.tests.cephmetrics.ceph.test_data import *   # noqa
from cephlm.cephmetrics.ceph.osd import OSD
from cephlm.utils.values import Severity


class TestOSD(unittest.TestCase):

    @mock.patch('cephlm.cephmetrics.ceph.osd.OSD.get_osd_tree')
    def test_osd_status_ok(self, mock_status):
        mock_status.return_value = OSDData.TEST_OSD_TREE
        result = OSD.osd_stats()
        values = [(item.value, item.name, str(item)) for item in result]
        self.assertEqual(sorted(values), sorted(OSDData.TEST_OSD_VALUES))

    @mock.patch('cephlm.cephmetrics.ceph.osd.OSD.get_osd_tree')
    def test_osd_status_null(self, mock_status):
        mock_status.return_value = OSDData.TEST_OSD_TREE_NULL
        result = OSD.osd_stats()
        values = [(item.value, item.name, str(item)) for item in result]
        self.assertEqual(sorted(values), sorted(OSDData.TEST_OSD_NULL_VALUES))

    @mock.patch('cephlm.cephmetrics.ceph.cluster.Cluster.get_osd_tree')
    def test_osd_status_error(self, mock_status):
        mock_status.side_effect = \
            CephCommandException("No such file or directory")
        result = OSD.osd_stats()
        values = [(item.value, item.name, str(item)) for item in result]
        self.assertEqual(sorted(values), sorted(OSDData.TEST_OSD_VALUES_ERROR))

    @mock.patch('cephlm.cephmetrics.ceph.osd.OSD.get_ceph_disk_list')
    def test_osd_journal_ratio_ok(self, mock_list):
        mock_list.return_value = CephDisksData.DISK_LIST_OK
        result = OSD.check_osd_journal_ratio()
        self.assertEqual(str(result), 'OSDs abide 4:1 OSD to Journal ratio')
        self.assertEqual(result.value, Severity.ok)

    @mock.patch('cephlm.cephmetrics.ceph.osd.OSD.get_ceph_disk_list')
    def test_osd_journal_ratio_warn(self, mock_list):
        mock_list.return_value = CephDisksData.DISK_LIST_RATIO_WARN
        result = OSD.check_osd_journal_ratio()
        regexp = 'Journal\(s\) .* violates the 4:1 OSD to Journal ratio'
        self.assertRegexpMatches(str(result), regexp)
        self.assertEqual(result.value, Severity.warn)

    @mock.patch('cephlm.cephmetrics.ceph.osd.OSD.get_ceph_disk_list')
    def test_osd_journal_shared_warn(self, mock_list):
        mock_list.return_value = CephDisksData.DISK_LIST_DATA_JOURNAL_WARN
        result = OSD.check_osd_journal_ratio()
        regexp = 'Disk\(s\) .* contain both ' \
                 'journal and data partitions'
        self.assertRegexpMatches(str(result), regexp)
        self.assertEqual(result.value, Severity.warn)

    @mock.patch('cephlm.cephmetrics.ceph.osd.OSD.get_ceph_disk_list')
    def test_osd_journal_command_failure(self, mock_list):
        mock_list.side_effect = \
            CephCommandException("No such file or directory")
        result = OSD.check_osd_journal_ratio()
        self.assertTrue('Probe error: No such file or directory'
                        in str(result))
        self.assertEqual(result.value, Severity.unknown)
