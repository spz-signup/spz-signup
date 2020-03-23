# -*- coding: utf-8 -*-

"""Provides pytest fixtures.
"""

from pytest import fixture
from spz import app, db
from spz.models import User, Origin, Degree, Graduation, Course
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


@fixture
def applicant_data(mail='mika.mueller@beispiel.de'):
    yield dict(
        first_name='Mika',
        last_name='Müller',
        phone='01521 1234567',
        mail=mail,
        confirm_mail=mail,
        tag='123456',
        semester=1,
        origin=Origin.query.first().id,
        degree=Degree.query.first().id,
        graduation=Graduation.query.first().id
    )


@fixture
def other_applicant_data(mail='max.muster@beispiel.de'):
    yield dict(
        first_name='Max',
        last_name='Muster',
        phone='01522 7654321',
        mail=mail,
        confirm_mail=mail,
        tag='654321',
        semester=3,
        origin=Origin.query.first().id,
        degree=Degree.query.first().id,
        graduation=Graduation.query.first().id
    )


@fixture
def courses(limit=10):
    # raise limit to stress test the export feature
    recreate_tables()
    insert_resources()
    with app.app_context():
        yield Course.query.limit(limit).all()


@fixture
def course():
    with app.app_context():
        yield Course.query.first()


@fixture
def other_course():
    with app.app_context():
        yield Course.query.filter(Course.id != Course.query.first().id).first()
