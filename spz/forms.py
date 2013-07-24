# -*- coding: utf-8 -*-

"""The application's sign up forms.

   Manages the mapping between database models and HTML forms.
"""

from flask.ext.wtf import Form
from wtforms import TextField, SelectField, IntegerField, validators

from spz import models, cache


# Cacheable helpers for database fields that are not supposed to change often or quickly
# Do not specify a timeout; so the default one (from the configuration) gets picked up

@cache.cached(key_prefix='degrees')
def degrees_to_choicelist():
    return [(x.id, x.name)
            for x in models.Degree.query.order_by(models.Degree.id.asc()).all()]


@cache.cached(key_prefix='origins')
def origins_to_choicelist():
    return [(x.id, u'{0} {1}'.format(x.name, x.department if x.department else u''))
            for x in models.Origin.query.order_by(models.Origin.id.asc()).all()]


@cache.cached(key_prefix='courses')
def courses_to_choicelist():
    return [(x.id, u'{0} {1}'.format(x.language.name, x.level))
            for x in models.Course.query.order_by(models.Course.id.asc()).all()]


class SignupForm(Form):
    """Represents the main sign up form.

       Get's populated with choices from the backend.
       Gathers the user's input and validates it against the provided constraints.

       .. note:: Keep this fully cacheable (i.e. do not query the database for every new form)
    """

    first_name = TextField('Vorname', [validators.Length(1, 60, 'Länge muss zwischen 1 und 60 Zeichen sein')])
    last_name = TextField('Nachname', [validators.Length(1, 60, 'Länge muss zwischen 1 and 60 sein')])
    phone = TextField('Telefon', [validators.Length(max=20, message='Länge darf maximal 20 Zeichen sein')])
    mail = TextField('E-Mail', [validators.Email('Valide Mail Adresse wird benötigt'),
                                validators.Length(max=120, message='Länge muss zwischen 1 und 120 Zeichen sein')])
    tag = TextField('Identifikation', [validators.DataRequired('Identifikation wird benötigt'),
                                       validators.Length(max=20, message='Länge darf maximal 20 Zeichen sein')])

    degree = SelectField('Angestrebter Abschluss', [validators.Optional()])
    semester = IntegerField('Semester', [validators.Optional()])
    origin = SelectField('Herkunft', [validators.Optional()])
    courses = SelectField('Kurs', [validators.Optional()])

    # Hack: The form is evaluated only once; but we want the choices to be in sync with the database values
    # see: http://wtforms.simplecodes.com/docs/0.6.1/fields.html#wtforms.fields.SelectField
    def __init__(self):
        super(SignupForm, self).__init__()
        self.populate()

    def populate(self):
        self.degree.choices = degrees_to_choicelist()
        self.origin.choices = origins_to_choicelist()
        self.courses.choices = courses_to_choicelist()


# vim: set tabstop=4 shiftwidth=4 expandtab:
