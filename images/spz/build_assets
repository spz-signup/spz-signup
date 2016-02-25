#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from webassets.script import CommandLineEnvironment

from spz import assets_env

# Setup a logger
log = logging.getLogger('webassets')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

cmdenv = CommandLineEnvironment(assets_env, log)
cmdenv.build()
