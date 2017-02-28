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

        def print_stderr(prog):
            while True:
                nextline = prog.stderr.readline()
                if nextline == b'' and prog.poll() is not None:
                    break
                common.log_error(nextline.rstrip().decode('ascii'))

        def print_stdout(prog):
            """
            print stdout to stderr because only thing printed to stdout should be result json
            """
            while True:
                nextline = prog.stdout.readline()
                if nextline == b'' and prog.poll() is not None:
                    break
                common.log_info(nextline.rstrip().decode('ascii'))

        p = Popen(command, stdout=PIPE, stderr=PIPE, env=environment, cwd=directory or '/')

        out_p = Process(target=print_stdout(p))
        out_e = Process(target=print_stderr(p))

        out_e.start()
        out_p.start()

        out_p.join()
        out_e.join()

        returncode = p.wait()

        common.log_info("{} exited with {}".format(command[0:2], returncode))

        return p.returncode
