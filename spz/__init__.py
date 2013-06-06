# -*- coding: utf-8 -*-

from flask import Flask


app = Flask(__name__, instance_relative_config=True)

from spz import views
from spz import errorhandlers


# vim: set tabstop=4 shiftwidth=4 expandtab:
