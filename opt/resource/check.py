#! /usr/bin/env python3
from model import Model, Request


def execute():
    try:
        Model(Request.CHECK)
    except TypeError:
        return -1

    print([{}])

    return 0

if __name__ == '__main__':
    exit(execute())
