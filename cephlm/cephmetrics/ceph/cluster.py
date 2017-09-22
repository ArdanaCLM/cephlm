#!/usr/bin/python

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

import json
try:
    import rados
except ImportError:
    rados = None

from cephlm.cephmetrics.common.ceph_common import Ceph

from cephlm.common.exceptions import *    # noqa
from cephlm.utils.metricdata import MetricData
from cephlm.utils.values import Severity


class Cluster(Ceph):

    @staticmethod
    def check_status():
        """
        Display the status of the ceph cluster as returned by 'ceph -s' command
        """
        base_result = MetricData(
            name='cephlm.cluster.status',
            messages={
                'ok': 'Cluster is in healthy state.',
                'warn': 'Cluster is in warning state: {msg}.',
                'fail': 'Cluster is in error state: {msg}.',
                'unknown': 'Probe error: {msg}.'
            }
        )

        try:
            output = Cluster.get_status()
        except (CephLMException, CephCommandException,
                CephCommandTimeoutException) as e:
            result = base_result.child(msgkeys={'msg': str(e)})
            result.value = Severity.unknown
            return result

        status = output['health']['overall_status']
        summary = output['health']['summary']
        msgkeys = {'msg': Cluster._process_status_message(status, summary)}

        result = base_result.child(msgkeys=msgkeys)
        result.value = Cluster._process_status(status)
        return result

    @staticmethod
    def _process_status_message(status, summary):
        filtered_summary = [entry['summary'] for entry in summary
                            if entry['severity'] == status]
        # We could simply report the above list as message, but may end up
        # bloating the UI screen with a big message truncated by at will by
        # Monasca. Hence we truncate it ourselves and convey how many such
        # messages have been truncated
        message_list = list()
        message = str()
        msg_ctr = 0
        for element in filtered_summary:
            # 2048 chars is the message limit for Monasca of which the body
            # constitutes utmost 1916 chars. 1916 minus 56 chars for the
            # message prefix and truncated message suffix, we have 1860 left
            if len(message) > 1860:
                break
            message_list.append(element)
            message = ", ".join(message_list)
            msg_ctr += 1
        if msg_ctr < len(filtered_summary):
            message = "%s (truncated %s messages)" \
                      % (message, len(filtered_summary) - msg_ctr)
        return message

    @staticmethod
    def _process_status(status):
        status_map = {
            "HEALTH_OK": Severity.ok,
            "HEALTH_ERR": Severity.fail,
            "HEALTH_WARN": Severity.warn
        }
        value = status_map[status] \
            if status in status_map else Severity.unknown
        return value

    @staticmethod
    def _verify_monitor_connectivity(monitors):
        """
        Execute the 'status' command on each monitor using the rados module and
        report the connectivity status.
        :return: tuple of reachable and unreachable monitors list
        """
        rados_cmd = json.dumps({'prefix': 'status', 'format': 'json'})
        cluster_name, config, config_file = Cluster._get_ceph_config()
        unreachable_mons = []
        reachable_mons = []
        for monitor in monitors:
            with rados.Rados(clustername=cluster_name, conffile=config_file) \
                    as cluster_handle:
                ret, outbuf, outs = cluster_handle.mon_command(
                    rados_cmd,
                    b'',
                    timeout=Cluster.COMMAND_TIMEOUT_SECS,
                    target=monitor)
                if ret == 0:
                    reachable_mons.append(monitor)
                else:
                    unreachable_mons.append(monitor)
        return (reachable_mons, unreachable_mons)

    @staticmethod
    def check_monitor_connectivity():
        """
        Display the connectivity of the Ceph cluster to each Monitor host
        """
        base_result = MetricData(
            name='cephlm.connectivity.status',
            messages={
                'ok': 'Monitors {mons} are reachable.',
                'warn': 'Monitor(s) {mons} is/are unreachable.',
                'fail': 'Monitor(s) {mons} is/are unreachable.',
                'unknown': 'Probe error: {msg}.'
            }
        )

        try:
            monitors = Cluster.get_monitors()
            reachable, unreachable = \
                Cluster._verify_monitor_connectivity(monitors)
        except (CephLMException, CephCommandException) as e:
            result = base_result.child(msgkeys={'msg': str(e)})
            result.value = Severity.unknown
            return result

        if len(unreachable) == 0:
            result = base_result.child(
                msgkeys={'mons': ', '.join(reachable)})
            result.value = Severity.ok
        else:
            result = base_result.child(msgkeys={'mons':
                                                ', '.join(unreachable)})
            if len(reachable) == 0:
                result.value = Severity.fail
            else:
                result.value = Severity.warn
        return result
