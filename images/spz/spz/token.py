# -*- coding: utf-8 -*-

"""One-Time-Token management for a single signup permission.

"""

from datetime import timedelta

from hashlib import sha256

from sqlalchemy import func
from itsdangerous import URLSafeTimedSerializer as Signer

from spz import app


def get_default_signer(namespace=None):
    """Returns default signer for that application."""
    if not namespace:
        namespace = 'default'
    salt = 'spz.token.' + namespace
    return Signer(
        app.config['TOKEN_SECRET_KEY'],
        salt=salt,
        signer_kwargs={
            'key_derivation': 'hmac',
            'digest_method': sha256,
        },
    )


def generate(payload, namespace=None):
    """Generates a payload-specific time-based token.

       The return value is sanitized to be used in URLs, e.g. as GET argument.
       The token can be used for multi-time or one-time validation.

       .. warning::
          * Return value partially depends on time. f_t1(m) != f_t2(m).
          * Use the corresponding validate function instead of equality checking.
    """
    signer = get_default_signer(namespace)
    return signer.dumps(payload)


def validate_multi(token, namespace=None, max_age=timedelta(weeks=2).total_seconds()):
    """Validates a payload-specific multi-time-token.

       Additional checking is done for its integrity and expiration, defaulting to one week.
    """
    signer = get_default_signer(namespace)

    # guard against obviously invalid inputs
    if not token:
        return False

    # we're not interested in the exception type (BadSignature, SignatureExpired)
    # see: https://pythonhosted.org/itsdangerous/#responding-to-failure
    # however, payload can be `None` after this call
    _ok, payload_extracted = signer.loads_unsafe(token, max_age=max_age)
    return payload_extracted


def validate_once(
            token,
            payload_wanted,
            db_model,
            db_column,
            max_age=timedelta(weeks=2).total_seconds(),
            namespace=None
        ):
    """Validates a payload-specific one-time-token.

       Additional checking is done for its integrity and expiration, defaulting to one week.
    """
    signer = get_default_signer(namespace)

    # guard against obviously invalid inputs
    if not token:
        return False

    # we're not interested in the exception type (BadSignature, SignatureExpired)
    # see: https://pythonhosted.org/itsdangerous/#responding-to-failure
    # however, payload can be `None` after this call
    ok, payload_extracted = signer.loads_unsafe(token, max_age=max_age)

    # token is only valid if it's associated payload_wanted is not already in the database
    # this way we're able to guarantee the token's one-time property
    # defaults to False if no payload was extracted
    # WARNING: Be careful about the fact that a matching instance might be created during the request/form handling
    #          but wasn't commited to the DB. We do NOT want to match these kind of objects so the following
    #          around: a) use `.all()` instead of `.first()` and set `autoflush` to `False`.
    found = (not payload_extracted) or \
        db_model.query.filter(func.lower(db_column) == func.lower(payload_extracted)).autoflush(False).all()

    # optional case insensitive mail address check, otherwise confusing!
    same = (not payload_wanted) or (payload_extracted and (payload_extracted.lower() == payload_wanted.lower()))

    if ok and same and not found:
        return payload_extracted
    else:
        return None
