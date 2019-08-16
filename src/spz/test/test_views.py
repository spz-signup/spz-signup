# -*- coding: utf-8 -*-

"""Tests the application views.
"""

from test import login, logout, get_text
from spz.models import Course, Origin, Degree, Graduation, Applicant


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


def fake_person(mail):
    return dict(
        first_name='Mika',
        last_name='Müller',
        phone='01521 1234567',
        mail=mail,
        confirm_mail=mail,
        tag='123456',
        semester=1)


def test_signup(client, superuser):
    course = Course.query.first()
    origin = Origin.query.first()
    degree = Degree.query.first()
    graduation = Graduation.query.first()
    mail = 'mika.mueller@beispiel.de'
    data = dict(
        fake_person(mail),
        course=course.id,
        origin=origin.id,
        degree=degree.id,
        graduation=graduation.id)

    login(client, superuser)  # login to override time-delta restrictions
    response = client.post('/', data=data)
    response_text = get_text(response)
    logout(client)

    assert '{} {} – Sie haben sich für den Kurs {} beworben.'.format(
        data['first_name'], data['last_name'], course.full_name()) in response_text

    applicant = Applicant.query.filter(Applicant.mail == mail).first()
    assert applicant.in_course(course)
