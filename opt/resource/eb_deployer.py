from os import path
from subprocess import Popen, PIPE

from concourse_common.common import *
from concourse_common.jsonutil import *
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

        config_filepath = path.join(self.directory, get_params_value(self.payload, CONFIG_FILE_KEY), self.CONFIG_FILENAME)
        artifact_filepath = path.join(self.directory, get_params_value(self.payload, ARTIFACT_FILE_KEY))

        if not validate_path(config_filepath):
            log_error("Config file not found")
            return -1

        if not validate_path(artifact_filepath):
            log_error("Artifact not found")
            return -1

        deploy_command = ['eb_deploy', '-c', config_filepath, '-p', artifact_filepath, '-e', self.env]

        return self.execute_command(deploy_command, self.directory)

    def remove_service(self):
        if self.directory is '':
            log_error("Directory is not set.")
            return -1

        config_filepath = join_paths(self.directory, get_params_value(self.payload, CONFIG_FILE_KEY), self.CONFIG_FILENAME)

        if not validate_path(config_filepath):
            log_error("Config file not found")
            return -1

        remove_command = ['eb_deploy', '-c', config_filepath, '-e', self.env, '-d']

        return self.execute_command(remove_command, self.directory)

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
