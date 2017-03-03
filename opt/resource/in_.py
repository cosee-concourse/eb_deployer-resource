#! /usr/bin/env python3
import os

from concourse_common.jsonutil import *
from concourse_common.common import *

import schemas
from model import *


def execute(directory):
    valid, payload = load_and_validate_payload(schemas, Request.IN)
    if not valid:
        return -1

    with open(join_paths(directory, "env"), "w+") as file:
        file.write(get_version(payload, VERSION_JSON_NAME))

    print(get_version_output(get_version(payload, VERSION_JSON_NAME), VERSION_JSON_NAME))
    return 0


if __name__ == '__main__':
    if not check_system_argument_number():
        exit(-1)
    exit(execute(sys.argv[1]))
