#!/usr/bin/python

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

import swiftlm
from swiftlm.hp_hardware import hpssacli

from cephlm.cephmetrics.common.ceph_common import Ceph
from cephlm.utils.metricdata import MetricData
from cephlm.utils.values import Severity

from cephlm.common.exceptions import CephLMException


class HPssaCli(Ceph):
    @staticmethod
    def _override_plugin_settings():
        """
        Overrides configuration settings inherited from dependent packages
        like swiftlm
        :return: None
        """
        swiftlm.CONFIG_FILE = '/etc/cephlm/cephlm.conf'
        hpssacli.LOCK_FILE_COMMAND = \
            '/usr/bin/flock -w 10 /var/lock/hpssacli-cephlm.lock '

    @staticmethod
    def check_hpssacli():
        """
        Checks controller and drive information with hpssacli [Run as root]
        """
        base_result = MetricData(
            name='cephlm.hpssacli',
            messages=hpssacli.BASE_RESULT.messages
        )
        HPssaCli._override_plugin_settings()
        try:
            results = hpssacli.main()
        except Exception as e:
            # Unlike other parameters, we do not know the list of metrics here.
            # Hence there is no way to set each of them to error. Instead we
            # raise exception wich will be handled by the generic cephlm-probe
            # exception handler
            msg = "Unknown exception occured when " \
                  "executing swiftlm hpssacli module"
            raise CephLMException(msg)

        ceph_results = list()
        for entry in results:
            # Extract the main metric name, and strip off the parent hierarchy
            # E.g., swiftlm.hp_hardware.hpssacli.smart_array to smart_array
            name = entry.name.split('hpssacli.', 1)[1]
            # Clone the dimensions excluding entries pointing to external
            # service references
            dimensions = {key: value
                          for key, value in entry.dimensions.iteritems()
                          if key not in ['service']}
            # Convert external metric class to cephlm metric class
            result = base_result.child(name=name, dimensions=dimensions)
            result.value = HPssaCli._get_severity_level(entry.value)
            ceph_results.append(result)
        return ceph_results

    @staticmethod
    def _get_severity_level(value):
        # Convert external severity class to cephlm severity class
        severity_map = {
            '0': Severity.ok,
            '1': Severity.warn,
            '2': Severity.fail,
            '3': Severity.unknown
        }
        return severity_map.get(str(value), value)
