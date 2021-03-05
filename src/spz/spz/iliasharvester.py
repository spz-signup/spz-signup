# -*- coding: utf-8 -*-

"""Module that harvests approval data from Ilias.

.. code-block:: python
"""
import csv
import requests
from spz import app, db, models
from bs4 import BeautifulSoup
from urllib import parse


# headers that will be used for all Ilias HTTPS requests
headers = {
    'Accept-Language': 'en-US,en;q=0.8,de-DE;q=0.5,de;q=0.3',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0',
}


def get_export_parameters(html):
    parsed_html = BeautifulSoup(html, 'html.parser')
    url = parsed_html.body.find('form', attrs={'id': 'ilToolbar'}).get('action')

    return dict(parse.parse_qsl(parse.urlsplit(url).query))


def download_data():
    """Download relevant CSV data from Ilias.

    Returns line->byte iterator."""

    username = app.config['ILIAS_USERNAME']
    password = app.config['ILIAS_PASSWORD']
    ref_id = app.config['ILIAS_REFID']
    url = app.config['ILIAS_URL']

    # get inital cookies
    url0 = '{}login.php'.format(url)
    r0 = requests.get(
        url0,
        headers=headers
    )
    assert r0.status_code == 200
    cookies = r0.cookies

    # login
    url1 = '{}ilias.php'.format(url)
    r1 = requests.post(
        url1,
        params={
            'baseClass': 'ilStartUpGUI',
            'client_id': 'pilot',
            'cmd': 'post',
            'cmdClass': 'ilstartupgui',
            'cmdNode': 'y3',
            'lang': 'de',
            'rtoken': '',
        },
        data={
            'cmd[doStandardAuthentication]': 'Anmelden',
            'password': password,
            'username': username,
        },
        cookies=cookies,
        headers=headers
    )
    assert r1.status_code == 200
    cookies = r1.history[0].cookies  # use cookies of first request

    # get bunch of metadata
    url2 = '{}ilias.php'.format(url)
    r2 = requests.get(
        url2,
        params={
            'baseClass': 'ilrepositorygui',
            'cmd': 'outEvaluation',
            'cmdClass': 'iltestevaluationgui',
            'cmdNode': 'ut:ph:112',
            'ref_id': ref_id,
        },
        cookies=cookies,
        headers=headers
    )
    assert r2.status_code == 200
    text2 = r2.text
    # these tokens occur multiple times but seem to be unique
    export_parameters = get_export_parameters(text2)
    rtoken = export_parameters['rtoken']
    active_id = export_parameters['active_id']

    # prepare form / virtual table so we get all the information we need
    # without this step, the "Matrikelnummer" won't be present.
    # WARNING: this change is stateful (i.e. Ilias keeps track of it, not the URI / cookie / session storage / ...)
    url3 = '{}ilias.php'.format(url)
    r3 = requests.post(
        url3,
        params={
            'baseClass': 'ilrepositorygui',
            'cmd': 'post',
            'cmdClass': 'iltestevaluationgui',
            'cmdNode': 'ut:ph:112',
            'fallbackCmd': 'outEvaluation',
            'ref_id': ref_id,
            'rtoken': rtoken,
        },
        data={
            'cmd[outEvaluation]': 'Aktualisieren',
            'course': '',
            'group': '',
            'name': '',
            'tblfshtst_eval_all': '1',
            'tblfstst_eval_all[]': 'matriculation',
            'tst_eval_all_table_nav': 'name:asc:0',
            'tst_eval_all_table_nav1': 'name:asc:0',
            'tst_eval_all_table_nav2': 'name:asc:0',
        },
        cookies=cookies,
        headers=headers
    )
    assert r3.status_code == 200

    # download file
    url4 = '{}ilias.php'.format(url)
    r4 = requests.post(
        url4,
        params={
            'active_id': active_id,
            'baseClass': 'ilrepositorygui',
            'cmd': 'post',
            'cmdClass': 'iltestevaluationgui',
            'cmdNode': 'ut:ph:112',
            'fallbackCmd': 'exportEvaluation',
            'ref_id': ref_id,
            'rtoken': rtoken,
        },
        data={
            'cmd[exportEvaluation]': 'Export',
            'export_type': 'csv',
        },
        cookies=cookies,
        headers=headers
    )
    assert r4.status_code == 200
    # don't use r2.text here, it's very very slow!
    it = r4.iter_lines()

    # logout
    url5 = '{}logout.php'.format(url)
    r5 = requests.post(
        url5,
        params={
            'lang': 'de',
        },
        cookies=cookies,
        headers=headers
    )
    assert r5.status_code == 200

    return it


def parse_data(it):
    """Parse CSV string from Ilias into list of Approval objects."""
    # do lazy string conversion for performance reasons
    # WARNING: Ilias emits invalid Unicode characters!
    fp = (line.decode('utf-8', 'replace') for line in it)
    reader = csv.reader(fp, dialect=csv.excel, delimiter=';')

    # get first row and do sanity check
    # don't be to smart here so we get errors in case the Ilias output changes.
    # when this happens we are going to double check the parser
    head = next(reader)
    assert head[0] == 'Name'
    assert head[1] == 'Benutzername'
    assert head[2] == 'Matrikelnummer'
    assert head[3] == 'Testergebnis in Punkten'
    assert head[4] == 'Maximal erreichbare Punktezahl'
    assert head[5] == 'Testergebnis als Note'
    # don't care about the rest

    # parse file
    approvals = []
    for idx, row in enumerate(reader, 1):
        # for some reason, Ilias emits a new header before every line,
        # so we only parse every second line.
        if idx % 2 == 0:
            continue

        # ==========================
        # == 1. get right columns ==
        # ==========================
        s_user = row[1]
        s_idnumber = row[2]
        s_points_got = row[3]
        s_points_max = row[4]

        # some lines might be empty/invalid
        if not ((bool(s_user) or bool(s_idnumber)) and bool(s_points_got) and bool(s_points_max)):
            continue

        # ==========================
        # == 2. parse data        ==
        # ==========================
        # normalized tag
        # prefer idnumber but fallback to username (e.g. for staff members)
        tag = s_idnumber.strip().lower() or s_user.strip().lower()

        # do not catch the exception here, so we know when something goes wrong
        points_got = int(s_points_got)
        points_max = int(s_points_max)

        # last sanity check
        if not (tag and points_got >= 0 and points_max > 0):
            continue

        # ==========================
        # == 3. create objects    ==
        # ==========================
        # limit rating to [0, 100] because for some reason,
        # points_got might be bigger than points_max
        rating = max(
            0,
            min(
                int(100 * points_got / points_max),
                100
            )
        )

        # finally add approval to output list
        approvals.append(
            models.Approval(
                tag=tag,
                percent=rating,
                sticky=False,
                priority=False
            )
        )

    return approvals


def download_and_parse_data():
    return parse_data(download_data())


def refresh():
    # Overwrite approvals in DB with newest Ilias data.
    approvals = download_and_parse_data()

    # start transaction rollback area
    try:
        # remove all non-sticky entries from DB
        models.Approval.query.filter(models.Approval.sticky == False).delete()  # NOQA

        # add all new approvals
        db.session.add_all(approvals)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
