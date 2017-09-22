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

import os
import re
import requests
from cephlm.cephmetrics.common.ceph_common import Ceph

from cephlm.common.exceptions import \
    CephCommandException,\
    CephLMException

from cephlm.utils.system import run_cmd
from cephlm.utils.metricdata import MetricData
from cephlm.utils.values import Severity


class Radosgw(Ceph):
    RADOSGW_SITE_CONF = '/etc/apache2/sites-available/rgw.conf'
    HTTP_REQ_TIMEOUT = Ceph.COMMAND_TIMEOUT_SECS

    @staticmethod
    def _fetch_radosgw_ip_port():
        """
        Read the RADOSGW_SITE_CONF and fetch the IP and port of the apache site
        :return: string of ip:port on success, raises exception on failure.
        """
        if not (os.path.isfile(Radosgw.RADOSGW_SITE_CONF) or
                os.access(Radosgw.RADOSGW_SITE_CONF, os.R_OK)):
            raise CephLMException("Configuration file %s for Radosgw apache "
                                  "site not found or cannot be read" %
                                  Radosgw.RADOSGW_SITE_CONF)
        cmd = 'grep Listen %s' % Radosgw.RADOSGW_SITE_CONF
        err_msg = "Failed to run command '%s'" % cmd
        output = run_cmd(cmd)

        m = re.search('Listen (\S+)', output)
        if m:
            return m.groups()[0]
        else:
            raise CephCommandException(err_msg)

    @staticmethod
    def get_status(ip_port):
        """
        Query the apache site hosting radosgw and report the status.
        :return: True if HTTP response is 200, False for non 200 response and
                 upon connection failure or request timeout.
        """
        swift_api_url = "http://%s/swift/v1?format=json" % ip_port
        try:
            req = requests.get(swift_api_url, timeout=Radosgw.HTTP_REQ_TIMEOUT)
        except requests.exceptions.ConnectionError:
            return False
        return req.status_code == 200

    @staticmethod
    def check_status():
        """
        Reports the status of the rados gateway service
        """
        base_result = MetricData(
            name='cephlm.radosgw.status',
            messages={
                'ok': 'Radosgw ({ip_port}) is in healthy state.',
                'fail': 'Radosgw ({ip_port}) is in error state.',
                'unknown': 'Probe error: {msg}.'
            }
        )

        try:
            ip_port = Radosgw._fetch_radosgw_ip_port()
            status_success = Radosgw.get_status(ip_port)
        except (CephLMException, CephCommandException) as e:
            result = base_result.child(msgkeys={'msg': str(e)})
            result.value = Severity.unknown
            return result

        result = base_result.child(msgkeys={'ip_port': ip_port})
        result.value = Severity.ok if status_success else Severity.fail
        return result
