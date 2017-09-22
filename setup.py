#!/usr/bin/python
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
#


from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__name__))


def requirements():
    with open(here + '/requirements.txt', 'r') as f:
        return [y.strip() for y in f.readlines() if y.strip()]


setup(
    name='cephlm',
    version='1.0.0',
    description='Lifecycle management for Ceph cluster',
    author='Hewlett Packard Enterprise Development Company, L.P',
    license='Apache 2.0',
    classifers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache 2.0',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='Ceph',
    packages=find_packages(exclude=['docs', 'etc', 'tests']),
    install_requires=requirements(),
    entry_points={
        'console_scripts': [
            'cephlm-probe = cephlm.cli.runner:main',
        ],
        'cephlm.plugins': [
            'cluster-status = '
            'cephlm.cephmetrics.ceph.cluster:Cluster.check_status',
            'connectivity-status = '
            'cephlm.cephmetrics.ceph.cluster:Cluster.'
            'check_monitor_connectivity',
            'osd-stats = '
            'cephlm.cephmetrics.ceph.osd:OSD.osd_stats',
            'osd-journal-ratio = '
            'cephlm.cephmetrics.ceph.osd:OSD.check_osd_journal_ratio',
            'osd-node-ram = '
            'cephlm.cephmetrics.ceph.perfscale:PerfScale.check_osd_node_ram',
            'nic-speed = '
            'cephlm.cephmetrics.ceph.perfscale:PerfScale.check_nic_speed',
            'radosgw-status = '
            'cephlm.cephmetrics.ceph.radosgw:Radosgw.check_status',
            'pool-stats = '
            'cephlm.cephmetrics.usage.pool:Pool.pool_stats',
            'capacity-stats = '
            'cephlm.cephmetrics.usage.capacity:Capacity.capacity_stats',
            'hpssacli = '
            'cephlm.cephmetrics.system.hpssacli:HPssaCli.check_hpssacli',
            'pg-stats = '
            'cephlm.cephmetrics.ceph.pg:PG.pg_stats',
            'quorum-status = '
            'cephlm.cephmetrics.ceph.monitor_quorum:Monitor.quorum_status'
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
