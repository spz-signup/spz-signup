# -*- coding: utf-8 -*-

"""Validators used for different forms."""

import phonenumbers

from wtforms.validators import *  # NOQA
from wtforms.validators import ValidationError

from spz import models


class TagDependingOnOrigin(object):
    """Helper validator if origin requires validatation of registration."""

    def __call__(self, form, field):
        o = form.get_origin()
        if o and o.validate_registration and not models.Registration.exists(field.data):
            raise ValidationError('Ungültige Matrikelnummer')


class RequiredDependingOnOrigin(Required):  # NOQA
    """Helper validator if origin requires validatation of registration."""

    def __init__(self, *args, **kwargs):
        super(RequiredDependingOnOrigin, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        o = form.get_origin()
        if o and o.validate_registration:
            super(RequiredDependingOnOrigin, self).__call__(form, field)


class PhoneValidator(object):
    """Validates phone numbers."""

    def __call__(self, form, field):
        valid = True
        try:
            x = phonenumbers.parse(field.data, 'DE')
            if not phonenumbers.is_valid_number(x):
                valid = False
        except Exception:
            # XXX: by more specific about exception
            valid = False

        if not valid:
            raise ValidationError('Ungültige Telefonnummer')
