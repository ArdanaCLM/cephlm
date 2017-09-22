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


class SystemData:
    MEM_INFO_STDOUT = """MemTotal:        7917952 kB
    MemFree:         6142136 kB
    MemAvailable:    7136684 kB
    Buffers:          170592 kB
    Cached:          1000540 kB
    SwapCached:            0 kB
    Active:          1026308 kB
    Inactive:         546324 kB
    Active(anon):     419352 kB
    Inactive(anon):    45140 kB
    Active(file):     606956 kB
    Inactive(file):   501184 kB
    Unevictable:        6768 kB
    Mlocked:            6768 kB
    SwapTotal:             0 kB
    SwapFree:              0 kB
    Dirty:                24 kB
    Writeback:             0 kB
    AnonPages:        408264 kB
    Mapped:            43392 kB
    Shmem:             58000 kB
    Slab:             137060 kB
    SReclaimable:     110704 kB
    SUnreclaim:        26356 kB
    KernelStack:        8800 kB
    PageTables:         5044 kB
    NFS_Unstable:          0 kB
    Bounce:                0 kB
    WritebackTmp:          0 kB
    CommitLimit:     3958976 kB
    Committed_AS:    2010244 kB
    VmallocTotal:   34359738367 kB
    VmallocUsed:           0 kB
    VmallocChunk:          0 kB
    HardwareCorrupted:     0 kB
    AnonHugePages:         0 kB
    CmaTotal:              0 kB
    CmaFree:               0 kB
    HugePages_Total:       0
    HugePages_Free:        0
    HugePages_Rsvd:        0
    HugePages_Surp:        0
    Hugepagesize:       2048 kB
    DirectMap4k:       53184 kB
    DirectMap2M:     3092480 kB
    DirectMap1G:     7340032 kB
    """

    DISKS_STDOUT = """Disk /dev/ram0: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram1: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram2: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram3: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram4: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram5: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram6: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram7: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram8: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram9: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram10: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram11: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram12: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram13: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram14: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/ram15: 4 MiB, 4194304 bytes, 8192 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk /dev/sdb: 20 GiB, 21474836480 bytes, 41943040 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: gpt
    Disk identifier: BE45FC52-9EBF-45D8-82F4-33C4B72F4BB8

    Device        Start      End  Sectors Size Type
    /dev/sdb1      2048 10487807 10485760   5G unknown
    /dev/sdb2  10487808 20973567 10485760   5G unknown
    /dev/sdb3  20973568 31459327 10485760   5G unknown

    Disk /dev/sda: 40 GiB, 42949672960 bytes, 83886080 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x74923703

    Device     Boot   Start      End  Sectors  Size Id Type
    /dev/sda1          2048   999423   997376  487M 83 Linux
    /dev/sda2  *     999424  1998847   999424  488M 83 Linux
    /dev/sda3       2000894 83884031 81883138   39G  5 Extended
    /dev/sda5       2000896  2002943     2048    1M 83 Linux
    /dev/sda6       2004992 83884031 81879040   39G 8e Linux LVM

    Disk /dev/sdc: 10 GiB, 10737418240 bytes, 20971520 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: gpt
    Disk identifier: 71AB3D59-A01B-458B-B807-4014BC563B03

    Device     Start      End  Sectors Size Type
    /dev/sdc1   2048 20971486 20969439  10G unknown

    Disk /dev/sdd: 10 GiB, 10737418240 bytes, 20971520 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: gpt
    Disk identifier: 9C6EA4AB-9FC0-4044-AF75-FBE7DEBFC23D

    Device     Start      End  Sectors Size Type
    /dev/sdd1   2048 20971486 20969439  10G unknown

    Disk /dev/sde: 10 GiB, 10737418240 bytes, 20971520 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: gpt
    Disk identifier: 67574241-D1F1-4E71-8C83-7FC85411BBAB

    Device     Start      End  Sectors Size Type
    /dev/sde1   2048 20971486 20969439  10G unknown

    Disk /dev/mapper/ardana-vg-root: 35.1 GiB, 37727764480 bytes, 73687040 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    """

    IP_DATA = """
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
     default qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state
     UP group default qlen 1000
        link/ether 00:50:56:80:6b:0f brd ff:ff:ff:ff:ff:ff
        inet 192.168.40.11/24 brd 192.168.40.255 scope global eth0
           valid_lft forever preferred_lft forever
        inet6 fe80::250:56ff:fe80:6b0f/64 scope link
           valid_lft forever preferred_lft forever
    3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state
     UP group default qlen 1000
        link/ether 00:50:56:80:48:1a brd ff:ff:ff:ff:ff:ff
        inet 192.168.50.11/24 brd 192.168.50.255 scope global eth1
           valid_lft forever preferred_lft forever
        inet6 fe80::250:56ff:fe80:481a/64 scope link
           valid_lft forever preferred_lft forever
    4: eth2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state
     UP group default qlen 1000
        link/ether 00:50:56:80:cd:71 brd ff:ff:ff:ff:ff:ff
        inet 192.168.12.7/24 brd 192.168.12.255 scope global eth2
           valid_lft forever preferred_lft forever
        inet6 fe80::250:56ff:fe80:cd71/64 scope link
           valid_lft forever preferred_lft forever
       """

    IP_IFACE_MAP = {
        '192.168.12.7': 'eth2',
        '192.168.50.11': 'eth1',
        '127.0.0.1': 'lo',
        '192.168.40.11': 'eth0'
    }

    IFACE_DATA = """Settings for eth0:
    Supported ports: [ TP ]
    Supported link modes:   10baseT/Half 10baseT/Full
                            100baseT/Half 100baseT/Full
                            1000baseT/Full
    Supported pause frame use: No
    Supports auto-negotiation: Yes
    Advertised link modes:  10baseT/Half 10baseT/Full
                            100baseT/Half 100baseT/Full
                            1000baseT/Full
    Advertised pause frame use: No
    Advertised auto-negotiation: Yes
    Speed: 1000Mb/s
    Duplex: Full
    Port: Twisted Pair
    PHYAD: 0
    Transceiver: internal
    Auto-negotiation: on
    MDI-X: off (auto)
    Supports Wake-on: d
    Wake-on: d
    Current message level: 0x00000007 (7)
                           drv probe link
    Link detected: yes
    """

    # netifaces.interfaces() response
    NET_IFACES = ['lo', 'hed1', 'hed2', 'hed3', 'hed4', 'bond0',
                  'vlan1747', 'vlan1749', 'vlan1750']
    # netifaces.ifaddresses(intf) result for eachi of the above intf (in order)
    IF_ADDRESS = [
        {
            17: [{'peer': '00:00:00:00:00:00',
                  'addr': '00:00:00:00:00:00'}],
            2: [{'peer': '127.0.0.1', 'netmask': '255.0.0.0',
                 'addr': '127.0.0.1'}]
        },
        {
            17: [{'broadcast': 'ff:ff:ff:ff:ff:ff',
                  'addr': '58:20:b1:01:71:dc'}],
            2: [{'broadcast': '192.17.43.255', 'netmask': '255.255.255.0',
                 'addr': '192.17.43.23'}]
        },
        {
            17: [{'broadcast': 'ff:ff:ff:ff:ff:ff',
                  'addr': '58:20:b1:01:71:dd'}]
        },
        {
            17: [{'broadcast': 'ff:ff:ff:ff:ff:ff',
                  'addr': '00:11:0a:6b:55:00'}]
        },
        {
            17: [{'broadcast': 'ff:ff:ff:ff:ff:ff',
                  'addr': '00:11:0a:6b:55:00'}]
        },
        {
            17: [{'broadcast': 'ff:ff:ff:ff:ff:ff',
                  'addr': '00:11:0a:6b:55:00'}]
        },
        {
            17: [{'broadcast': 'ff:ff:ff:ff:ff:ff',
                  'addr': '00:11:0a:6b:55:00'}],
            2: [{'broadcast': '192.17.47.255', 'netmask': '255.255.255.0',
                 'addr': '192.17.47.22'}]
        },
        {
            17: [{'broadcast': 'ff:ff:ff:ff:ff:ff',
                  'addr': '00:11:0a:6b:55:00'}],
            2: [{'broadcast': '192.17.49.255', 'netmask': '255.255.255.0',
                 'addr': '192.17.49.11'}]
        },
        {
            17: [{'broadcast': 'ff:ff:ff:ff:ff:ff',
                  'addr': '00:11:0a:6b:55:00'}],
            2: [{'broadcast': '192.17.50.255', 'netmask': '255.255.255.0',
                 'addr': '192.17.50.3'}]}
    ]

    NIC_INFO = [
        {'ip': '127.0.0.1', 'mac': '00:00:00:00:00:00',
         'intf': 'lo', 'speed': 1000},
        {'ip': '192.17.43.23', 'mac': '58:20:b1:01:71:dc',
         'intf': 'hed1', 'speed': 1000},
        {'ip': '192.17.47.22', 'mac': '00:11:0a:6b:55:00',
         'intf': 'vlan1747', 'speed': 1000},
        {'ip': '192.17.49.11', 'mac': '00:11:0a:6b:55:00',
         'intf': 'vlan1749', 'speed': 1000},
        {'ip': '192.17.50.3', 'mac': '00:11:0a:6b:55:00',
         'intf': 'vlan1750', 'speed': 1000}
    ]


class CephLmConfigData:
    BIND_IPS = {'private_ip': '192.168.50.11', 'public_ip': '192.168.40.11'}
