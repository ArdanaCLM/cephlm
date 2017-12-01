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

# In case you are tempted to import from non-built-in libraries, think twice:
# this module will be imported by monasca-agent which must therefore be able
# to import any dependent modules.
from collections import defaultdict
import json

try:
    from monasca_agent.collector.checks import AgentCheck as AgentCheck
except IOError:
    # Unit tests do no have an /etc/monasca/agent/agent.yaml file
    class AgentCheck(object):
        def __init__(self, name, init_config, agent_config, instances):
            self.log = None

import socket
import subprocess
import threading

# This module provides a check plugin class for monasca-agent. The plugin
# runs 'tasks' each of which generates one or more metrics that are reported to
# the monasca-agent daemon. There are three types of tasks:
#
# 1. Load metrics from files: file names may be specified via an ansible
# playbook task that deploys the associated cephlm_detect detect plugin. Files
# should contain json encoded lists of metric dicts.
#
# 2. Run a cephlm-probe command line.
#
# 3. Run a python function found from a list of entry points.
#
# If any task times out or raises an exception then the check plugin itself
# will report a metric to that effect.
import fcntl
import errno
import time
import os
import glob


OK = 0
WARN = 1
FAIL = 2
UNKNOWN = 3

# name used for metrics reported directly by this module e.g. when a task
# fails or times out. (we need to hard code this name rather than use the
# module name because the module name reported by __name__ is dependant on how
# monasca-agent imports the module)
MODULE_METRIC_NAME = 'cephlm.cephlm_check'

# Directory to which Monasca Agent can write
POSTED_DIR = '/tmp'

# Assumes metrics file written every 120 seconds
METRIC_STALE_AGE = 120 * 3                # These are too old to report
POSTED_STALE_AGE = METRIC_STALE_AGE * 2   # Keep in posted file until this old


def _take_shared_lock(fd):
    # attempt to take a shared lock on fd, raising IOError if
    # lock cannot be taken after a number of attempts
    max_attempts = 5
    delay = 0.02
    attempts = 0
    while True:
        attempts += 1
        try:
            fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            break
        except IOError as err:
            if (err.errno != errno.EWOULDBLOCK or
                    attempts > max_attempts):
                raise
            time.sleep(delay * attempts)


