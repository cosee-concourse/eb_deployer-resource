#! /usr/bin/env python3
from concourse_common.jsonutil import *
import schemas


def execute():
    valid, payload = load_and_validate_payload(schemas, Request.CHECK)
    if not valid:
        return -1

    print([{}])

    return 0

if __name__ == '__main__':
    exit(execute())
