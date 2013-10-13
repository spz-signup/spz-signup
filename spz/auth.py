# -*- coding: utf-8 -*-

"""Authentication management.

   Provides means for logging the user in / out and retrieving the current user from the g object.

   .. seealso:: https://developer.mozilla.org/en-US/docs/Mozilla/Persona
"""

import requests
from flask import session, request, json, abort

from spz import app


def login_handler():
    """Dispatches the authentication; sends the browser's identity assertion.

       The request finally authenticates the user.
    """
    resp = requests.post(app.config['PERSONA_VERIFIER'], data={
        'assertion': request.form['assertion'],
        'audience': request.host_url,
    }, verify=True)

    if resp.ok:
        verification_data = json.loads(resp.content)
        if verification_data['status'] == 'okay':
            session['email'] = verification_data['email']
            return 'OK'

    abort(400)


def logout_handler():
    """Logout handling.

       No dispatching or request is needed.
       The user's authentication is not valid anymore after calling this.
    """
    session.clear()
    return 'OK'


# vim: set tabstop=4 shiftwidth=4 expandtab:
