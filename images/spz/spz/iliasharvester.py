# -*- coding: utf-8 -*-

"""Module that harvests approval data from Ilias.

.. code-block:: python
"""
from pysimplesoap import simplexml
import pysimplesoap
from spz import app, db, models

# WARNING: Ilias requires us to conform to the given parameter order
#          For that reason, we build XML data by hand rather using the
#          automatic kwargs conversion of pysimplesoap


def get_sid(client, username, password):
    element = simplexml.SimpleXMLElement(
        '<login xmlns="urn:ilUserAdministration">'
        '<client>pilot</client>'
        '<username>{}</username>'
        '<password>{}</password>'
        '</login>'.format(username, password)
    )
    response = client.call('login', element)
    return str(response('sid'))


def get_data(client, sid, ref_id):
    element = simplexml.SimpleXMLElement(
        '<getTestResults xmlns="urn:ilUserAdministration">'
        '<sid>{}</sid>'
        '<ref_id>{}</ref_id>'
        '<sum_only>true</sum_only>'
        '</getTestResults>'.format(sid, ref_id)
    )
    response = client.call('getTestResults', element)
    return simplexml.SimpleXMLElement(str(response('xml')))


def download_and_parse_data():
    # get credentials
    username = app.config['ILIAS_USERNAME']
    password = app.config['ILIAS_PASSWORD']
    ref_id = app.config['ILIAS_REFID']
    url = app.config['ILIAS_URL']

    cl = pysimplesoap.client.SoapClient(
        location=url,
        namespace='urn:ilUserAdministration'
    )

    # get session id and download data
    sid = get_sid(cl, username, password)
    data = get_data(cl, sid, ref_id)

    # parse xml response
    approvals = []
    for row in data.row:
        col = row.column

        # normalized tag
        # prefer idnumber but fallback to username (e.g. for staff members)
        tag = str(col[4]).strip().lower() or str(col[1]).strip().lower()

        # do not catch the exception here, so we know when something goes wrong
        points_max = int(col[5])
        points_got = int(col[6])

        # last sanity check
        if not (tag and points_got >= 0 and points_max > 0):
            continue

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
    # Overwrite approvals in DB with newest Ilias data.
    print("Start ilias")
    approvals = download_and_parse_data()
    # start transaction rollback area
    try:
        # remove all non-sticky entries from DB
        models.Approval.query.filter(models.Approval.sticky == False).delete()  # NOQA

        # add all new approvals
        db.session.add_all(approvals)
        db.session.commit()
        print("End ilias")

    except Exception:
        db.session.rollback()
        raise
