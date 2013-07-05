# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from spz import db
from spz.models import *


def dummy_values():
    fst_lang = Language('First Language', datetime.utcnow(), datetime.utcnow() + timedelta(weeks=2))
    snd_lang = Language('Second Language', datetime.utcnow() + timedelta(days=2), datetime.utcnow() + timedelta(days=4))

    c1 = Course(fst_lang, '1a', limit=15, price=60)
    c2 = Course(fst_lang, '1b', limit=10, price=60)
    c3 = Course(snd_lang, '2a', limit=15, price=60)
    c4 = Course(snd_lang, '2b', limit=15, price=120)
    db.session.add_all([c1, c2, c3, c4])

    bsc = Degree('Bachelor')
    msc = Degree('Master')
    db.session.add_all([bsc, msc])

    o1 = Origin('First origin')
    o2 = Origin('Second origin', 'Department')
    db.session.add_all([o1, o2])

    db.session.commit()


# Has to be done only once, to initialize the database;
# do not use this in regular code

if __name__ == '__main__':
    db.create_all()

    dummy_values()


# vim: set tabstop=4 shiftwidth=4 expandtab:
