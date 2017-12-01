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


class ClusterStatusData:
    HEALTH_NULL = {
        "health": {
            "overall_status": "",
            "summary": []
        }
    }
    HEALTH_OK = {
        "health": {
            "health": {
                "health_services": [
                    {
                        "mons": [
                            {
                                "name": "ceph3ntw-cp1-ceph-mon0001-osd-client",
                                "kb_total": 143785016,
                                "kb_used": 1315912,
                                "kb_avail": 136295200,
                                "avail_percent": 94,
                                "last_updated": "2016-06-17 12:25:47.742581",
                                "store_stats": {
                                    "bytes_total": 2435576,
                                    "bytes_sst": 0,
                                    "bytes_log": 905820,
                                    "bytes_misc": 1529756,
                                    "last_updated": "0.000000"
                                },
                                "health": "HEALTH_OK"
                            },
                            {
                                "name": "ceph3ntw-cp1-ceph-mon0002-osd-client",
                                "kb_total": 143785016,
                                "kb_used": 1320188,
                                "kb_avail": 136290924,
                                "avail_percent": 94,
                                "last_updated": "2016-06-17 12:25:47.718357",
                                "store_stats": {
                                    "bytes_total": 2884324,
                                    "bytes_sst": 0,
                                    "bytes_log": 1354316,
                                    "bytes_misc": 1530008,
                                    "last_updated": "0.000000"
                                },
                                "health": "HEALTH_OK"
                            },
                            {
                                "name": "ceph3ntw-cp1-ceph-mon0003-osd-client",
                                "kb_total": 143785016,
                                "kb_used": 1310932,
                                "kb_avail": 136300180,
                                "avail_percent": 94,
                                "last_updated": "2016-06-17 12:26:06.823494",
                                "store_stats": {
                                    "bytes_total": 2883119,
                                    "bytes_sst": 0,
                                    "bytes_log": 1354316,
                                    "bytes_misc": 1528803,
                                    "last_updated": "0.000000"
                                },
                                "health": "HEALTH_OK"
                            }
                        ]
                    }
                ]
            },
            "summary": [],
            "timechecks": {
                "epoch": 8,
                "round": 4754,
                "round_status": "finished",
                "mons": [
                    {
                        "name": "ceph3ntw-cp1-ceph-mon0001-osd-client",
                        "skew": "0.000000",
                        "latency": "0.000000",
                        "health": "HEALTH_OK"
                    },
                    {
                        "name": "ceph3ntw-cp1-ceph-mon0002-osd-client",
                        "skew": "-0.000000",
                        "latency": "0.000870",
                        "health": "HEALTH_OK"
                    },
                    {
                        "name": "ceph3ntw-cp1-ceph-mon0003-osd-client",
                        "skew": "-0.000001",
                        "latency": "0.000845",
                        "health": "HEALTH_OK"
                    }
                ]
            },
            "overall_status": "HEALTH_OK",
            "detail": []
        },
        "fsid": "2645bbf6-16d0-4c42-8835-8ba9f5c95a1d",
        "election_epoch": 8,
        "quorum": [
            0,
            1,
            2
        ],
        "quorum_names": [
            "ceph3ntw-cp1-ceph-mon0001-osd-client",
            "ceph3ntw-cp1-ceph-mon0002-osd-client",
            "ceph3ntw-cp1-ceph-mon0003-osd-client"
        ],
        "monmap": {
            "epoch": 1,
            "fsid": "2645bbf6-16d0-4c42-8835-8ba9f5c95a1d",
            "modified": "2016-06-07 19:20:39.570970",
            "created": "2016-06-07 19:20:39.570970",
            "mons": [
                {
                    "rank": 0,
                    "name": "ceph3ntw-cp1-ceph-mon0001-osd-client",
                    "addr": "192.168.56.11:6789/0"
                },
                {
                    "rank": 1,
                    "name": "ceph3ntw-cp1-ceph-mon0002-osd-client",
                    "addr": "192.168.56.12:6789/0"
                },
                {
                    "rank": 2,
                    "name": "ceph3ntw-cp1-ceph-mon0003-osd-client",
                    "addr": "192.168.56.13:6789/0"
                }
            ]
        },
        "osdmap": {
            "osdmap": {
                "epoch": 100,
                "num_osds": 8,
                "num_up_osds": 8,
                "num_in_osds": 8,
                "full": False,
                "nearfull": False
            }
        },
        "pgmap": {
            "pgs_by_state": [
                {
                    "state_name": "active+clean",
                    "count": 1900
                }
            ],
            "version": 11189,
            "num_pgs": 1900,
            "data_bytes": 3265269948,
            "bytes_used": 10288062464,
            "bytes_avail": 18198891069440,
            "bytes_total": 18209179131904
        },
        "mdsmap": {
            "epoch": 1,
            "up": 0,
            "in": 0,
            "max": 1,
            "by_rank": []
        }
    }
    HEALTH_WARN = {
        "health": {
            "health": {
                "health_services": [
                    {
                        "mons": [
                            {
                                "name": "ceph3ntw-cp1-ceph-mon0001-osd-client",
                                "kb_total": 143785016,
                                "kb_used": 1323236,
                                "kb_avail": 136287876,
                                "avail_percent": 94,
                                "last_updated": "2016-06-17 12:37:55.302375",
                                "store_stats": {
                                    "bytes_total": 9754279,
                                    "bytes_sst": 0,
                                    "bytes_log": 8383029,
                                    "bytes_misc": 1371250,
                                    "last_updated": "0.000000"
                                },
                                "health": "HEALTH_OK"
                            },
                            {
                                "name": "ceph3ntw-cp1-ceph-mon0002-osd-client",
                                "kb_total": 143785016,
                                "kb_used": 1331064,
                                "kb_avail": 136280048,
                                "avail_percent": 94,
                                "last_updated": "2016-06-17 12:37:55.290406",
                                "store_stats": {
                                    "bytes_total": 13922081,
                                    "bytes_sst": 0,
                                    "bytes_log": 12549953,
                                    "bytes_misc": 1372128,
                                    "last_updated": "0.000000"
                                },
                                "health": "HEALTH_OK"
                            },
                            {
                                "name": "ceph3ntw-cp1-ceph-mon0003-osd-client",
                                "kb_total": 143785016,
                                "kb_used": 1321788,
                                "kb_avail": 136289324,
                                "avail_percent": 94,
                                "last_updated": "2016-06-17 12:37:55.306747",
                                "store_stats": {
                                    "bytes_total": 13921895,
                                    "bytes_sst": 0,
                                    "bytes_log": 12549811,
                                    "bytes_misc": 1372084,
                                    "last_updated": "0.000000"
                                },
                                "health": "HEALTH_OK"
                            }
                        ]
                    }
                ]
            },
            "summary": [
                {
                    "severity": "HEALTH_WARN",
                    "summary": "1398 pgs degraded"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "441 pgs stuck unclean"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "recovery 641/2544 objects degraded (25.197%)"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "2/8 in osds are down"
                }
            ],
            "timechecks": {
                "epoch": 14,
                "round": 2,
                "round_status": "finished",
                "mons": [
                    {
                        "name": "ceph3ntw-cp1-ceph-mon0001-osd-client",
                        "skew": "0.000000",
                        "latency": "0.000000",
                        "health": "HEALTH_OK"
                    },
                    {
                        "name": "ceph3ntw-cp1-ceph-mon0002-osd-client",
                        "skew": "0.000000",
                        "latency": "0.001742",
                        "health": "HEALTH_OK"
                    },
                    {
                        "name": "ceph3ntw-cp1-ceph-mon0003-osd-client",
                        "skew": "0.000000",
                        "latency": "0.002167",
                        "health": "HEALTH_OK"
                    }
                ]
            },
            "overall_status": "HEALTH_WARN",
            "detail": []
        },
        "fsid": "2645bbf6-16d0-4c42-8835-8ba9f5c95a1d",
        "election_epoch": 14,
        "quorum": [
            0,
            1,
            2
        ],
        "quorum_names": [
            "ceph3ntw-cp1-ceph-mon0001-osd-client",
            "ceph3ntw-cp1-ceph-mon0002-osd-client",
            "ceph3ntw-cp1-ceph-mon0003-osd-client"
        ],
        "monmap": {
            "epoch": 1,
            "fsid": "2645bbf6-16d0-4c42-8835-8ba9f5c95a1d",
            "modified": "2016-06-07 19:20:39.570970",
            "created": "2016-06-07 19:20:39.570970",
            "mons": [
                {
                    "rank": 0,
                    "name": "ceph3ntw-cp1-ceph-mon0001-osd-client",
                    "addr": "192.168.56.11:6789/0"
                },
                {
                    "rank": 1,
                    "name": "ceph3ntw-cp1-ceph-mon0002-osd-client",
                    "addr": "192.168.56.12:6789/0"
                },
                {
                    "rank": 2,
                    "name": "ceph3ntw-cp1-ceph-mon0003-osd-client",
                    "addr": "192.168.56.13:6789/0"
                }
            ]
        },
        "osdmap": {
            "osdmap": {
                "epoch": 106,
                "num_osds": 8,
                "num_up_osds": 6,
                "num_in_osds": 8,
                "full": False,
                "nearfull": False
            }
        },
        "pgmap": {
            "pgs_by_state": [
                {
                    "state_name": "active+degraded",
                    "count": 1398
                },
                {
                    "state_name": "active+clean",
                    "count": 502
                }
            ],
            "version": 11211,
            "num_pgs": 1900,
            "data_bytes": 3265269948,
            "bytes_used": 10292371456,
            "bytes_avail": 18198886760448,
            "bytes_total": 18209179131904,
            "degraded_objects": 641,
            "degraded_total": 2544,
            "degraded_ratio": "25.197"
        },
        "mdsmap": {
            "epoch": 1,
            "up": 0,
            "in": 0,
            "max": 1,
            "by_rank": []
        }
    }
    HEALTH_ERR = {
        "health": {
            "health": {
                "health_services": [
                    {
                        "mons": [
                            {
                                "name": "mcloud-ccp1-c1-m1-osd-client",
                                "kb_total": 54712404,
                                "kb_used": 6534080,
                                "kb_avail": 45623884,
                                "avail_percent": 83,
                                "last_updated": "2016-06-17 11:43:33.845387",
                                "store_stats": {
                                    "bytes_total": 2152202,
                                    "bytes_sst": 0,
                                    "bytes_log": 608284,
                                    "bytes_misc": 1543918,
                                    "last_updated": "0.000000"
                                },
                                "health": "HEALTH_OK"
                            },
                            {
                                "name": "mcloud-ccp1-c1-m2-osd-client",
                                "kb_total": 54712404,
                                "kb_used": 6367924,
                                "kb_avail": 45790040,
                                "avail_percent": 83,
                                "last_updated": "2016-06-17 11:44:10.774470",
                                "store_stats": {
                                    "bytes_total": 2333063,
                                    "bytes_sst": 0,
                                    "bytes_log": 789069,
                                    "bytes_misc": 1543994,
                                    "last_updated": "0.000000"
                                },
                                "health": "HEALTH_OK"
                            },
                            {
                                "name": "mcloud-ccp1-c1-m3-osd-client",
                                "kb_total": 54712404,
                                "kb_used": 6375356,
                                "kb_avail": 45782608,
                                "avail_percent": 83,
                                "last_updated": "2016-06-17 11:43:25.624756",
                                "store_stats": {
                                    "bytes_total": 2303369,
                                    "bytes_sst": 0,
                                    "bytes_log": 759389,
                                    "bytes_misc": 1543980,
                                    "last_updated": "0.000000"
                                },
                                "health": "HEALTH_OK"
                            }
                        ]
                    }
                ]
            },
            "summary": [
                {
                    "severity": "HEALTH_WARN",
                    "summary": "26 pgs degraded"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "288 pgs incomplete"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "282 pgs peering"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "832 pgs stale"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "570 pgs stuck inactive"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "832 pgs stuck stale"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "596 pgs stuck unclean"
                },
                {
                    "severity": "HEALTH_WARN",
                    "summary": "recovery 2/129 objects degraded (1.550%)"
                },
                {
                    "severity": "HEALTH_ERR",
                    "summary": "no osds"
                }
            ],
            "timechecks": {
                "epoch": 458,
                "round": 274,
                "round_status": "finished",
                "mons": [
                    {
                        "name": "mcloud-ccp1-c1-m1-osd-client",
                        "skew": "0.000000",
                        "latency": "0.000000",
                        "health": "HEALTH_OK"
                    },
                    {
                        "name": "mcloud-ccp1-c1-m2-osd-client",
                        "skew": "0.000000",
                        "latency": "0.001945",
                        "health": "HEALTH_OK"
                    },
                    {
                        "name": "mcloud-ccp1-c1-m3-osd-client",
                        "skew": "0.000000",
                        "latency": "0.051806",
                        "health": "HEALTH_OK"
                    }
                ]
            },
            "overall_status": "HEALTH_ERR",
            "detail": []
        },
        "fsid": "2645bbf6-16d0-4c42-8835-8ba9f5c95a1d",
        "election_epoch": 458,
        "quorum": [
            0,
            1,
            2
        ],
        "quorum_names": [
            "mcloud-ccp1-c1-m1-osd-client",
            "mcloud-ccp1-c1-m2-osd-client",
            "mcloud-ccp1-c1-m3-osd-client"
        ],
        "monmap": {
            "epoch": 1,
            "fsid": "2645bbf6-16d0-4c42-8835-8ba9f5c95a1d",
            "modified": "2016-06-10 10:34:47.152728",
            "created": "2016-06-10 10:34:47.152728",
            "mons": [
                {
                    "rank": 0,
                    "name": "mcloud-ccp1-c1-m1-osd-client",
                    "addr": "192.168.12.2:6789/0"
                },
                {
                    "rank": 1,
                    "name": "mcloud-ccp1-c1-m2-osd-client",
                    "addr": "192.168.12.3:6789/0"
                },
                {
                    "rank": 2,
                    "name": "mcloud-ccp1-c1-m3-osd-client",
                    "addr": "192.168.12.4:6789/0"
                }
            ]
        },
        "osdmap": {
            "osdmap": {
                "epoch": 115,
                "num_osds": 0,
                "num_up_osds": 0,
                "num_in_osds": 0,
                "full": False,
                "nearfull": False
            }
        },
        "pgmap": {
            "pgs_by_state": [
                {
                    "state_name": "stale+peering",
                    "count": 282
                },
                {
                    "state_name": "stale+active+clean",
                    "count": 236
                },
                {
                    "state_name": "stale+incomplete",
                    "count": 288
                },
                {
                    "state_name": "stale+active+degraded",
                    "count": 26
                }
            ],
            "version": 2574,
            "num_pgs": 832,
            "data_bytes": 840,
            "bytes_used": 0,
            "bytes_avail": 0,
            "bytes_total": 0,
            "degraded_objects": 2,
            "degraded_total": 129,
            "degraded_ratio": "1.550"
        },
        "mdsmap": {
            "epoch": 1,
            "up": 0,
            "in": 0,
            "max": 1,
            "by_rank": []
        }
    }


