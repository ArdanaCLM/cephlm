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


from cephlm.utils.metricdata import MetricData
from cephlm.utils.values import Severity


class HPssaCliData:
    MOCK_BASE_RESULT = MetricData(
        name='swiftlm.hpssacli',
        messages={
            'no_battery': 'No cache battery',
            'unknown': 'hpssacli command failed',
            'controller_status': '{sub_component} status is {status}',
            'in_hba_mode': 'Controller is in HBA mode;'
                           ' performance will be poor',
            'physical_drive': 'Drive {serial_number}: '
            '{box}:{bay} has status: {status}',
            'l_drive': 'Logical Drive {logical_drive} has status: {status}',
            'l_cache': 'Logical Drive {logical_drive}'
                       ' has cache status: {caching}',
            'ok': 'OK',
            'fail': 'FAIL',
        }
    )

    MOCK_CHILD_FLOAT = MOCK_BASE_RESULT.child()
    MOCK_CHILD_FLOAT.name = 'swiftlm.hp_hardware.hpssacli.smart_array.firmware'
    MOCK_CHILD_FLOAT.value = 3.0
    MOCK_CHILD_FLOAT.dimensions = {'component': 'controller',
                                   'controller_slot': '1',
                                   'hostname': 'ardana-ccp-ceph0001-clm',
                                   'model': 'Smart HBA H240',
                                   'service': 'object-storage'}

    MOCK_CHILD_OK = MOCK_BASE_RESULT.child()
    MOCK_CHILD_OK.name = 'swiftlm.hp_hardware.hpssacli.smart_array'
    MOCK_CHILD_OK.value = Severity.ok
    MOCK_CHILD_OK.dimensions = {'component': 'controller',
                                'sub_component': 'controller_not_hba_mode',
                                'controller_slot': '1',
                                'hostname': 'ardana-ccp-ceph0001-clm',
                                'model': 'Smart HBA H240',
                                'service': 'object-storage'}

    MOCK_CHILD_FAIL = MOCK_BASE_RESULT.child()
    MOCK_CHILD_FAIL.name = 'swiftlm.hp_hardware.hpssacli.smart_array'
    MOCK_CHILD_FAIL.value = Severity.fail
    MOCK_CHILD_FAIL.dimensions = {'component': 'controller',
                                  'sub_component': 'battery_capacitor_status',
                                  'controller_slot': '1',
                                  'hostname': 'ardana-ccp-ceph0001-clm',
                                  'model': 'Smart HBA H240',
                                  'service': 'object-storage'}

    MOCK_RESPONSE = [MOCK_CHILD_FLOAT, MOCK_CHILD_OK, MOCK_CHILD_FAIL]
