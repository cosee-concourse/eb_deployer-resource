#! /usr/bin/env python3

from concourse_common.common import *
from concourse_common.jsonutil import *

import schemas
from model import *


def execute(directory):
    valid, payload = load_and_validate_payload(schemas, Request.IN)
    if not valid:
        return -1

    with open(join_paths(directory, "env"), "w+") as file:
        file.write(get_version(payload, VERSION_KEY_NAME))

    print(get_version_output(get_version(payload, VERSION_KEY_NAME), VERSION_KEY_NAME))
    return 0


if __name__ == '__main__':
    if not check_system_argument_number():
        exit(-1)
    exit(execute(sys.argv[1]))
