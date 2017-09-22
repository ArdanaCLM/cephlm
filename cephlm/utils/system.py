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

import re
import string
import netifaces
import subprocess
import ConfigParser

from cephlm.common.config import cfg

from cephlm.utils.utility import str_to_num
from cephlm.common.exceptions import ShellCommandException
from cephlm.common.exceptions import ShellCommandTimeoutException


def get_system_disks_size():
    """
    :return: A dict with disk and disk-size in bytes
    E.g.,
        {
            '/dev/sda': 3.299e+12,
            '/dev/sdb': 3.299e+12,
            '/dev/sdc': 1.074e+10
        }
    """
    output = run_cmd('fdisk -l')
    pattern = re.compile("Disk (.*): (.*), (.*) bytes")
    disk_dict = dict()
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('Disk /dev/'):
            match = pattern.match(line)
            disk_dict[match.group(1)] = int(match.group(3))
    return disk_dict


def get_system_memory_info():
    """
    :return: Dict with key and integer value pairs, after stripping off the
             standard 'kB' unit string
    E.g.,
        {
            'MemTotal': 263848920,
            'MemFree': 658064
            ...
        }
    """
    output = run_cmd('cat /proc/meminfo')
    meminfo = dict()
    for line in output.split('\n'):
        line = line.strip()
        if line and ':' in line:
            key, val = line.split(':', 1)
            meminfo[key] = int(val.strip().replace(' kB', ''))
    return meminfo


def get_ceph_bind_ips():
    """
    Get unique bind ips from cephlm.conf.
    :returns: dict of bind_ips
    E.g.,
        {
            'private_ip': '192.17.50.3',
            'public_ip': '192.17.49.11'
        }
    """
    bind_ips = dict()
    option_name_list = ["public_ip", "private_ip"]
    for option_name in option_name_list:
        try:
            ip = cfg.get("network-interface", option_name)
            bind_ips.update({option_name: ip})
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            pass
    return bind_ips


def get_interface_speed(interface_name):
    """
    Get the NIC speed of the specified interface
    :param interface_name: interface logical name E.g., eth1
    :return: NIC Speed in Mb/s
    """
    interface_data = run_cmd("ethtool " + interface_name)
    speed = ''

    # Filter lines here. We only want the speed.
    lines = interface_data.split('\n')
    for line in lines:
        if 'Speed' in line:
            _, speed = line.split(':')

    # Only leave the digits
    speed = ''.join(c for c in speed if c in string.digits)
    speed = str_to_num(speed) if speed else 'NA'
    return speed


def get_nic_info():
    """
    Fetches physical NIC information and returns only the logical NICs which
    have IP Address assigned to them
    :return: NIC info dict
    E.g.,
        [
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
    """
    nic_info = list()
    for intf in netifaces.interfaces():
        addrs = netifaces.ifaddresses(intf)
        if netifaces.AF_INET in addrs and netifaces.AF_PACKET in addrs:
            nic_info.append({'intf': intf,
                             'mac': addrs[netifaces.AF_PACKET][0]['addr'],
                             'ip': addrs[netifaces.AF_INET][0]['addr'],
                             'speed': get_interface_speed(intf)})
    return nic_info


def run_cmd(command):
    """
    Wrapper for subprocess popen with basic try & catch blocks
    :param command: command to be run
    :return: Command output
    """
    try:
        process = subprocess.Popen(
            command.split(' '),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        if process.returncode:
            if 'InterruptedOrTimeoutError' in str(error) or 'TimedOut' in str(error):    # noqa
                msg = 'Command execution timed out'
                raise ShellCommandTimeoutException(msg)
            else:
                msg = "Failed to run command '%s'" % command
                raise ShellCommandException(msg)
        return output
    except (OSError, IOError) as e:
        msg = "Failed to run command '%s'" % command
        raise ShellCommandException(msg)
