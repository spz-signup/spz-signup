# -*- coding: utf-8 -*-

"""The application's sign up forms.

   Manages the mapping between database models and HTML forms.
"""

from flask.ext.wtf import Form
from wtforms import TextField, validators


# Note: It's possible to generate the form from the model.
#       For now we do it manually because of customizations.
#
# from wtforms.ext.sqlalchemy.orm import model_form
# MyForm = model_form(Applicant, Form)


class SignupForm(Form):
    first_name = TextField('Vorname', [validators.Length(1, 60, 'Länge muss zwischen 1 und 60 Zeichen sein')])
    last_name = TextField('Nachname', [validators.Length(1, 60, 'Länge muss zwischen 1 and 60 sein')])
    phone = TextField('Telephon', [validators.Length(max=20, message='Länge darf maximal 20 Zeichen sein')])
    mail = TextField('Mail', [validators.Email('Valide Mail Adresse wird benötigt'),
                              validators.Length(max=120, message='Länge muss zwischen 1 und 120 Zeichen sein')])
    tag = TextField('Identifikation', [validators.DataRequired('Identifikation wird benötigt'),
                                       validators.Length(max=20, message='Länge darf maximal 20 Zeichen sein')])

    # course



# vim: set tabstop=4 shiftwidth=4 expandtab:
