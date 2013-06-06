# -*- coding: utf-8 -*-

from spz import app


# do not try to import this, instead run it like:
# python runserver.py

# guard against accidental imports
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)


# vim: set tabstop=4 shiftwidth=4 expandtab:
