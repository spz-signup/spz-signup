# -*- coding: utf-8 -*-

"""Tests the application views.
"""

from test import login, logout, get_text


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