class CommandRunner(object):
    def __init__(self, command):
        self.command = command
        self.stderr = self.stdout = self.returncode = self.exception = None
        self.timed_out = False
        self.process = None

    def run_with_timeout(self, timeout):
        thread = threading.Thread(target=self._run_subprocess)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.timed_out = True
            if self.process:
                self.process.terminate()

    def _run_subprocess(self):
        try:
            self.process = subprocess.Popen(
                self.command, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            self.stdout, self.stderr = self.process.communicate()
            self.returncode = self.process.returncode
        except Exception as e:  # noqa
            self.exception = e


class CephLMScan(AgentCheck):
    # set of check tasks implemented by cephlm
    TASKS = (
    )
    # we explicitly list the entry points to be called rather than just use
    # whatever is found via pkg_resources.get_entry_map() because (a) we'd like
    # to know if an entry point is missing and (b) we may have experimental
    # cephlm entry points installed that should not just automatically run
    # in this plugin.
    TASK_ENTRY_POINTS = []
    # uncomment if entry points are to be used...
    # TASK_ENTRY_POINTS = TASKS

    # command args to be used for all calls to shell commands
    COMMAND_ARGS = ['sudo', 'cephlm-probe', '--format', 'json']
    COMMAND_TIMEOUT = 15.0
    SUBCOMMAND_PREFIX = '--'

    # list of sub-commands each of which is appended to a shell command
    # with the prefix added
    DEFAULT_SUBCOMMANDS = TASKS

    # list of tasks for which any 'ok' metrics will NOT be reported
    DEFAULT_SUPPRESS_OK = []

    def __init__(self, name, init_config, agent_config, instances=None,
                 logger=None):
        super(CephLMScan, self).__init__(
            name, init_config, agent_config, instances)
        self.log = logger or self.log
        self.plugin_failures = []

    def _plugin_failed(self, msg):
        self.log.warn(msg)
        self.plugin_failures.append(msg)

    def _plugin_check_metric(self):
        """
        Generate metric to report that a task has raised an exception.
        """
        if self.plugin_failures:
            msg = ', '.join(self.plugin_failures)
            if len(msg) > 2047:
                msg = msg[:-3] + '...'
            return dict(
                metric=MODULE_METRIC_NAME,
                dimensions={'service': 'ceph-storage',
                            'hostname': socket.gethostname()},
                value_meta=dict(msg=msg),
                value=FAIL)
        else:
            msg = 'Ok'
            return dict(
                metric=MODULE_METRIC_NAME,
                dimensions={'service': 'ceph-storage',
                            'hostname': socket.gethostname()},
                value_meta=dict(msg=msg),
                value=OK)

    def log_summary(self, task_type, summary):
        task_count = len(summary.get('tasks', []))
        if task_count == 1:
            msg = 'Ran 1 %s task.' % task_type
        else:
            msg = 'Ran %d %s tasks.' % (task_count, task_type)
        # suppress log noise if no tasks were configured
        logger = self.log.info if task_count else self.log.debug
        if summary:
            msg += ' Metrics summary: {'
            m = {'total': 'Total', OK: 'Ok', WARN: 'Warn', FAIL: 'Fail',
                 UNKNOWN: 'Unknown'}
            for key in ('total', OK, WARN, FAIL, UNKNOWN):
                msg += '%s: %d, ' % (m[key], len(summary.get(key, [])))
            msg += '}'
        logger(msg)

    def _run_command_line_task(self, task_name):
        # why is this here? If cephlm entry points are not available to
        # monasca-agent then we have to call out to a command line that
        # can find the entry points.
        command = list(self.COMMAND_ARGS)
        command.append(self.SUBCOMMAND_PREFIX + task_name)
        cmd_str = ' '.join(command)
        runner = CommandRunner(command)
        metrics = []
        msg = ''
        try:
            runner.run_with_timeout(self.COMMAND_TIMEOUT)
        except Exception as e:  # noqa
            msg = 'Command "%s" failed with "%s"' % (cmd_str, e)
            self._plugin_failed(msg)
        else:
            if runner.exception:
                msg = 'Command "%s" failed with "%s"' \
                      % (cmd_str, runner.exception)
            elif runner.timed_out:
                msg = 'Command "%s" timed out after %ss' \
                      % (cmd_str, self.COMMAND_TIMEOUT)
            elif runner.returncode:
                msg = 'Command "%s" failed with status %s' \
                      % (cmd_str, runner.returncode)
            else:
                try:
                    metrics = json.loads(runner.stdout)
                except (ValueError, TypeError) as e:
                    msg = 'Failed to parse json: %s' % e
            self._plugin_failed(msg)
        return metrics

    def _run_load_file_task(self, file_path):
        metrics = []
        try:
            with open(file_path, 'r') as f:
                _take_shared_lock(f.fileno())
                f.seek(0)
                metrics = json.load(f)
        except (ValueError, TypeError) as e:
            msg = 'Loading file "%s" failed parsing json: %s' % (file_path, e)
            self._plugin_failed(msg)
        except Exception as e:  # noqa
            msg = 'Loading file "%s" failed with "%s"' % (file_path, e)
            self._plugin_failed(msg)
        return self._remove_duplicate_metrics(metrics, file_path)

    def _remove_duplicate_metrics(self, metrics, file_path):
        """
        Remove metrics if we've already reported them

        We track the metrics we return to the Monasca Agent in a
        "posted" file. This allows us to discard duplicate metrics.
        We also discard metrics that seem stale. This can occur when the
        program creating the metrics file has died, so the metrics file
        does not update with new metrics.

        The posted file contains recently posted metrics. The file is
        read, then re-writen on each cycle. Metrics older than
        POSTED_STALE_AGE are removed from the posted file (so it does not
        grow forever).

        :param metrics: The metrics we found in the metrics file
        :param file_path: the path of the metrics file -- this is used to
                          derive an appropriate name for the posted file
        :returns: A list of metrics that should be posted
        """
        stale_metrics = False
        posted_metrics = []
        file_name = os.path.split(file_path)[1]
        pfile_path = os.path.join(POSTED_DIR, file_name) + '.posted'
        try:
            with open(pfile_path, 'r') as p:
                posted_metrics = json.load(p)
        except Exception as e:  # noqa
            # This is normal when program first runs (no file exists)
            self.log.warn('Loading file "%s" failed: %s' % (pfile_path, e))

        # Purge already posted and stale metrics
        for metric in list(metrics):
            if (time.time() - metric.get('timestamp')) > METRIC_STALE_AGE:
                metrics.remove(metric)
                stale_metrics = True
            else:
                posted_metrics.append(metric)

        # Purge really old metrics from posted file
        for metric in list(posted_metrics):
            if (time.time() - metric.get('timestamp')) > POSTED_STALE_AGE:
                posted_metrics.remove(metric)
        try:
            with open(pfile_path, 'w') as p:
                json.dump(posted_metrics, p)
        except Exception as e:  # noqa
            self.log.warn('Dumping file "%s" failed: %s'
                          % (pfile_path, e))

        if stale_metrics:
            msg = 'Stale metrics, older than %s seconds, found in file %s' \
                  % (METRIC_STALE_AGE, file_path)
            self._plugin_failed(msg)
        return metrics

    def _is_reported(self, task_name, metric):
        # filter out 'suppress_ok' metrics
        if task_name in self.suppress_ok and metric.get('value') == OK:
            return False
        return True

    def _get_metrics(self, task_names, task_runner):
        reported = []
        summary = defaultdict(list)
        for task_name in task_names:
            summary['tasks'].append(task_name)
            metrics = task_runner(task_name)
            if not isinstance(metrics, list):
                metrics = [metrics]
            for metric in metrics:
                summary[metric.get('value')].append(metric)
                summary['total'].append(metric)
                if self._is_reported(task_name, metric):
                    reported.append(metric)
        return reported, summary

    def _csv_to_list(self, csv):
        return [f.strip() for f in csv.split(',') if f]

    def _load_instance_config(self, instance):
        self.log.debug('instance config %s' % str(instance))
        self.metrics_files = list()

        parsed_metrics_files = list(set(self._csv_to_list(
            instance.get('metrics_files', ''))))

        for entry in parsed_metrics_files:
            # Resolve wildcard metric file patterns if any
            if set('[*?]').intersection(set(entry)):
                self.metrics_files.extend(glob.glob(entry))
            else:
                self.metrics_files.append(entry)

        self.log.debug('Using metrics files %s' % str(self.metrics_files))

        if instance.get('subcommands') is None:
            self.subcommands = self.DEFAULT_SUBCOMMANDS
        else:
            self.subcommands = self._csv_to_list(instance.get('subcommands'))
        self.log.debug('Using subcommands %s' % str(self.subcommands))

        if instance.get('suppress_ok') is None:
            self.suppress_ok = self.DEFAULT_SUPPRESS_OK
        else:
            self.suppress_ok = self._csv_to_list(instance.get('suppress_ok'))
        self.plugin_failures = []

    def check(self, instance):
        self._load_instance_config(instance)
        all_metrics = list()

        # run command line tasks
        metrics, summary = self._get_metrics(
            self.subcommands, self._run_command_line_task)
        self.log_summary('command', summary)
        all_metrics.extend(metrics)

        # run load file tasks
        metrics, summary = self._get_metrics(
            self.metrics_files, self._run_load_file_task)
        self.log_summary('load file', summary)
        all_metrics.extend(metrics)

        # plugin status
        all_metrics.extend([self._plugin_check_metric()])

        current_timestamp = time.time()

        for metric in all_metrics:
            # apply any instance dimensions that may be configured,
            # overriding any dimension with same key that check has set.
            metric['dimensions'] = self._set_dimensions(metric['dimensions'],
                                                        instance)

            # Monasca API checks reported metrics at an interval of 1 minute,
            # and it expects atleast one metric instance posted within 2 minute
            # interval. Since we are allowing a flexible command execution time
            # period, we overwrite the timestamp with latest, to make sure
            # Monasca doesn't move the alarm to UNDETERMINED state
            metric['timestamp'] = current_timestamp

            self.log.debug(
                'metric %s %s %s %s %s'
                % (metric.get('timestamp'),
                   metric.get('metric'), metric.get('value'),
                   metric.get('value_meta'), metric.get('dimensions')))
            try:
                self.gauge(**metric)
            except Exception as e:  # noqa
                self.log.exception('Exception while reporting metric: %s' % e)
