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

from cephlm.cephmetrics.common.ceph_common import Ceph
from cephlm.utils.metricdata import MetricData
from cephlm.common import exceptions as exc


class Capacity(Ceph):

    @staticmethod
    def _stats():
        """
        Computes capacity statistic
        """
        capacity_dict = Capacity.get_ceph_df()
        capacity_stats = dict()
        capacity_stats['total_bytes'] = capacity_dict['stats']['total_bytes']
        capacity_stats['used_bytes'] = \
            capacity_dict['stats']['total_used_bytes']
        capacity_stats['available_bytes'] = \
            capacity_dict['stats']['total_avail_bytes']
        capacity_stats['perc_utilization'] = \
            round(capacity_dict['stats']['total_used_bytes'] /
                  float(capacity_dict['stats']['total_bytes']), 4) * 100
        return capacity_stats

    @staticmethod
    def capacity_stats():
        """
        Publishes the capacity statistics
        """
        metric_list = ['total_bytes', 'used_bytes',
                       'available_bytes', 'perc_utilization']
        msg = ''
        result = list()
        capacity_dict = dict()
        INVALID_VALUE = -1
        probe_failed = False
        try:
            capacity_dict = Capacity._stats()
        except (exc.CephLMException, exc.CephCommandException,
                exc.CephCommandTimeoutException) as e:
            probe_failed = True
            msg = str(e)
        for metric_name in metric_list:
            name = "cephlm.capacity.%s" % metric_name
            value = capacity_dict[metric_name] \
                if not probe_failed else INVALID_VALUE
            base_result = MetricData.single(name, value, message=msg)
            result.append(base_result)
        return result
