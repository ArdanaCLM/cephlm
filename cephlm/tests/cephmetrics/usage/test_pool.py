#!/usr/bin/env python
#
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

import mock
import unittest
from cephlm.tests.cephmetrics.usage.test_data import PoolData
from cephlm.cephmetrics.usage.pool import Pool
from cephlm.common import exceptions as exc


class TestCluster(unittest.TestCase):

    @mock.patch('cephlm.cephmetrics.usage.pool.Pool.get_ceph_df')
    def test_status_ok(self, mock_ceph_df):
        mock_ceph_df.return_value = PoolData.test_pool_df
        result = Pool.pool_stats()
        values = [(item.value, item.name) for item in result]
        metric_strings = [str(item) for item in result]
        for string in metric_strings:
            if string.startswith('Pool'):
                regexp = 'Pool .* is/are the top pools'
            else:
                regexp = "User: (\\d+), Internal: (\\d+)"
            self.assertRegexpMatches(string, regexp)
        self.assertEqual(sorted(values),
                         sorted(PoolData.test_pool_values))

    @mock.patch('cephlm.cephmetrics.usage.pool.Pool.get_ceph_df')
    def test_status_error(self, mock_ceph_df):
        mock_ceph_df.side_effect = \
            exc.CephCommandException("Probe error: Command 'ceph df' failed")
        result = Pool.pool_stats()
        values = [(item.value, item.name, str(item)) for item in result]
        self.assertEqual(sorted(values),
                         sorted(PoolData.test_pool_values_error))
