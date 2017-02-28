#! /usr/bin/env python3
import json
import os
import sys

from concourse_common import common
from model import Model, Request, VERSION_JSON_NAME


def execute(directory):
    try:
        model = Model(Request.IN)
    except TypeError:
        return -1

    with open(os.path.join(directory, "env"), "w+") as file:
        file.write(model.get_env_version())

    if model.get_env_version() is None:
        print([{}])
    else:
        print(json.dumps({"version": {VERSION_JSON_NAME: model.get_env_version()}}))

    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        common.log_error("Wrong number of arguments!")
        exit(-1)
    exit(execute(sys.argv[1]))
