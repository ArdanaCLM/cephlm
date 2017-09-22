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
from cephlm.tests.cephmetrics.system.test_data import HPssaCliData
from cephlm.cephmetrics.system.hpssacli import HPssaCli

from cephlm.common.exceptions import CephLMException


class TestHPssaCli(unittest.TestCase):

    @mock.patch('swiftlm.hp_hardware.hpssacli.main')
    def test_check_hpssacli_success(self, mock_hpssacli):
        mock_hpssacli.return_value = HPssaCliData.MOCK_RESPONSE
        result = HPssaCli.check_hpssacli()
        for entry in result:
            self.assertEqual(entry.dimensions['service'], 'ceph-storage')
            self.assertTrue(entry.name.startswith('cephlm.hpssacli'))

    @mock.patch('swiftlm.hp_hardware.hpssacli.main')
    def test_check_hpssacli_failure(self, mock_hpssacli):
        mock_hpssacli.side_effect = Exception("Unknown error")
        regexp = "Unknown exception occured when " \
                 "executing swiftlm hpssacli module"
        self.assertRaisesRegexp(CephLMException, regexp,
                                lambda: HPssaCli.check_hpssacli())
