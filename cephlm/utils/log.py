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

import logging
import syslog

LOG_LEVEL_MAP = {'debug': logging.DEBUG,
                 'info': logging.INFO,
                 'warning': logging.WARNING,
                 'error': logging.ERROR,
                 'critical': logging.CRITICAL}

SYSLOG_LEVEL_MAP = {'debug': syslog.LOG_DEBUG,
                    'info': syslog.LOG_INFO,
                    'warning': syslog.LOG_WARNING,
                    'error': syslog.LOG_ERR,
                    'critical': syslog.LOG_CRIT}

LOG_FACILITY_MAP = {"LOG_LOCAL0": syslog.LOG_LOCAL0,
                    "LOG_LOCAL1": syslog.LOG_LOCAL1,
                    "LOG_LOCAL2": syslog.LOG_LOCAL2,
                    "LOG_LOCAL3": syslog.LOG_LOCAL3,
                    "LOG_LOCAL4": syslog.LOG_LOCAL4,
                    "LOG_LOCAL5": syslog.LOG_LOCAL5,
                    "LOG_LOCAL6": syslog.LOG_LOCAL6,
                    "LOG_LOCAL7": syslog.LOG_LOCAL7}


class CephlmSysLogHandler(logging.Handler):
    """A logging handler that emits messages to syslog.syslog."""
    def __init__(self, log_facility, log_level_str):
        try:
            syslog.openlog(logoption=syslog.LOG_PID, facility=log_facility)
        except IOError:
            try:
                syslog.openlog(syslog.LOG_PID, log_facility)
            except IOError:
                try:
                    syslog.openlog('cephlm', syslog.LOG_PID,
                                   log_facility)
                except:
                    raise
        syslog.setlogmask(syslog.LOG_UPTO(SYSLOG_LEVEL_MAP[log_level_str]))
        logging.Handler.__init__(self)

    def emit(self, record):
        syslog.syslog(self.format(record))


def get_logger(conf, name=None):
    if not conf:
        conf = {}
    if not name:
        name = "cephlm"

    # Some variables we need
    log_level_str = conf.get('log_level', 'info').lower()
    log_level = LOG_LEVEL_MAP[log_level_str]
    log_format = conf.get('log_format', '%(levelname)s : %(message)s')
    log_facility = LOG_FACILITY_MAP[conf.get('log_facility', 'LOG_LOCAL0')]
    # Configuring the logger
    logger = logging.getLogger(name=name)
    logger.setLevel(log_level)

    # Clearing previous logs
    logger.handlers = []

    # Setting formatters and adding handlers.
    formatter = logging.Formatter(log_format)
    handlers = [CephlmSysLogHandler(log_facility, log_level_str)]
    for h in handlers:
        h.setFormatter(formatter)
        logger.addHandler(h)
    return logger
