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

import mock
import requests
import unittest

from cephlm.common.exceptions import \
    CephCommandException,\
    CephLMException,\
    ShellCommandException

from cephlm.cephmetrics.ceph.radosgw import Radosgw
from cephlm.utils.values import Severity


class TestRadosgw(unittest.TestCase):
    def setUp(self):
        self.rgw_host_port = "standard-ceph-ccp-rgw-m1-mgmt:8079"

    @mock.patch('os.path.isfile')
    @mock.patch('os.access')
    @mock.patch('cephlm.cephmetrics.ceph.radosgw.run_cmd')
    def test_fetch_radosgw_ip_port_ok(self, mock_run, mock_access,
                                      mock_isfile):
        mock_run.return_value = "Listen %s" % self.rgw_host_port
        mock_access.return_value = True
        mock_isfile.return_value = True
        result = Radosgw._fetch_radosgw_ip_port()
        self.assertEqual(self.rgw_host_port, result)

    @mock.patch('cephlm.cephmetrics.ceph.radosgw.run_cmd')
    @mock.patch('os.path.isfile')
    def test_fetch_radosgw_ip_port_no_conf(self, mock_isfile, mock_run):
        mock_isfile.return_value = False
        mock_run.return_value = "Listen %s" % self.rgw_host_port
        msg = ("Configuration file /etc/apache2/sites-available/rgw.conf for "
               "Radosgw apache site not found or cannot be read")
        self.assertRaisesRegexp(CephLMException, msg,
                                lambda: Radosgw._fetch_radosgw_ip_port())

    @mock.patch('cephlm.cephmetrics.ceph.radosgw.run_cmd')
    @mock.patch('os.path.isfile')
    @mock.patch('os.access')
    def test_fetch_radosgw_ip_port_exc(self, mock_access, mock_isfile,
                                       mock_run):
        mock_access.return_value = True
        mock_isfile.return_value = True
        regexp = ("Failed to run command 'grep Listen "
                  "/etc/apache2/sites-available/rgw.conf'")
        mock_run.side_effect = ShellCommandException(regexp)
        self.assertRaisesRegexp(CephCommandException, regexp,
                                lambda: Radosgw._fetch_radosgw_ip_port())

    @mock.patch('cephlm.cephmetrics.ceph.radosgw.run_cmd')
    @mock.patch('os.path.isfile')
    @mock.patch('os.access')
    def test_fetch_radosgw_ip_port_error(self, mock_access, mock_isfile,
                                         mock_run):
        mock_access.return_value = True
        mock_isfile.return_value = True
        mock_run.return_value = "junk data"
        regexp = ("Failed to run command 'grep Listen "
                  "/etc/apache2/sites-available/rgw.conf'")
        self.assertRaisesRegexp(CephCommandException, regexp,
                                lambda: Radosgw._fetch_radosgw_ip_port())

    @mock.patch(
        'cephlm.cephmetrics.ceph.radosgw.Radosgw._fetch_radosgw_ip_port')
    def test_get_status_ok(self, mock_fetch):
        mock_fetch.return_value = "standard-ceph-ccp-rgw-m1-mgmt:8079"
        with mock.patch('requests.get') as mocked:
            mocked.return_value = mock.MagicMock(
                spec=requests.get,
                status_code=200)
            result = Radosgw.get_status(mock_fetch.return_value)
            self.assertTrue(result)

    @mock.patch(
        'cephlm.cephmetrics.ceph.radosgw.Radosgw._fetch_radosgw_ip_port')
    def test_get_status_error(self, mock_fetch):
        mock_fetch.return_value = "standard-ceph-ccp-rgw-m1-mgmt:8079"
        with mock.patch('requests.get') as mocked:
            mocked.return_value = mock.MagicMock(
                spec=requests.get,
                status_code=500)
            result = Radosgw.get_status(mock_fetch.return_value)
            self.assertFalse(result)

    @mock.patch(
        'cephlm.cephmetrics.ceph.radosgw.Radosgw._fetch_radosgw_ip_port')
    def test_get_status_error_get_failure(self, mock_fetch):
        mock_fetch.return_value = "standard-ceph-ccp-rgw-m1-mgmt:8079"
        with mock.patch('requests.get') as mocked:
            mocked.side_effect = requests.exceptions.ConnectionError(
                "No response")
            result = Radosgw.get_status(mock_fetch.return_value)
            self.assertFalse(result)

    @mock.patch('cephlm.cephmetrics.ceph.radosgw.Radosgw.get_status')
    @mock.patch(
        'cephlm.cephmetrics.ceph.radosgw.Radosgw._fetch_radosgw_ip_port')
    def test_check_status_ok(self, mock_fetch, mock_status):
        mock_fetch.return_value = "standard-ceph-ccp-rgw-m1-mgmt:8079"
        mock_status.return_value = True
        result = Radosgw.check_status()
        self.assertEqual(str(result),
                         'Radosgw (%s) is in healthy state.' %
                         mock_fetch.return_value)
        self.assertEqual(result.value, Severity.ok)

    @mock.patch(
        'cephlm.cephmetrics.ceph.radosgw.Radosgw._fetch_radosgw_ip_port')
    def test_check_status_unknown_fetch_err(self, mock_fetch):
        err_msg = ("Failed to run command 'grep Listen "
                   "/etc/apache2/sites-available/rgw.conf")
        mock_fetch.side_effect = CephCommandException(err_msg)
        result = Radosgw.check_status()
        self.assertEqual(str(result), 'Probe error: %s.' % err_msg)
        self.assertEqual(result.value, Severity.unknown)

    @mock.patch(
        'cephlm.cephmetrics.ceph.radosgw.Radosgw.get_status')
    @mock.patch(
        'cephlm.cephmetrics.ceph.radosgw.Radosgw._fetch_radosgw_ip_port')
    def test_check_status_unknown_get_status_err(self, mock_fetch, mock_get):
        mock_fetch.return_value = "standard-ceph-ccp-rgw-m1-mgmt:8079"
        err_msg = ("Failed to run command 'grep Listen "
                   "/etc/apache2/sites-available/rgw.conf")
        mock_get.side_effect = CephLMException(err_msg)
        result = Radosgw.check_status()
        self.assertEqual(str(result), 'Probe error: %s.' % err_msg)
        self.assertEqual(result.value, Severity.unknown)

    @mock.patch(
        'cephlm.cephmetrics.ceph.radosgw.Radosgw.get_status')
    @mock.patch(
        'cephlm.cephmetrics.ceph.radosgw.Radosgw._fetch_radosgw_ip_port')
    def test_check_status_fail(self, mock_fetch, mock_get):
        mock_fetch.return_value = "standard-ceph-ccp-rgw-m1-mgmt:8079"
        mock_get.return_value = False
        result = Radosgw.check_status()
        self.assertEqual(str(result),
                         'Radosgw (%s) is in error state.' %
                         mock_fetch.return_value)
        self.assertEqual(result.value, Severity.fail)
