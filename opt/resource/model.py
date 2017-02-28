import os

from concourse_common import common
from enum import Enum
import schemas

VERSION_JSON_NAME = 'env'


class Model:

    def __init__(self, request):
        self.payload = common.load_payload()
        self.directory = ''

        if request == Request.CHECK:
            schema = schemas.checkSchema
        elif request == Request.IN:
            schema = schemas.inSchema
        else:
            schema = schemas.outSchema

        common.validate_payload(self.payload, schema)

    def get_access_key(self):
        access_key = self.payload['source']['access_key_id']
        return access_key

    def get_secret(self):
        secret_key = self.payload['source']['secret_access_key']
        return secret_key

    def get_config_file(self):
        config_filepath = self.payload['params']['config_file']
        config_absolute_filepath = os.path.join(config_filepath, 'eb_deployer.yml')
        return config_absolute_filepath

    def get_artifact_file(self):
        artifact_folder = self.payload['params']['artifact_file']
        return artifact_folder

    def get_env_file(self):
        return self.payload['params']['env_file']

    def get_env_name(self):
        return self.payload['params']['env']

    def env_file_exists(self):
        return 'env_file' in self.payload['params']

    def env_name_exists(self):
        return 'env' in self.payload['params']

    def is_deploy_command(self):
        return 'deploy' in self.payload['params'] and self.payload['params']['deploy']

    def is_remove_command(self):
        return 'remove' in self.payload['params'] and self.payload['params']['remove']

    def get_env_version(self):
        try:
            stage = self.payload['version'][VERSION_JSON_NAME]
        except KeyError:
            stage = None
        return stage


class Request(Enum):
    CHECK = 1
    IN = 2
    OUT = 3