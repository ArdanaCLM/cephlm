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

from cephlm.common.config import cfg
from cephlm.cephmetrics.common.ceph_common import Ceph
from cephlm.utils.metricdata import MetricData
from cephlm.common import exceptions as exc


class Pool(Ceph):

    INCLUDE_PRIVATE_POOLS = \
        cfg.getboolean('pools', 'include_private_pools')
    MAX_TOP_POOLS = 3

    @staticmethod
    def _fetch_top_pools(pools, key, n):
        pools.sort(key=lambda e: e['stats'][key], reverse=True)
        top_pools = list()
        for i in range(n):
            top_pools.append((pools[i]['name'], pools[i]['stats'][key]))
        return top_pools

    @staticmethod
    def _compute_pool_metric(pools, n=0):
        """Compute pool stats. Also, provides top 'n'
        pools by size as well as number of objects.
        :param pools: list of pools
        :param n: Number of top pools we want
        :return: pool_stats which is a dict of below format:
             pool_stats = {
                'count': 0
                'size_bytes': 0,
                'objects': 0,
                'top_pools_by_size': list()
                'top_pools_by_objects': list()
            }
        """
        top_pool_count = n if len(pools) > n else len(pools)
        pool_stats = {
            'count': 0,
            'size_bytes': 0,
            'objects': 0,
            'top_pools_by_size': list(),
            'top_pools_by_objects': list()
        }
        for p in pools:
            pool_stats['count'] += 1
            pool_stats['size_bytes'] = \
                pool_stats['size_bytes'] + p['stats']['bytes_used']
            pool_stats['objects'] = \
                pool_stats['objects'] + p['stats']['objects']
        if n != 0:
            pool_stats['top_pools_by_size'] = \
                Pool._fetch_top_pools(pools, 'bytes_used', top_pool_count)
            pool_stats['top_pools_by_objects'] = \
                Pool._fetch_top_pools(pools, 'objects', top_pool_count)
        return pool_stats

    @staticmethod
    def _stats():
        """ Compute pools stats so that data can be
        published using monasca. The data being generated is in
        following format:
            pool_stats = {
                total = {
                'count': 0
                'size_bytes': 0,
                'objects': 0,
                'top_pools_by_size': list()
                'top_pools_by_objects': list()
                }
                user = {
                'count': 0
                'size_bytes': 0,
                'objects': 0,
                'top_pools_by_size': list()
                'top_pools_by_objects': list()
                }
                internal = {
                'count': 0
                'size_bytes': 0,
                'objects': 0,
                }
            }
        """
        pools = Pool.get_ceph_df()
        pools = pools['pools']
        internal_pools = list()
        user_pools = list()
        total_pool_stats = dict()
        for p in pools:
            if p['name'][0] == '.':
                internal_pools.append(p)
            else:
                user_pools.append(p)
        user_pool_stats = \
            Pool._compute_pool_metric(user_pools, Pool.MAX_TOP_POOLS)
        internal_pool_stats = \
            Pool._compute_pool_metric(internal_pools)
        if Pool.INCLUDE_PRIVATE_POOLS:
            total_pool_stats = \
                Pool._compute_pool_metric(pools, Pool.MAX_TOP_POOLS)
        else:
            total_pool_stats = \
                Pool._compute_pool_metric(pools)
            total_pool_stats['top_pools_by_size'] = \
                user_pool_stats['top_pools_by_size']
            total_pool_stats['top_pools_by_objects'] = \
                user_pool_stats['top_pools_by_objects']
        pool_stats = {'total': total_pool_stats,
                      'user': user_pool_stats,
                      'internal': internal_pool_stats}
        return pool_stats

    @staticmethod
    def _return_total_metrics(pool_dict, key):
        """
        Reports the pool stats for requested metric
        Metric can be count, size or objects
        """
        msg = "User: %s, Internal: %s" % (pool_dict['user'][key],
                                          pool_dict['internal'][key])
        return msg, pool_dict['total'][key]

    @staticmethod
    def _pools_by_metric(pool_dict, key):
        """
        Reports top 3 pools by requested metric
        Metric can be size or objects
        """
        total_size = 0
        pool_string = ''
        top_pools = pool_dict['total'][key]
        for pool in top_pools:
            total_size += pool[1]
            pool_string += '%s(%s) ' % (pool[0], pool[1])
        pool_string = 'Pool ' + pool_string + 'is/are the top pools'
        return pool_string, total_size

    @staticmethod
    def pool_stats():
        """
        Publishes the pool statistics
        """
        result = list()
        INVALID_VALUE = -1
        probe_failed = False
        metric_dict = {'count': 'count',
                       'total_objects': 'objects',
                       'usage_bytes': 'size_bytes',
                       'top_three_by_usage_bytes': 'top_pools_by_size',
                       'top_three_by_objects': 'top_pools_by_objects',
                       }
        try:
            pool_dict = Pool._stats()
        except (exc.CephLMException, exc.CephCommandException,
                exc.CephCommandTimeoutException) as e:
            probe_failed = True
            msg = str(e)
        for metric_name, state in metric_dict.iteritems():
            name = "cephlm.pool.%s" % metric_name
            if probe_failed:
                value = INVALID_VALUE
            elif 'top_three' in metric_name:
                msg, value = Pool._pools_by_metric(pool_dict, state)
            else:
                msg, value = Pool._return_total_metrics(pool_dict, state)
            base_result = MetricData.single(name, value, message=msg)
            result.append(base_result)
        return result
