# -*- coding: utf-8 -*-

"""The application's sign up forms.

   Manages the mapping between database models and HTML forms.
"""

from flask.ext.wtf import Form
from wtforms import TextField, validators


class SignupForm(Form):
    first_name = TextField('First name', [validators.Length(1, 60, 'Length has to be between 1 and 60')])
    last_name = TextField('Last name', [validators.Length(1, 60, 'Length has to be between 1 and 60')])
    phone = TextField('Phone', [validators.Length(max=20, message='Length max. is 20')])
    mail = TextField('Mail', [validators.Email('Valid mail is required'),
                              validators.Length(max=120, message='Length has to be between 1 and 120')])
    tag = TextField('Identification', [validators.DataRequired('Identification is required')])

    # course


# vim: set tabstop=4 shiftwidth=4 expandtab:
