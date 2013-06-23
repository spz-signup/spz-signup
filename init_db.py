# -*- coding: utf-8 -*-

from spz import db
from spz.models import *


# Has to be done only once, to initialize the database;
# do not use this in regular code

if __name__ == '__main__':
    db.create_all()


# vim: set tabstop=4 shiftwidth=4 expandtab:
