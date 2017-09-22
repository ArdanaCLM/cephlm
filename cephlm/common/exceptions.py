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

import sys


class CephLMException(Exception):
    """ To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """

    message = "Unknown cephlm error occured."

    def __init__(self, message=None, **kwargs):
        if not message:
            message = self.message
        try:
            message = message % kwargs
        except Exception as e:
            exc_info = sys.exc_info()
            raise exc_info[0], exc_info[1], exc_info[2]

        # at least get the core message out if something happened
        self.message = message
        super(CephLMException, self).__init__(message)


class CephCommandException(CephLMException):
    message = "%(msg)s"


class CephCommandTimeoutException(CephLMException):
    message = "%(msg)s"


class ShellCommandException(CephCommandException):
    message = "%(msg)s"


class ShellCommandTimeoutException(CephCommandTimeoutException):
    message = "%(msg)s"
