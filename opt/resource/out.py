#! /usr/bin/env python3
import io
import json
import sys
from os import path

from concourse_common import common
from model import Model, Request, VERSION_JSON_NAME
from eb_deployer import Eb_deployer


def execute(directory):
    try:
        model = Model(Request.OUT)
    except TypeError:
        return -1

    if model.env_file_exists():
        env = io.open(path.join(directory, model.get_env_file()), "r").read()
    elif model.env_name_exists():
        env = model.get_env_name()
    else:
        common.log_error("Requires env or env_file.")
        return -1

    eb_deployer = Eb_deployer(model, env)

    result = 0

    model.directory = directory

    if model.is_deploy_command():
        result = eb_deployer.deploy_service()

    if model.is_remove_command():
        result = eb_deployer.remove_service()

    if result == 0:
        print(json.dumps({'version': {VERSION_JSON_NAME: env}}))

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        common.log_error("Wrong number of arguments!")
        exit(-1)
    exit(execute(sys.argv[1]))
