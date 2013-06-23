# -*- coding: utf-8 -*-

import argparse

from spz import app


# Do not try to import this, instead run it like:
# python runserver.py


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Starts a local development server running the spz application')

    mode = parser.add_mutually_exclusive_group(required=False)
    mode.add_argument('-p', '--profile', dest='profiling', action="store_true",
                      help='Enable profiling support, see: http://werkzeug.pocoo.org/docs/contrib/profiler/')
    mode.add_argument('-l', '--lint', dest='linting', action="store_true",
                      help='Enable WSGI sanity checks, see: http://werkzeug.pocoo.org/docs/contrib/lint/')

    args = parser.parse_args()

    if args.profiling:
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app)

    elif args.linting:
        from werkzeug.contrib.lint import LintMiddleware
        app.wsgi_app = LintMiddleware(app.wsgi_app)

    app.run(host='127.0.0.1', port=8080)


# vim: set tabstop=4 shiftwidth=4 expandtab:
