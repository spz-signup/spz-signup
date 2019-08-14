# -*- coding: utf-8 -*-

"""Tests the application views.
"""
import pytest

from spz import app
from util.init_db import recreate_tables, insert_resources


@pytest.fixture
def client():
    client = app.test_client()

    recreate_tables()
    insert_resources()

    yield client


def test_startpage(client):
    assert client.get('/').status_code == 200
