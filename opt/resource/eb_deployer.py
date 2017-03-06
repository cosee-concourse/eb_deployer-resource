from os import path
from subprocess import Popen, PIPE

from concourse_common.common import *
from concourse_common.jsonutil import *
from concourse_common.archiveutil import files
import re
from model import *


class EBDeployer:
    CONFIG_FILENAME = 'eb_deployer.yml'

    def __init__(self, payload, directory, env='dev'):
        self.payload = payload
        self.directory = directory
        self.env = env

    def deploy_service(self):
        if self.directory is '':
            log_error("Directory is not set.")
            return -1

        config_filepath = path.join(self.directory, get_params_value(self.payload, CONFIG_FILE_KEY))

        artifact_regex = get_params_value(self.payload, ARTIFACT_FILE_KEY)
        artifact_filename = self.get_artifact_filename(artifact_regex)

        if artifact_filename is None:
            log_error("No Artifact found for specified regex")
            return -1

        artifact_filepath = path.join(self.directory, artifact_filename)

        if not validate_path(join_paths(config_filepath, 'config', self.CONFIG_FILENAME)):
            log_error("Config file not found")
            return -1

        if not validate_path(artifact_filepath):
            log_error("Artifact not found")
            return -1

        deploy_command = ['eb_deploy', '-p', artifact_filepath, '-e', self.env]

        return self.execute_command(deploy_command, config_filepath)

    def remove_service(self):
        if self.directory is '':
            log_error("Directory is not set.")
            return -1

        config_filepath = join_paths(self.directory, get_params_value(self.payload, CONFIG_FILE_KEY))

        if not validate_path(join_paths(config_filepath, 'config', self.CONFIG_FILENAME)):
            log_error("Config file not found")
            return -1

        remove_command = ['eb_deploy', '-e', self.env, '-d']

        return self.execute_command(remove_command, config_filepath)

    def execute_command(self, command, directory=None):
        environment = os.environ.copy()
        environment['AWS_ACCESS_KEY_ID'] = get_source_value(self.payload, ACCESS_KEY)
        environment['AWS_SECRET_ACCESS_KEY'] = get_source_value(self.payload, SECRET_KEY)

        p = Popen(command, stdout=PIPE, stderr=PIPE, env=environment, cwd=directory or '/', universal_newlines=True)

        out, err = p.communicate()
        log_info(out)
        log_error(err)

        log_info("{} exited with {}".format(command[0:2], p.returncode))

        return p.returncode

    @staticmethod
    def get_artifact_filename(artifact_regex):
        elements = artifact_regex.split('/')
        artifact_file_regex = elements[len(elements) - 1]

        artifact_filename = None
        for file in files(path.dirname(artifact_file_regex)):
            m = re.match(artifact_file_regex, file)
            if m is not None:
                artifact_filename = m.group(0)
        return path.join(path.dirname(artifact_regex), artifact_filename)
