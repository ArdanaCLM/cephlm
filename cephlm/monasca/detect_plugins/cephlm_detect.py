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

from monasca_setup import agent_config
import monasca_setup.detection
from monasca_setup.detection.utils import _get_dimensions
import os


class CephLMDetect(monasca_setup.detection.ArgsPlugin):
    """
    Detect if cephlm-probe will be monitoring.
    """
    CEPHLM_DIR = '/etc/cephlm'
    CHECK_NAME = 'cephlm_check'

    def __init__(self, template_dir, overwrite=True, args=None):
        super(CephLMDetect, self).__init__(
            template_dir, overwrite, args)

    def _detect(self):
        """
        Run detection, set self.available True if any ceph config is detected.
        (Called during superclass __init__).
        """
        self.available = False
        conf_file = 'cephlm.conf'
        if os.path.isfile(os.path.join(self.CEPHLM_DIR, conf_file)):
            self.available = True

    def build_config(self):
        """
        Build the config as a Plugins object and return.
        """
        config = agent_config.Plugins()
        parameters = {'name': self.CHECK_NAME}
        if self.args:
            for arg in ('metrics_files', 'subcommands', 'suppress_ok'):
                if arg in self.args:
                    parameters[arg] = self.args.get(arg)

        # set service and component
        dimensions = _get_dimensions('ceph-storage', None)
        if len(dimensions) > 0:
            parameters['dimensions'] = dimensions

        config[self.CHECK_NAME] = {'init_config': None,
                                   'instances': [parameters]}
        return config

    def dependencies_installed(self):
        """
        Return True if dependencies are installed.
        """
        return True
