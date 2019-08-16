# -*- coding: utf-8 -*-

"""Provides pytest fixtures to tests.
"""

from pytest import fixture
from spz import app, db
from spz.models import User
from util.init_db import recreate_tables, insert_resources


def create_user(mail, superuser=False, languages=[]):
    user = User(mail, active=True, superuser=superuser, languages=languages)
    password = user.reset_password()
    db.session.add(user)
    db.session.commit()
    return (mail, password)


@fixture
def client():
    client = app.test_client()

    recreate_tables()
    insert_resources()

    with app.app_context():  # app context allows for implicit database session usage
        yield client


@fixture
def superuser():
    yield create_user('superuser@localhost', superuser=True)


@fixture
def user():
    yield create_user('user@localhost')
