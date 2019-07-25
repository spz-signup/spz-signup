# -*- coding: utf-8 -*-

"""Tests the application views.
"""
import pytest

from spz import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

#    with app.app_context():
#        app.init_db()

    yield client


def test_startpage(client):
    assert client.get('/').status_code == 200
