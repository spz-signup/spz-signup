# -*- coding: utf-8 -*-

"""Tests the application views.
"""
import pytest

from spz import app, db
from spz.models import User
from util.init_db import recreate_tables, insert_resources
from bs4 import BeautifulSoup


@pytest.fixture
def client():
    client = app.test_client()

    recreate_tables()
    insert_resources()

    yield client


def create_user(mail, superuser=False, languages=[]):
    user = User(mail, active=True, superuser=superuser, languages=languages)
    password = user.reset_password()
    db.session.add(user)
    db.session.commit()
    return (mail, password)


def login(client, user, password):
    return client.post('/internal/login', data=dict(
            user=user,
            password=password),
        follow_redirects=True)


def logout(client):
    return client.post('/internal/logout', follow_redirects=True)


def get_text(response, expected_response_code=200):
    assert response.status_code == expected_response_code
    html = BeautifulSoup(response.data, 'html.parser')
    return html.body.get_text()


def test_startpage(client):
    response = client.get('/')
    response_text = get_text(response)
    assert 'Anmeldung' in response_text
    assert 'Kurswahl' in response_text
    assert 'Persönliche Angaben' in response_text
    assert 'Absenden' in response_text


def test_login(client):
    credentials = create_user('test@localhost', superuser=True)

    response = login(client, credentials[0], credentials[1])
    response_text = get_text(response)
    assert 'Angemeldet als {} (SUPERUSER)'.format(credentials[0]) in response_text
    logout(client)

    response = login(client, credentials[0], 'definately-wrong-password')
    response_text = get_text(response)
    assert 'Du kommst hier net rein!' in response_text
    logout(client)

    response = login(client, 'definately-wrong-username', credentials[1])
    response_text = get_text(response)
    assert 'Du kommst hier net rein!' in response_text
    logout(client)
