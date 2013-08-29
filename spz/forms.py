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
    return [(unicode(x.id), x.name)
            for x in models.Degree.query.order_by(models.Degree.id.asc()).all()]


@cache.cached(key_prefix='origins')
def origins_to_choicelist():
    return [(unicode(x.id), u'{0} {1}'.format(x.name, x.department if x.department else u''))
            for x in models.Origin.query.order_by(models.Origin.id.asc()).all()]


@cache.cached(key_prefix='languages')
def languages_to_choicelist():
    return [(unicode(x.id), x.name)
            for x in models.Language.query.order_by(models.Language.id.asc()).all()]


@cache.cached(key_prefix='courses')
def courses_to_choicelist():
    return [(unicode(x.id), u'{0} {1}'.format(x.language.name, x.level))
            for x in models.Course.query.order_by(models.Course.id.asc()).all()]


class SignupForm(Form):
    """Represents the main sign up form.

       Get's populated with choices from the backend.
       Gathers the user's input and validates it against the provided constraints.

       .. note:: Keep this fully cacheable (i.e. do not query the database for every new form)
    """

    first_name = TextField(u'Vorname', [validators.Length(1, 60, u'Länge muss zwischen 1 und 60 Zeichen sein')])
    last_name = TextField(u'Nachname', [validators.Length(1, 60, u'Länge muss zwischen 1 and 60 sein')])
    phone = TextField(u'Telefon', [validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])
    mail = TextField(u'E-Mail', [validators.Email(u'Valide Mail Adresse wird benötigt'),
                                validators.Length(max=120, message=u'Länge muss zwischen 1 und 120 Zeichen sein')])
    tag = TextField(u'Identifikation', [validators.Required(u'Identifikation wird benötigt'),
                                       validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])

    degree = SelectField(u'Angestrebter Abschluss', [validators.Optional()])
    semester = IntegerField(u'Semester', [validators.Optional()])
    origin = SelectField(u'Herkunft', [validators.Required(u'Herkunft muss angegeben werden')])
    languages = SelectField(u'Sprache', [validators.Optional()])  # only used for filtering on the frontend
    courses = SelectField(u'Kurs', [validators.Required(u'Kurs muss angegeben werden')])

    # Hack: The form is evaluated only once; but we want the choices to be in sync with the database values
    # see: http://wtforms.simplecodes.com/docs/0.6.1/fields.html#wtforms.fields.SelectField
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.populate()

    def populate(self):
        self.degree.choices = degrees_to_choicelist()
        self.origin.choices = origins_to_choicelist()
        self.languages.choices = languages_to_choicelist()
        self.courses.choices = courses_to_choicelist()


# vim: set tabstop=4 shiftwidth=4 expandtab: