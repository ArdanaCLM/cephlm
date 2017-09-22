#!/usr/bin/python
#
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

from cephlm.cephmetrics.common.ceph_common import Ceph
from cephlm.common.exceptions import CephCommandException,\
    CephCommandTimeoutException
from cephlm.utils.metricdata import MetricData
from cephlm.utils.values import Severity


class Monitor(Ceph):

    @staticmethod
    def quorum_status():
        """
        Reports the status of monitor quorum
        """
        base_result = MetricData(
            name='cephlm.monitor.quorum',
            messages={
                'ok': 'Monitors are in quorum.',
                'warn': 'Monitors ({msg}) is/are not in quorum.',
                'fail': 'Monitors ({msg}) have not formed quorum.',
                'unknown': 'Probe error: {msg}.'
            }
        )
        msg = ''
        value = Severity.ok
        try:
            output = Monitor.get_quorum_status()
            quorum = output['quorum']
            monitors = output['monmap']['mons']
            if len(quorum) < len(monitors):
                value = Severity.warn
                for mon in monitors:
                    if mon['rank'] not in quorum:
                        msg += mon['name'] + ', '
                msg = msg[:-2]
        except CephCommandTimeoutException:
            value = Severity.fail
            cluster_name, config, config_file = Ceph._get_ceph_config()
            msg = config.get('global', 'mon_host')
        except CephCommandException as e:
            value = Severity.unknown
            msg = str(e)
        result = base_result.child(msgkeys={'msg': msg})
        result.value = value
        return result