class ExtendedPGData(ClusterStatusData):
    """
    Note: ClusterStatusData is imported as we use 'ceph -s' command
          to get pgmap
    """
    test_pg_health_ok_values = (1900, 'cephlm.pg.count',
                                ['active=1900', 'clean=1900'])
    test_pg_health_error_values = (832, 'cephlm.pg.count',
                                   ['active=262', 'clean=236', 'degraded=26',
                                    'incomplete=288', 'peering=282',
                                    'stale=832'])
    test_pg_values_error = (-1, 'cephlm.pg.count',
                            "Probe error: Command 'ceph -s' failed")


class OSDData:
    TEST_OSD_TREE = {
        "nodes": [
            {
                "id": -1,
                "name": "default",
                "type": "root",
                "type_id": 10,
                "children": [
                    -4,
                    -3,
                    -2
                ]
            },
            {
                "id": -2,
                "name": "ardana-cp1-ceph0001-mgmt",
                "type": "host",
                "type_id": 1,
                "children": [
                    7,
                    4,
                    1
                ]
            },
            {
                "id": 1,
                "name": "osd.1",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 4,
                "name": "osd.4",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 7,
                "name": "osd.7",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": -3,
                "name": "ardana-cp1-ceph0003-mgmt",
                "type": "host",
                "type_id": 1,
                "children": [
                    8,
                    5,
                    2
                ]
            },
            {
                "id": 2,
                "name": "osd.2",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "down",
                "reweight": 0,
                "primary_affinity": 1
            },
            {
                "id": 5,
                "name": "osd.5",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "down",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 8,
                "name": "osd.8",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": -4,
                "name": "ardana-cp1-ceph0002-mgmt",
                "type": "host",
                "type_id": 1,
                "children": [
                    6,
                    3,
                    0
                ]
            },
            {
                "id": 0,
                "name": "osd.0",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 3,
                "name": "osd.3",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 0,
                "primary_affinity": 1
            },
            {
                "id": 6,
                "name": "osd.6",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 0,
                "primary_affinity": 1
            }
        ],
        "stray": []
    }
    TEST_OSD_TREE_NULL = {
        "nodes": [
            {
                "id": -1,
                "name": "default",
                "type": "root",
                "type_id": 10,
                "children": [
                    -3,
                    -4,
                    -2
                ]
            },
            {
                "id": -2,
                "name": "ardana-cp1-ceph0003-mgmt",
                "type": "host",
                "type_id": 1,
                "children": [
                    8,
                    5,
                    2
                ]
            },
            {
                "id": 2,
                "name": "osd.2",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 5,
                "name": "osd.5",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 8,
                "name": "osd.8",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": -4,
                "name": "ardana-cp1-ceph0001-mgmt",
                "type": "host",
                "type_id": 1,
                "children": [
                    7,
                    4,
                    1
                ]
            },
            {
                "id": 1,
                "name": "osd.1",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 4,
                "name": "osd.4",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 7,
                "name": "osd.7",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": -3,
                "name": "ardana-cp1-ceph0002-mgmt",
                "type": "host",
                "type_id": 1,
                "children": [
                    6,
                    3,
                    0
                ]
            },
            {
                "id": 0,
                "name": "osd.0",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 3,
                "name": "osd.3",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            },
            {
                "id": 6,
                "name": "osd.6",
                "type": "osd",
                "type_id": 0,
                "crush_weight": 1,
                "depth": 2,
                "exists": 1,
                "status": "up",
                "reweight": 1,
                "primary_affinity": 1
            }
        ],
        "stray": []
    }
    TEST_OSD_VALUES_ERROR = [(-1, 'cephlm.osd.down_count',
                              "Probe error: Command 'ceph osd tree' failed"),
                             (-1, 'cephlm.osd.down_in_count',
                              "Probe error: Command 'ceph osd tree' failed"),
                             (-1, 'cephlm.osd.total_count',
                              "Probe error: Command 'ceph osd tree' failed"),
                             (-1, 'cephlm.osd.up_count',
                              "Probe error: Command 'ceph osd tree' failed"),
                             (-1, 'cephlm.osd.up_out_count',
                              "Probe error: Command 'ceph osd tree' failed")]
    TEST_OSD_VALUES = [(2, 'cephlm.osd.down_count', 'OSD(s) 2,5 is/are down'),
                       (1, 'cephlm.osd.down_in_count',
                        'OSD(s) 5 is/are down_in'),
                       (9, 'cephlm.osd.total_count',
                        'OSD(s) 0-8 is/are in cluster'),
                       (7, 'cephlm.osd.up_count',
                        'OSD(s) 0-1,3-4,6-8 is/are up'),
                       (2, 'cephlm.osd.up_out_count',
                        'OSD(s) 3,6 is/are up_out')]
    TEST_OSD_NULL_VALUES = [(0, 'cephlm.osd.down_count',
                             'No OSD(s) is/are down'),
                            (0, 'cephlm.osd.down_in_count',
                             'No OSD(s) is/are down_in'),
                            (9, 'cephlm.osd.total_count',
                             'OSD(s) 0-8 is/are in cluster'),
                            (9, 'cephlm.osd.up_count', 'OSD(s) 0-8 is/are up'),
                            (0, 'cephlm.osd.up_out_count',
                             'No OSD(s) is/are up_out')]


