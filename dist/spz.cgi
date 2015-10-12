#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This files is only needed for deploying the project with
# the CGI protocol. You do not need it while developing.

# For various server configurations see:
# http://flask.pocoo.org/docs/deploying/cgi/#server-setup


from wsgiref.handlers import CGIHandler
from spz import app


CGIHandler().run(app)
