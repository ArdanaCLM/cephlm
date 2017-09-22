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

from cephlm.tests.cephmetrics.usage.test_data import PoolData, CapacityData
from cephlm.common.exceptions import CephCommandException, CephLMException
from cephlm.cephmetrics.usage.capacity import Capacity


class TestCapacity(unittest.TestCase):

    @mock.patch('cephlm.cephmetrics.usage.capacity.Capacity.get_ceph_df')
    def test_capacity_stats_ok(self, mock_status):
        mock_status.return_value = PoolData.test_pool_df
        result = Capacity.capacity_stats()
        values = [(item.value, item.name) for item in result]
        self.assertEqual(sorted(values),
                         sorted(CapacityData.test_capacity_values))

    @mock.patch('cephlm.cephmetrics.usage.capacity.Capacity.get_ceph_df')
    def test_capacity_stats_error(self, mock_status):
        mock_status.side_effect = \
            CephCommandException("Failed to run command 'ceph df'")
        result = Capacity.capacity_stats()
        values = [(item.value, item.name, str(item)) for item in result]
        self.assertEqual(sorted(values),
                         sorted(CapacityData.test_capacity_values_error))
