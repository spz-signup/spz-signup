# -*- coding: utf-8 -*-

"""Testing resources.

   See https://pytest.org/ for information about automatic test-discovery.
"""

from bs4 import BeautifulSoup


def login(client, credentials):
    return client.post('/internal/login', data=dict(
            user=credentials[0],
            password=credentials[1]),
        follow_redirects=True)


def logout(client):
    return client.post('/internal/logout', follow_redirects=True)


def get_text(response):
    html = BeautifulSoup(response.data, 'html.parser')
    return html.find('div', {'class': 'main'}).get_text()
