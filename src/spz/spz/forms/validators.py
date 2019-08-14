# -*- coding: utf-8 -*-

"""Validators used for different forms."""

import dns
import email_validator
import phonenumbers

from wtforms.validators import *  # NOQA
from wtforms.validators import ValidationError

from spz import models
from spz.util.Filetype import size_from_filepointer


# set LRU cache for DNS caching
# TODO: use flask cache instead (LRU + timeout)
dns.resolver.get_default_resolver().cache = dns.resolver.LRUCache()


class EmailPlusValidator(object):
    """Validates mail addresses including DNS check."""

    def __call__(self, form, field):
        try:
            email_validator.validate_email(field.data)
        except email_validator.EmailNotValidError:
            raise ValidationError('Ungültige E-Mail Adresse')


class MultiFilesFileSizeValidator(object):
    """Validates that file does not exceed certain size."""

    def __init__(self, smin, smax):
        self.smin = smin
        self.smax = smax

    def __call__(self, form, field):
        if field.data:
            sum = 0
            for fld in field.data:
                s = size_from_filepointer(fld)
                sum += s
                if s < self.smin:
                    raise ValidationError('Eine Datei ist zu klein')
                if sum > self.smax:
                    raise ValidationError('Dateien sind zu groß')


class FileSizeValidator(object):
    """Validates that file does not exceed certain size."""

    def __init__(self, smin, smax):
        self.smin = smin
        self.smax = smax

    def __call__(self, form, field):
        if field.data:
            s = size_from_filepointer(field.data)
            if s < self.smin:
                raise ValidationError('Datei ist zu klein')
            if s > self.smax:
                raise ValidationError('Datei ist zu groß')


class TagDependingOnOrigin(object):
    """Helper validator if origin requires validatation of registration."""

    def __call__(self, form, field):
        o = form.get_origin()
        if o and o.validate_registration and not models.Registration.exists(field.data):
            raise ValidationError('Ungültige Matrikelnummer')


class RequiredDependingOnOrigin(DataRequired):  # NOQA
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