class CephDisksData:
    DISK_LIST_STDOUT_OK = \
        'WARNING:ceph-disk:Old blkid does not support' \
        ' ID_PART_ENTRY_* fields, trying sgdisk;' \
        ' may not correctly identify ceph volumes with dmcryp\n' \
        '/dev/sda :\n' \
        '/dev/sda1 other, 21686148-6449-6e6f-744e-656564454649\n' \
        '/dev/sda2 other, ext3\n' \
        '/dev/sda3 other, ext3, mounted on /boot\n' \
        '/dev/sda4 other, LVM2_member\n' \
        '/dev/sdb other, unknown\n' \
        '/dev/sdc :\n' \
        '/dev/sdc1 ceph data, active, cluster ceph, osd.7,' \
        ' journal /dev/sdd1\n'\
        '/dev/sdd :\n' \
        '/dev/sdd1 ceph journal, for /dev/sdc1\n' \
        '/dev/sde :\n' \
        '/dev/sde1 ceph data, active, cluster ceph, osd.4,' \
        ' journal /dev/sdg2\n' \
        '/dev/sdf :\n' \
        '/dev/sdf1 ceph data, active, cluster ceph, osd.2,' \
        ' journal /dev/sdg1\n' \
        '/dev/sdg :\n' \
        '/dev/sdg1 ceph journal, for /dev/sdf1\n' \
        '/dev/sdg2 ceph journal, for /dev/sde1\n'

    DISK_LIST_OK = (
        {
            '/dev/sdg': [
                '/dev/sdg1 ceph journal, for /dev/sdf1',
                '/dev/sdg2 ceph journal, for /dev/sde1'
            ],
            '/dev/sdd': [
                '/dev/sdd1 ceph journal, for /dev/sdc1'
            ]
        },
        {
            '/dev/sdf': [
                '/dev/sdf1 ceph data, active, cluster ceph, osd.2,'
                ' journal /dev/sdg1'
            ],
            '/dev/sde': [
                '/dev/sde1 ceph data, active, cluster ceph, osd.4,'
                ' journal /dev/sdg2'
            ],
            '/dev/sdc': [
                '/dev/sdc1 ceph data, active, cluster ceph, osd.7,'
                ' journal /dev/sdd1'
            ]
        }
    )

    DISK_LIST_RATIO_WARN = (
        {
            '/dev/sdg': [
                '/dev/sdg1 ceph journal, for /dev/sdb1',
                '/dev/sdg2 ceph journal, for /dev/sdc1',
                '/dev/sdg3 ceph journal, for /dev/sdd1',
                '/dev/sdg4 ceph journal, for /dev/sde1',
                '/dev/sdg5 ceph journal, for /dev/sdf1'
            ]
        },
        {
            '/dev/sdf': [
                '/dev/sdf1 ceph data, active, cluster ceph, osd.5,'
                ' journal /dev/sdg5'
            ],
            '/dev/sdd': [
                '/dev/sdd1 ceph data, active, cluster ceph, osd.3,'
                ' journal /dev/sdg3'
            ],
            '/dev/sde': [
                '/dev/sde1 ceph data, active, cluster ceph, osd.4,'
                ' journal /dev/sdg4'
            ],
            '/dev/sdb': [
                '/dev/sdb1 ceph data, active, cluster ceph, osd.1,'
                ' journal /dev/sdg1'
            ],
            '/dev/sdc': [
                '/dev/sdc1 ceph data, active, cluster ceph, osd.2,'
                ' journal /dev/sdg2'
            ]
        }
    )

    DISK_LIST_DATA_JOURNAL_WARN = (
        {
            '/dev/sdg': [
                '/dev/sdg1 ceph journal, for /dev/sdf1',
                '/dev/sdg2 ceph journal, for /dev/sde1'
            ],
            '/dev/sdd': [
                '/dev/sdd1 ceph journal, for /dev/sdc1'
            ],
            '/dev/sdh': [
                '/dev/sdh2 ceph journal, for /dev/sdh1'
            ]
        },
        {
            '/dev/sdf': [
                '/dev/sdf1 ceph data, active, cluster ceph, osd.2,'
                ' journal /dev/sdg1'
            ],
            '/dev/sde': [
                '/dev/sde1 ceph data, active, cluster ceph, osd.4,'
                ' journal /dev/sdg2'
            ],
            '/dev/sdc': [
                '/dev/sdc1 ceph data, active, cluster ceph, osd.7,'
                ' journal /dev/sdd1'
            ],
            '/dev/sdh': [
                '/dev/sdh1 ceph data, active, cluster ceph, osd.9,'
                ' journal /dev/sdh2'
            ]
        }
    )


