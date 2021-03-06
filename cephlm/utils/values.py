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


import enum


class Severity(enum.IntEnum):
    # We need to use an IntEnum to dump to JSON/YAML
    ok = 0
    warn = 1
    fail = 2
    unknown = 3

    def __str__(self):
        return str(int(self))

    @staticmethod
    def yaml_repr(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', str(data))
