# -*- coding: utf-8 -*-

"""One-Time-Token management for a single signup permission.

"""

from datetime import timedelta

from hashlib import sha256

from sqlalchemy import func
from itsdangerous import URLSafeTimedSerializer as Signer

from spz import app, models


def get_default_signer():
    """Returns default signer for that application."""
    return Signer(
        app.config['TOKEN_SECRET_KEY'],
        salt='spz.token',
        signer_kwargs={
            'key_derivation': 'hmac',
            'digest_method': sha256,
        },
    )


def generate(mail, signer=None):
    """Generates a mail-specific one-time-token.

       The return value is sanitized to be used in URLs, e.g. as GET argument.

       .. warning::
          * Return value partially depends on time. f_t1(m) != f_t2(m).
          * Use the corresponding validate function instead of equality checking.
    """
    if not signer:
        signer = get_default_signer()
    return signer.dumps(mail)


def validate(token, mail, max_age=timedelta(weeks=2).total_seconds(), signer=None):
    """Validates a mail-specific one-time-token.

       Additional checking is done for its integrity and expiration, defaulting to one week.
    """
    if not signer:
        signer = get_default_signer()

    # guard against obviously invalid inputs
    if not token or not mail:
        return False

    # we're not interested in the exception type (BadSignature, SignatureExpired)
    # see: https://pythonhosted.org/itsdangerous/#responding-to-failure
    # however, payload can be `None` after this call
    ok, payload = signer.loads_unsafe(token, max_age=max_age)

    # token is only valid if it's associated mail is not already in the database
    # this way we're able to guarantee the token's one-time property
    found = models.Applicant.query.filter(func.lower(models.Applicant.mail) == func.lower(mail)).first()

    # case insensitive mail address check, otherwise confusing!
    same = payload and (payload.lower() == mail.lower())

    return ok and same and not found
