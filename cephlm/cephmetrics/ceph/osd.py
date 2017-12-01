#!/usr/bin/env python
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

from cephlm.common.config import cfg
from cephlm.cephmetrics.common.ceph_common import Ceph
from cephlm.utils.metricdata import MetricData
from cephlm.utils.values import Severity
from cephlm.common import exceptions as exc
from cephlm.utils.utility import string_range


class OSD(Ceph):
    OPTIMAL_OSD_PER_JOURNAL = int(cfg.get('osd', 'optimal_osd_per_journal'))

    @staticmethod
    def _stats():
        """
        Passes the statistics of osds in a dictionary to osd_stats
        """
        osd_dict = OSD.get_osd_tree()
        all_osds = list()
        osds_up = list()
        osds_down = list()
        osds_in = list()
        osds_out = list()
        output_dict = dict()
        for obj in osd_dict['nodes']:
            if obj['type'] == 'osd':
                all_osds.append(obj['id'])
                if obj['status'] == 'up':
                    osds_up.append(obj['id'])
                else:
                    osds_down.append(obj['id'])
                if isinstance(obj['reweight'], str):
                    obj['reweight'] = \
                        float(obj['reweight'].encode('ascii', 'ignore'))
                if obj['reweight'] == 0:
                    osds_out.append(obj['id'])
                else:
                    osds_in.append(obj['id'])
        output_dict['total_osds'] = all_osds
        output_dict['osds_up'] = osds_up
        output_dict['osds_down'] = osds_down
        output_dict['osds_in'] = osds_in
        output_dict['osds_out'] = osds_out
        return output_dict

    @staticmethod
    def _up_count(osd_dict):
        """
        Reports the count of osds that are up i.e running
        """
        return len(osd_dict['osds_up']),\
            string_range(sorted(osd_dict['osds_up']))

    @staticmethod
    def _up_out_count(osd_dict):
        """
        Reports the count of osds that are up but out of the cluster
        """
        osds_up_and_out = set(
            osd_dict['osds_up']).intersection(set(osd_dict['osds_out']))
        return len(osds_up_and_out),\
            string_range(sorted(list(osds_up_and_out)))

    @staticmethod
    def _down_count(osd_dict):
        """
        Reports the count of osds that are down i.e not running
        """
        return len(osd_dict['osds_down']),\
            string_range(sorted(osd_dict['osds_down']))

    @staticmethod
    def _down_in_count(osd_dict):
        """
        Reports the count of osds that are down and in the cluster
        """
        osds_down_and_in = set(
            osd_dict['osds_down']).intersection(set(osd_dict['osds_in']))
        return len(osds_down_and_in), string_range(sorted(osds_down_and_in))

    @staticmethod
    def _total_count(osd_dict):
        """
        Reports the total count of osds
        """
        return len(osd_dict['total_osds']),\
            string_range(sorted(osd_dict['total_osds']))

    @staticmethod
    def osd_stats():
        """
        Publishes the osd statistics
        """
        metric_dict = {'up': OSD._up_count, 'up_out': OSD._up_out_count,
                       'down': OSD._down_count, 'down_in': OSD._down_in_count,
                       'total': OSD._total_count}
        INVALID_VALUE = -1
        result = list()
        probe_failed = False
        try:
            osd_stats = OSD._stats()
        except (exc.CephLMException, exc.CephCommandException,
                exc.CephCommandTimeoutException) as e:
            probe_failed = True

        for metric_state, func in metric_dict.iteritems():
            name = "cephlm.osd.%s_count" % metric_state
            if probe_failed:
                value = INVALID_VALUE
                msg = "Probe error: Command 'ceph osd tree' failed"
            else:
                value, msg = func(osd_stats)
                msg = "OSD(s) %s" % msg if msg else "No OSD(s)"
                msg += " is/are in cluster" if metric_state == 'total' \
                    else " is/are %s" % metric_state
            base_result = MetricData.single(name, value, message=msg)
            result.append(base_result)
        return result

    @staticmethod
    def check_osd_journal_ratio():
        """
        Checks the ratio of osd disks mapped to journal disks
        """
        base_result = MetricData(
            name='cephlm.osd.osd_journal_ratio',
            messages={
                'ok': 'OSDs abide %s:1 OSD to Journal ratio'
                      % OSD.OPTIMAL_OSD_PER_JOURNAL,
                'warn': '{msg}',
                'unknown': 'Probe error: {msg}'
            }
        )
        try:
            journal_disks, data_disks = OSD.get_ceph_disk_list()
        except (exc.CephLMException, exc.CephCommandException) as e:
            result = base_result.child(msgkeys={'msg': str(e)})
            result.value = Severity.unknown
            return result

        # Set metric to warning state when there is both journal and data
        # partition on a given disk
        shared_osd_journals = \
            set(journal_disks.keys()).intersection(set(data_disks.keys()))

        # Set metric to warning state when the number of OSDs mapped to a given
        # journal disk exceeds the recommended limit
        non_optimal_disks = {key: val for key, val in journal_disks.iteritems()
                             if len(val) > OSD.OPTIMAL_OSD_PER_JOURNAL}

        return OSD._process_journal_status(base_result,
                                           shared_osd_journals,
                                           non_optimal_disks)

    @staticmethod
    def _process_journal_status(base_result, shared_osd_journals,
                                non_optimal_disks):
        if shared_osd_journals:
            msg = "Disk(s) %s contain both journal and data partitions" \
                  % ', '.join(shared_osd_journals)
            result = base_result.child(msgkeys={'msg': msg})
            result.value = Severity.warn
            return result

        if non_optimal_disks:
            msg = "Journal(s) %s violates the " \
                  "%s:1 OSD to Journal ratio guideline" \
                  % (', '.join(non_optimal_disks), OSD.OPTIMAL_OSD_PER_JOURNAL)
            result = base_result.child(msgkeys={'msg': msg})
            result.value = Severity.warn
            return result

        result = base_result.child()
        result.value = Severity.ok
        return result
