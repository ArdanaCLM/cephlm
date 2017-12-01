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

import os
import json
import ConfigParser

from cephlm.common.config import cfg
from cephlm.common import exceptions as exc
from cephlm.utils.system import run_cmd


class Ceph:
    COMMAND_TIMEOUT_SECS = int(cfg.get('global', 'ceph_command_timeout'))

    @staticmethod
    def _get_ceph_config():
        # Default cluster name
        ceph_config_dir = '/etc/ceph'
        # Get the cluster_name from <cluster_name>.conf in /etc/ceph/ directory
        if os.path.exists(ceph_config_dir):
            config_files = [f for f in os.listdir(ceph_config_dir)
                            if f.endswith('.conf')]
            if not config_files:
                return None
            config_file = os.path.join(ceph_config_dir, config_files[0])
            cluster_name = config_files[0][:-5]
            config = ConfigParser.RawConfigParser()
            config.read(config_file)
            return cluster_name, config, config_file
        else:
            msg = "Could not find ceph configuration directory /etc/ceph"
            raise exc.CephLMException(msg)

    @staticmethod
    def get_status():
        try:
            cluster_name, config, config_file = Ceph._get_ceph_config()
            output = run_cmd('ceph -s --connect-timeout %s -f json '
                             '--cluster %s' % (Ceph.COMMAND_TIMEOUT_SECS,
                                               cluster_name))
            return json.loads(output)
        except (exc.ShellCommandException, ValueError) as e:
            raise exc.CephCommandException(str(e))
        except exc.ShellCommandTimeoutException as e:
            raise exc.CephCommandTimeoutException(str(e))

    @staticmethod
    def get_osd_tree():
        try:
            cluster_name, config, config_file = Ceph._get_ceph_config()
            output = run_cmd('ceph osd tree --connect-timeout %s -f json '
                             '--cluster %s' % (Ceph.COMMAND_TIMEOUT_SECS,
                                               cluster_name))
            return json.loads(output)
        except (exc.ShellCommandException, ValueError) as e:
            raise exc.CephCommandException(str(e))
        except exc.ShellCommandTimeoutException as e:
            raise exc.CephCommandTimeoutException(str(e))

    @staticmethod
    def get_ceph_disk_list():
        try:
            output = run_cmd('ceph-disk list')
            return Ceph._process_ceph_disk_list(output)
        except (exc.ShellCommandException, ValueError) as e:
            raise exc.CephCommandException(str(e))

    @staticmethod
    def _process_ceph_disk_list(raw_output):
        journal_disk_map = dict()
        data_disk_map = dict()
        for line in raw_output.split('\n'):
            line = line.strip()
            if ":" in line and line.startswith('/dev/'):
                device = line.split(" :")[0]
                data_disk_map[device] = list()
                journal_disk_map[device] = list()
            elif "ceph journal" in line:
                journal_disk_map[device].append(line)
            elif "ceph data" in line:
                data_disk_map[device].append(line)

        journal_disks = {key: val for key, val in journal_disk_map.iteritems()
                         if journal_disk_map[key]}
        data_disks = {key: val for key, val in data_disk_map.iteritems()
                      if data_disk_map[key]}
        return journal_disks, data_disks

    @staticmethod
    def get_monitors():
        cluster_status = Ceph.get_status()
        return [mon['name'] for mon in cluster_status['monmap']['mons']]

    @staticmethod
    def get_ceph_df():
        try:
            cluster_name, config, config_file = Ceph._get_ceph_config()
            output = run_cmd('ceph df --connect-timeout %s -f json '
                             '--cluster %s' % (Ceph.COMMAND_TIMEOUT_SECS,
                                               cluster_name))
            return json.loads(output)
        except (exc.ShellCommandException, ValueError) as e:
            raise exc.CephCommandException(str(e))
        except exc.ShellCommandTimeoutException as e:
            raise exc.CephCommandTimeoutException(str(e))

    @staticmethod
    def get_quorum_status():
        try:
            cluster_name, config, config_file = Ceph._get_ceph_config()
            output = run_cmd('ceph quorum_status --connect-timeout %s -f json '
                             '--cluster %s' % (Ceph.COMMAND_TIMEOUT_SECS,
                                               cluster_name))
            return json.loads(output)
        except (exc.ShellCommandException, ValueError) as e:
            raise exc.CephCommandException(str(e))
        except exc.ShellCommandTimeoutException as e:
            raise exc.CephCommandTimeoutException(str(e))
