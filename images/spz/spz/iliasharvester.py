# -*- coding: utf-8 -*-

"""Module that harvests approval data from Ilias.

How you should do it:

    import pysimplesoap

    # WARNING: Ilias requires us to conform to the given parameter order
    #          For that reason, we build XML data by hand rather using the
    #          automatic kwargs conversion of pysimplesoap

    cl = pysimplesoap.client.SoapClient(
        location='https://ilias.studium.kit.edu/webservice/soap/server.php',
        namespace='urn:ilUserAdministration'
    )

    def get_sid(client):
        element = SimpleXMLElement(
            '<login xmlns="urn:ilUserAdministration">'
            '<client>produktiv</client>'
            '<username>????????</username>'
            '<password>????????</password>'
            '</login>'
        )
        response = client.call('login', element)
        return str(response('sid'))

    sid = get_sid(cl)
    ref_id=????????

    def get_data(client, sid, ref_id):
        element = SimpleXMLElement(
            '<getTestResults xmlns="urn:ilUserAdministration">'
            '<sid>{}</sid>'
            '<ref_id>{}</ref_id>'
            '<sum_only>false</sum_only>'
            '</getTestResults>'.format(sid, ref_id)
        )
        response = client.call('getTestResults', element)
        reutrn SimpleXMLElement(str(response('xml')))

    data = get_data(cl, sid, ref_id)
    for row in data.rows.row:
        mtr = row.column[4]
        # sadly, this is where it stops working, because all relevant data (all scores) are zero,
        # thanks to the shitty, untested Ilias SOAP interface.


So instead, we are emulating the requests that a browser would do to download the data.
"""

import csv

import requests

from spz import app, db, models


# headers that will be used for all Ilias HTTPS requests
headers = {
    'Accept-Language': 'en-US,en;q=0.8,de-DE;q=0.5,de;q=0.3',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0',
}


def extract_text(s, token_begin, token_end):
    """Extract text from string that is located between 2 tokens."""
    l0 = len(token_begin)
    idx0 = s.find(token_begin)
    assert idx0 > -1

    begin = idx0 + l0

    idx1 = s.find(token_end, begin)
    assert idx1 > -1

    end = idx1
    return s[begin:end]


def download_data():
    """Download relevant CSV data from Ilias.

    Returns line->byte iterator."""
    # get inital cookies
    url0 = '{}login.php'.format(app.config['ILIAS_URL'])
    r0 = requests.get(
        url0,
        params={
            'client_id': 'produktiv',
            'cmd': 'force_login',
            'lang': 'de',
            'target': '',
        },
        headers=headers
    )
    assert r0.status_code == 200
    cookies = r0.cookies

    # login
    url1 = '{}ilias.php'.format(app.config['ILIAS_URL'])
    r1 = requests.post(
        url1,
        params={
            'baseClass': 'ilStartUpGUI',
            'client_id': 'produktiv',
            'cmd': 'post',
            'cmdClass': 'ilstartupgui',
            'cmdNode': 'fp',
            'lang': 'de',
            'rtoken': '',
        },
        data={
            'cmd[showLogin]': 'Anmelden',
            'password': app.config['ILIAS_PASSWORD'],
            'username': app.config['ILIAS_USERNAME'],
        },
        cookies=cookies,
        headers=headers
    )
    assert r1.status_code == 200
    cookies = r1.history[0].cookies  # use cookies of first request

    # get bunch of metadata
    url2 = '{}ilias.php'.format(app.config['ILIAS_URL'])
    r2 = requests.get(
        url2,
        params={
            'baseClass': 'ilObjTestGUI',
            'cmd': 'outEvaluation',
            'cmdClass': 'iltestevaluationgui',
            'cmdNode': 'a2:a5',
            'ref_id': app.config['ILIAS_REFID'],
        },
        cookies=cookies,
        headers=headers
    )
    assert r2.status_code == 200
    text2 = r2.text
    # these tokens occur multiple times but seem to be unique
    rtoken = extract_text(text2, "rtoken=", "&")
    active_id = extract_text(text2, "active_id=", "&")

    # prepare form / virtual table so we get all the information we need
    # without this step, the "Matrikelnummer" won't be present.
    # WARNING: this change is stateful (i.e. Ilias keeps track of it, not the URI / cookie / session storage / ...)
    url3 = '{}ilias.php'.format(app.config['ILIAS_URL'])
    r3 = requests.post(
        url3,
        params={
            'baseClass': 'ilObjTestGUI',
            'cmd': 'post',
            'cmdClass': 'iltestevaluationgui',
            'cmdNode': 'a2:a5',
            'fallbackCmd': 'outEvaluation',
            'ref_id': app.config['ILIAS_REFID'],
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
    url4 = '{}ilias.php'.format(app.config['ILIAS_URL'])
    r4 = requests.post(
        url4,
        params={
            'active_id': active_id,
            'baseClass': 'ilObjTestGUI',
            'cmd': 'post',
            'cmdClass': 'iltestevaluationgui',
            'cmdNode': 'a2:a5',
            'fallbackCmd': 'exportEvaluation',
            'ref_id': app.config['ILIAS_REFID'],
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
    url5 = '{}logout.php'.format(app.config['ILIAS_URL'])
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


def refresh():
    """Overwrite approvals in DB with newest Ilias data."""
    it = download_data()
    approvals = parse_data(it)

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
