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


class PG(Ceph):

    @staticmethod
    def _stats():
        """
        Reports the count of pgs in various states
        pg_state_count: {'active': 414,
                    'count': 768,
                    'degraded': 361,
                    'remapped': 361,
                    'incomplete': 354}
        """
        pgs_dict = PG.get_status()
        pg_state_count = dict()
        for obj in pgs_dict['pgmap']['pgs_by_state']:
            pg_name = obj['state_name'].encode('ascii', 'ignore')
            pg_count = obj['count']
            pgs = pg_name.split('+')
            for state in pgs:
                if state not in pg_state_count:
                    pg_state_count[state] = pg_count
                else:
                    pg_state_count[state] += pg_count
        pg_state_count['count'] = pgs_dict['pgmap']['num_pgs']
        return pg_state_count

    @staticmethod
    def pg_stats():
        """
        Function to aggregate all metrics
        """
        msg = ''
        INVALID_VALUE = -1
        probe_failed = False
        try:
            pg_stats = PG._stats()
        except (exc.CephLMException, exc.CephCommandException,
                exc.CephCommandTimeoutException) as e:
            probe_failed = True
            msg = 'Probe error: ' + str(e)
        if probe_failed:
            value = INVALID_VALUE
        else:
            value = pg_stats.pop('count')
            for pg_state, count in pg_stats.iteritems():
                msg += '%s=%s, ' % (pg_state, count)
            msg = msg[:-2]
        name = "cephlm.pg.count"
        base_result = MetricData.single(name, value, message=msg)
        return base_result
