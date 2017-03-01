import os
from multiprocessing import Process
from subprocess import Popen, PIPE

from concourse_common import common
from os import path


class Eb_deployer:
    def __init__(self, model, env='dev'):
        self.model = model
        self.env = env

    def deploy_service(self):
        if self.model.directory is '':
            common.log_error("Directory is not set.")
            return -1

        config_filepath = path.join(self.model.directory, self.model.get_config_file())
        artifact_filepath = path.join(self.model.directory, self.model.get_artifact_file())

        if not common.validate_path(config_filepath):
            common.log_error("Config file not found")
            return -1

        if not common.validate_path(artifact_filepath):
            common.log_error("Artifact not found")
            return -1

        deploy_command = ['eb_deploy', '-c', config_filepath, '-p', artifact_filepath, '-e', self.env]

        return self.execute_command(deploy_command, self.model.directory)

    def remove_service(self):
        if self.model.directory is '':
            common.log_error("Directory is not set.")
            return -1

        config_filepath = path.join(self.model.directory, self.model.get_config_file())

        remove_command = ['eb_deploy', '-c', config_filepath, '-e', self.env, '-d']

        return self.execute_command(remove_command, self.model.directory)

    def execute_command(self, command, directory=None):
        environment = os.environ.copy()
        environment['AWS_ACCESS_KEY_ID'] = self.model.get_access_key()
        environment['AWS_SECRET_ACCESS_KEY'] = self.model.get_secret()

        p = Popen(command, stdout=PIPE, stderr=PIPE, env=environment, cwd=directory or '/', universal_newlines=True)

        out, err = p.communicate()
        common.log_info(out)
        common.log_error(err)

        common.log_info("{} exited with {}".format(command[0:2], p.returncode))

        return p.returncode
