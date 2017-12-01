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

from cephlm.common.exceptions import CephCommandException
from cephlm.tests.cephmetrics.ceph.test_data import ExtendedPGData
from cephlm.cephmetrics.ceph.pg import PG


class TestCluster(unittest.TestCase):
    @mock.patch('cephlm.cephmetrics.ceph.pg.PG.get_status')
    def test_pg_health_ok(self, mock_status):
        mock_status.return_value = ExtendedPGData.HEALTH_OK
        result = PG.pg_stats()
        pgs = str(result).split(', ')
        values = (result.value, result.name, sorted(pgs))
        self.assertEqual(sorted(values),
                         sorted(ExtendedPGData.test_pg_health_ok_values))

    @mock.patch('cephlm.cephmetrics.ceph.pg.PG.get_status')
    def test_pg_health_error(self, mock_status):
        mock_status.return_value = ExtendedPGData.HEALTH_ERR
        result = PG.pg_stats()
        pgs = str(result).split(', ')
        values = (result.value, result.name, sorted(pgs))
        self.assertEqual(sorted(values),
                         sorted(ExtendedPGData.test_pg_health_error_values))

    @mock.patch('cephlm.cephmetrics.ceph.pg.PG.get_status')
    def test_pg_error(self, mock_status):
        mock_status.side_effect = \
            CephCommandException("Command 'ceph -s' failed")
        result = PG.pg_stats()
        values = (result.value, result.name, str(result))
        self.assertEqual(sorted(values),
                         sorted(ExtendedPGData.test_pg_values_error))
