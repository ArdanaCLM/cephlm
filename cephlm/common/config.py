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

import ConfigParser

CEPHLM_CONF = '/etc/cephlm/cephlm.conf'


def set_default_values(cfg):
    # Function to define configuration sections,parameters,default values etc.
    cfg.add_section('perfscale')
    cfg.add_section('pools')
    cfg.add_section('global')
    cfg.add_section('osd')

    # Configuration default for including private pools in metrics
    # Accepted values are 'true' and 'false'
    cfg.set('pools', 'include_private_pools', 'false')

    # Configuration default for ceph commands timeout value
    cfg.set('global', 'ceph_command_timeout', '60')

    # Recommended Public NIC Speed in Mb/s
    cfg.set('perfscale', 'public_nic_speed', '10000')

    # Recommended Private NIC speed = n * public_nic_speed
    # Where 'n' is the multiplier calculated predominantly based on the replica
    # count. By default the assumption is replica count of 3
    cfg.set('perfscale', 'private_nic_speed_multiplier', '3')

    # RAM in GiB per TiB of data disk
    cfg.set('perfscale', 'ram_gib_per_tib', '1')
    cfg.set('perfscale', 'min_ram_gib', '1')

    # Maximum number of OSDs per journal disk
    cfg.set('osd', 'optimal_osd_per_journal', '4')


cfg = ConfigParser.RawConfigParser()
set_default_values(cfg)
cfg.read(CEPHLM_CONF)
