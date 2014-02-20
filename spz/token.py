# -*- coding: utf-8 -*-

"""One-Time-Token management for a single signup permission.

"""

import hmac
import hashlib
from datetime import timedelta

from itsdangerous import URLSafeTimedSerializer as Signer

from spz import app


def generate(mail, signer=Signer(app.config['TOKEN_SECRET_KEY'])):
    """Generates a mail-specific one-time-token.

       The return value is sanitized to be used in URLs, e.g. as GET argument.

       .. warning::
          * Return value partially depends on time. f_t1(m) != f_t2(m).
          * Use the corresponding validate function instead of equality checking.
    """
    return signer.dumps(mail)

    # XXX: alt. impl., validate in the following month
    # return hmac.new(app.config['TOKEN_SECRET_KEY'], mail, hashlib.sha256).hexdigest()


def validate(token, mail, max_age=timedelta(weeks=1).total_seconds(), signer=Signer(app.config['TOKEN_SECRET_KEY'])):
    """Validates a mail-specific one-time-token.

       Additional checking is done for its integrity and expiration, defaulting to one week.
    """

    # guard against obviously invalid inputs
    if not token or not mail:
        return False

    # we're not interested in the exception type (BadSignature, SignatureExpired)
    # see: https://pythonhosted.org/itsdangerous/#responding-to-failure
    ok, payload = signer.loads_unsafe(token, max_age=max_age)
    return ok and payload == mail

    # XXX: alt. impl., validate in the following month
    # prevent None token, mail: otherwise generated token is already nonsense
    #return token and mail and token == generate_token(mail)


# vim: set tabstop=4 shiftwidth=4 expandtab:
