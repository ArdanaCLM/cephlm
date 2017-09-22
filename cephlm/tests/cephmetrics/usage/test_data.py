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


class PoolData:

    test_pool_df = {"stats": {
        "total_bytes": 14995448135680,
        "total_used_bytes": 224784384,
        "total_avail_bytes": 14995223351296
    },
        "pools": [
            {
                "name": "rbd",
                "id": 0,
                "stats": {
                    "kb_used": 0,
                    "bytes_used": 0,
                    "max_avail": 8997130402342,
                    "objects": 0
                }
            },
            {
                "name": ".rgw.root",
                "id": 1,
                "stats": {
                    "kb_used": 1,
                    "bytes_used": 848,
                    "max_avail": 8997130402342,
                    "objects": 3
                }
            },
            {
                "name": ".rgw.control",
                "id": 2,
                "stats": {
                    "kb_used": 0,
                    "bytes_used": 0,
                    "max_avail": 8997130402342,
                    "objects": 8
                }
            },
            {
                "name": ".rgw",
                "id": 3,
                "stats": {
                    "kb_used": 0,
                    "bytes_used": 0,
                    "max_avail": 8997130402342,
                    "objects": 0
                }
            },
            {
                "name": ".rgw.gc",
                "id": 4,
                "stats": {
                    "kb_used": 0,
                    "bytes_used": 0,
                    "max_avail": 8997130402342,
                    "objects": 32
                }
            },
            {
                "name": ".users.uid",
                "id": 5,
                "stats": {
                    "kb_used": 0,
                    "bytes_used": 0,
                    "max_avail": 8997130402342,
                    "objects": 0
                }
            }
        ]
    }
    test_pool_values_error = [(-1, 'cephlm.pool.count',
                              "Probe error: Command 'ceph df' failed"),
                              (-1, 'cephlm.pool.total_objects',
                              "Probe error: Command 'ceph df' failed"),
                              (-1, 'cephlm.pool.usage_bytes',
                              "Probe error: Command 'ceph df' failed"),
                              (-1, 'cephlm.pool.top_three_by_usage_bytes',
                              "Probe error: Command 'ceph df' failed"),
                              (-1, 'cephlm.pool.top_three_by_objects',
                              "Probe error: Command 'ceph df' failed")]
    test_pool_values = [(6, 'cephlm.pool.count'),
                        (43, 'cephlm.pool.total_objects'),
                        (848, 'cephlm.pool.usage_bytes'),
                        (0, 'cephlm.pool.top_three_by_usage_bytes'),
                        (0, 'cephlm.pool.top_three_by_objects')]


class CapacityData:
    test_capacity_values_error = [(-1, 'cephlm.capacity.total_bytes',
                                  "Failed to run command 'ceph df'"),
                                  (-1, 'cephlm.capacity.available_bytes',
                                  "Failed to run command 'ceph df'"),
                                  (-1, 'cephlm.capacity.used_bytes',
                                  "Failed to run command 'ceph df'"),
                                  (-1, 'cephlm.capacity.perc_utilization',
                                  "Failed to run command 'ceph df'")]
    test_capacity_values = [(14995448135680, 'cephlm.capacity.total_bytes'),
                            (14995223351296,
                             'cephlm.capacity.available_bytes'),
                            (224784384, 'cephlm.capacity.used_bytes'),
                            (0.0, 'cephlm.capacity.perc_utilization')]