class HardwareData:
    MEMINFO_OK = {
        'MemTotal': 263848920,
        'MemFree': 658064
    }

    MEMINFO_WARN = {
        'MemTotal': 4048240,
        'MemFree': 1135564
    }

    MEMINFO_LOW_END = {
        'MemTotal': 524288,
        'MemFree': 124288
    }

    DISK_SIZE_MAP = {
        '/dev/sda': 3.299e+12,
        '/dev/sdb': 3.299e+12,
        '/dev/sdc': 3.299e+12,
        '/dev/sdd': 3.299e+12,
        '/dev/sde': 3.299e+12,
        '/dev/sdf': 3.299e+12,
        '/dev/sdh': 3.299e+12,
    }

    DISK_SIZE_MAP_LOW_END = {
        '/dev/sda': 1.074e+10,
        '/dev/sdb': 1.074e+10,
        '/dev/sdc': 1.074e+10,
        '/dev/sdd': 1.074e+10,
        '/dev/sde': 1.074e+10,
        '/dev/sdf': 1.074e+10,
        '/dev/sdh': 1.074e+10,
    }

    # The below data represents the responses of utils method get_nic_info()
    # which returns the list of interfaces with IP and filters out the rest.

    # In dedicated NIC case the hierarchy of NICs are as follows:
    #
    # hed1 ---> Untagged Ardana network
    # hed2 ---> vlan1747 (tagged MGMT network)
    # hed3 ---> vlan1749 (tagged Ceph public network)
    # hed4 ---> vlan1750 (tagged Ceph private network)

    CEPH_DEDICATED_NIC_OK = [
        {'ip': '127.0.0.1', 'mac': '00:00:00:00:00:00',
         'intf': 'lo', 'speed': 'NA'},
        {'ip': '192.17.43.23', 'mac': '58:20:b1:01:71:dc',
         'intf': 'hed1', 'speed': 1000},
        {'ip': '192.17.47.22', 'mac': '00:11:0a:6b:33:03',
         'intf': 'vlan1747', 'speed': 1000},
        {'ip': '192.17.49.11', 'mac': '00:11:0a:6b:44:04',
         'intf': 'vlan1749', 'speed': 10000},
        {'ip': '192.17.50.3', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1750', 'speed': 40000}
    ]

    CEPH_DEDICATED_NIC_WARN = [
        {'ip': '127.0.0.1', 'mac': '00:00:00:00:00:00',
         'intf': 'lo', 'speed': 'NA'},
        {'ip': '192.17.43.23', 'mac': '58:20:b1:01:71:dc',
         'intf': 'hed1', 'speed': 1000},
        {'ip': '192.17.47.22', 'mac': '00:11:0a:6b:33:03',
         'intf': 'vlan1747', 'speed': 1000},
        {'ip': '192.17.49.11', 'mac': '00:11:0a:6b:44:04',
         'intf': 'vlan1749', 'speed': 1000},
        {'ip': '192.17.50.3', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1750', 'speed': 10000}
    ]

    # In shared NIC case the hierarchy of NICs are as follows:
    #
    # hed1 ---> Untagged Ardana network
    # hed2 ---> vlan1747 (tagged MGMT network)
    # hed3 -|         |-> vlan1749 (tagged Ceph public network)
    #       |- bond0 -|
    # hed4 -|         |-> vlan1750 (tagged Ceph private network)

    CEPH_SHARED_NIC_OK = [
        {'ip': '127.0.0.1', 'mac': '00:00:00:00:00:00',
         'intf': 'lo', 'speed': 'NA'},
        {'ip': '192.17.43.23', 'mac': '58:20:b1:01:71:dc',
         'intf': 'hed1', 'speed': 1000},
        {'ip': '192.17.47.22', 'mac': '00:11:0a:6b:33:03',
         'intf': 'vlan1747', 'speed': 1000},
        {'ip': '192.17.49.11', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1749', 'speed': 40000},
        {'ip': '192.17.50.3', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1750', 'speed': 40000}
    ]

    CEPH_SHARED_NIC_WARN = [
        {'ip': '127.0.0.1', 'mac': '00:00:00:00:00:00',
         'intf': 'lo', 'speed': 'NA'},
        {'ip': '192.17.43.23', 'mac': '58:20:b1:01:71:dc',
         'intf': 'hed1', 'speed': 1000},
        {'ip': '192.17.47.22', 'mac': '00:11:0a:6b:33:03',
         'intf': 'vlan1747', 'speed': 1000},
        {'ip': '192.17.49.11', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1749', 'speed': 10000},
        {'ip': '192.17.50.3', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1750', 'speed': 10000}
    ]

    CEPH_SHARED_NIC_OK_VCP = [
        {'ip': '127.0.0.1', 'mac': '00:00:00:00:00:00',
         'intf': 'lo', 'speed': 'NA'},
        {'ip': '192.17.43.23', 'mac': '58:20:b1:01:71:dc',
         'intf': 'hed1', 'speed': 'NA'},
        {'ip': '192.17.47.22', 'mac': '00:11:0a:6b:33:03',
         'intf': 'vlan1747', 'speed': 'NA'},
        {'ip': '192.17.49.11', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1749', 'speed': 'NA'},
        {'ip': '192.17.50.3', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1750', 'speed': 'NA'}
    ]

    # In shared external network case the hierarchy of NICs are as follows:
    #
    # hed1 ---> Untagged Ardana network
    # hed3 -|         |-> vlan1749 (tagged Ceph public network)
    #       |- bond0 -|-> vlan1747 (tagged MGMT network)
    # hed4 -|         |-> vlan1750 (tagged Ceph private network)

    CEPH_SHARED_EXTERNAL_NET = [
        {'ip': '127.0.0.1', 'mac': '00:00:00:00:00:00',
         'intf': 'lo', 'speed': 'NA'},
        {'ip': '192.17.43.23', 'mac': '58:20:b1:01:71:dc',
         'intf': 'hed1', 'speed': 1000},
        {'ip': '192.17.47.22', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1747', 'speed': 40000},
        {'ip': '192.17.49.11', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1749', 'speed': 40000},
        {'ip': '192.17.50.3', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1750', 'speed': 40000}
    ]

    CEPH_SHARED_EXTERNAL_NET_VCP = [
        {'ip': '127.0.0.1', 'mac': '00:00:00:00:00:00',
         'intf': 'lo', 'speed': 'NA'},
        {'ip': '192.17.43.23', 'mac': '58:20:b1:01:71:dc',
         'intf': 'hed1', 'speed': 'NA'},
        {'ip': '192.17.47.22', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1747', 'speed': 'NA'},
        {'ip': '192.17.49.11', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1749', 'speed': 'NA'},
        {'ip': '192.17.50.3', 'mac': '00:11:0a:6b:55:05',
         'intf': 'vlan1750', 'speed': 'NA'}
    ]


class CephLmConfigData:
    BIND_IPS = {'private_ip': '192.17.50.3', 'public_ip': '192.17.49.11'}


class MonitorQuorumData:
    QUORUM_WARN = {"election_epoch": 298,
                   "quorum": [
                       0,
                       1
                   ],
                   "quorum_names": [
                       "mcloud-ccp1-c1-m1-osd-client",
                       "mcloud-ccp1-c1-m2-osd-client"
                   ],
                   "quorum_leader_name": "mcloud-ccp1-c1-m1-osd-client",
                   "monmap": {
                       "epoch": 1,
                       "fsid": "2645bbf6-16d0-4c42-8835-8ba9f5c95a1d",
                       "modified": "2016-06-22 06:52:02.384290",
                       "created": "2016-06-22 06:52:02.384290",
                       "mons": [
                           {
                               "rank": 0,
                               "name": "mcloud-ccp1-c1-m1-osd-client",
                               "addr": "192.168.12.3:6789/0"
                           },
                           {
                               "rank": 1,
                               "name": "mcloud-ccp1-c1-m2-osd-client",
                               "addr": "192.168.12.4:6789/0"
                           },
                           {
                               "rank": 2,
                               "name": "mcloud-ccp1-c1-m3-osd-client",
                               "addr": "192.168.12.5:6789/0"
                           }
                       ]
                   }
                   }
    QUORUM_OK = {"election_epoch": 300,
                 "quorum": [
                     0,
                     1,
                     2
                 ],
                 "quorum_names": [
                     "mcloud-ccp1-c1-m1-osd-client",
                     "mcloud-ccp1-c1-m2-osd-client",
                     "mcloud-ccp1-c1-m3-osd-client"
                 ],
                 "quorum_leader_name": "mcloud-ccp1-c1-m1-osd-client",
                 "monmap": {
                     "epoch": 1,
                     "fsid": "2645bbf6-16d0-4c42-8835-8ba9f5c95a1d",
                     "modified": "2016-06-22 06:52:02.384290",
                     "created": "2016-06-22 06:52:02.384290",
                     "mons": [
                         {
                             "rank": 0,
                             "name": "mcloud-ccp1-c1-m1-osd-client",
                             "addr": "192.168.12.3:6789/0"},
                         {
                             "rank": 1,
                             "name": "mcloud-ccp1-c1-m2-osd-client",
                             "addr": "192.168.12.4:6789/0"},
                         {
                             "rank": 2,
                             "name": "mcloud-ccp1-c1-m3-osd-client",
                             "addr": "192.168.12.5:6789/0"}]
                 }}
    Monitors = 'mcloud-ccp1-c1-m1-osd-client,mcloud-ccp1-c1-m2-osd-client,' \
               'mcloud-ccp1-c1-m3-osd-client'
