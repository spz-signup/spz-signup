#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from webassets.script import CommandLineEnvironment

from spz import assets_env

# Setup a logger
log = logging.getLogger('webassets')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


def build_assets():
    cmdenv = CommandLineEnvironment(assets_env, log)
    cmdenv.build()


if __name__ == '__main__':
    build_assets()
