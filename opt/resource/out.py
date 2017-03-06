#! /usr/bin/env python3

from concourse_common import ioutil
from concourse_common.common import *
from concourse_common.jsonutil import *

import schemas
from eb_deployer import EBDeployer
from model import *


def is_deploy_command(payload):
    if contains_params_key(payload, DEPLOY_KEY):
        return get_params_value(payload, DEPLOY_KEY)
    return False


def is_remove_command(payload):
    if contains_params_key(payload, REMOVE_KEY):
        return get_params_value(payload, REMOVE_KEY)
    return False


def execute(directory):
    valid, payload = load_and_validate_payload(schemas, Request.OUT)
    if not valid:
        return -1
    # change directory to config folder and make artifact path fixed
    if contains_params_key(payload, ENV_FILE_KEY):
        env = ioutil.read_file(join_paths(directory, get_params_value(payload, ENV_FILE_KEY)))
    elif contains_params_key(payload, ENV_KEY):
        env = get_params_value(payload, ENV_KEY)
    else:
        log_error("Requires env or env_file.")
        return -1

    eb_deployer = EBDeployer(payload, directory, env)

    result = 0

    if is_deploy_command(payload):
        result = eb_deployer.deploy_service()

    if is_remove_command(payload):
        result = eb_deployer.remove_service()

    if result == 0:
        print(get_version_output(env, VERSION_KEY_NAME))

    return result


if __name__ == '__main__':
    if not check_system_argument_number():
        exit(-1)
    exit(execute(sys.argv[1]))
