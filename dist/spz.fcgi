#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This files is only needed for deploying the project with
# the FastCGI protocol. You do not need it while developing.

# For various server configurations see:
# http://flask.pocoo.org/docs/deploying/fastcgi/#fastcgi

# If you're deploying on Lighttpd, you have use a middleware:
# from werkzeug.contrib.fixers import LighttpdCGIRootFix
# WSGIServer(LighttpdCGIRootFix(app)).run()


from flup.server.fcgi import WSGIServer
from spz import app


if __name__ == '__main__':
    WSGIServer(app, bindAddress='/path/to/fcgi.sock').run()
