# -*- coding: utf-8 -*-

"""Tests the signup view.
"""

from test import get_text
from spz.models import Applicant
from spz import token

from datetime import datetime, timedelta


def signup_set_open(course, open=True):
    language = course.language
    now = datetime.utcnow()
    delta = timedelta(hours=1)

    if open:
        language.signup_begin = now - delta
        language.signup_end = now + delta
        assert language.is_open_for_signup(now)
    else:
        language.signup_begin = now - 3 * delta
        language.signup_end = now - delta
        assert not language.is_open_for_signup(now)


def in_course(applicant_data, course):
    applicant = Applicant.query.filter(Applicant.mail == applicant_data['mail']).first()
    return applicant is not None and applicant.in_course(course)


def test_opened_signup(client, applicant_data, course):
    signup_set_open(course, open=True)

    data = dict(applicant_data, course=course.id)

    assert not in_course(applicant_data, course)

    response = client.post('/', data=data)
    response_text = get_text(response)

    assert "Ihre Registrierung war erfolgreich" in response_text
    assert in_course(applicant_data, course)


def test_closed_signup(client, applicant_data, course):
    signup_set_open(course, open=False)

    data = dict(applicant_data, course=course.id)

    assert not in_course(applicant_data, course)

    response = client.post('/', data=data)
    response_text = get_text(response)

    assert "Not a valid choice" in response_text

    assert not in_course(applicant_data, course)


def test_duplicate_signup(client, applicant_data, course):
    test_opened_signup(client, applicant_data, course)  # first signup

    data = dict(applicant_data, course=course.id)

    response = client.post('/', data=data)
    response_text = get_text(response)

    assert "Sie sind bereits für diesen Kurs oder einem Parallelkurs angemeldet!" in response_text


def test_priority_signup(client, applicant_data, course):
    signup_set_open(course, open=False)
    t = token.generate(applicant_data['mail'], namespace='preterm')

    url = '/?token={}'.format(t)
    data = dict(applicant_data, course=course.id)

    assert not in_course(applicant_data, course)

    response = client.post(url, data=data)
    response_text = get_text(response)

    assert "Prioritäranmeldung aktiv!" in response_text
    assert "Ihre Registrierung war erfolgreich" in response_text
    assert in_course(applicant_data, course)
