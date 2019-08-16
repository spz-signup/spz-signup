# -*- coding: utf-8 -*-

"""Tests the application views.
"""

from . import login, logout, get_text
from test.fixtures import client, user, superuser
from spz import app
from spz.models import Course, Origin, Degree, Graduation


def test_startpage(client):
    response = client.get('/')
    response_text = get_text(response)
    assert 'Anmeldung' in response_text
    assert 'Kurswahl' in response_text
    assert 'Persönliche Angaben' in response_text
    assert 'Absenden' in response_text


def test_login(client, user, superuser):
    response = login(client, user)
    response_text = get_text(response)
    logout(client)
    assert 'Angemeldet als {} ()'.format(user[0]) in response_text

    response = login(client, superuser)
    response_text = get_text(response)
    logout(client)
    assert 'Angemeldet als {} (SUPERUSER)'.format(superuser[0]) in response_text

    response = login(client, (user[0], 'definately-wrong-password'))
    response_text = get_text(response)
    logout(client)
    assert 'Du kommst hier net rein!' in response_text

    response = login(client, ('definately-wrong-username', user[1]))
    response_text = get_text(response)
    logout(client)
    assert 'Du kommst hier net rein!' in response_text


def test_signup(client, superuser):
    with app.app_context():  # lazy load (as used in course.full_name()) will fail otherwise
        course = Course.query.first()
        origin = Origin.query.first()
        degree = Degree.query.first()
        graduation = Graduation.query.first()
        course_name = course.full_name()
    name = ('Mika', 'Müller')
    tag = '123456'
    phone = '01521 1234567'
    mail = 'mika.mueller@beispiel.de'
    semester = 1
    data = dict(
        course=course.id,
        first_name=name[0],
        last_name=name[1],
        phone=phone,
        mail=mail,
        confirm_mail=mail,
        origin=origin.id)

    if origin.validate_registration:
        data = dict(
            data,
            tag=tag,
            degree=degree.id,
            semester=semester,
            graduation=graduation.id)

    login(client, superuser)  # login to override time-delta restrictions
    response = client.post('/', data=data)
    response_text = get_text(response)
    logout(client)

    assert '{} {} – Sie haben sich für den Kurs {} beworben.'.format(name[0], name[1], course_name) in response_text
