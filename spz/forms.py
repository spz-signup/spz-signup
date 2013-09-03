# -*- coding: utf-8 -*-

"""The application's sign up forms.

   Manages the mapping between database models and HTML forms.
"""

from flask.ext.wtf import Form
from wtforms import TextField, SelectField, IntegerField, TextField, TextAreaField, validators

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


@cache.cached(key_prefix='coursegroups')
def coursegroups_to_choicelist():
    # List of (language, [courses for this language]) tuples, i.e. [(lang, [(cid, cname), (cid, cname)]), (lang, [(cid, cname)]), ...]
    return [(u'{0}'.format(lang.name), [(course.id, u'{0} {1}'.format(lang.name, course.level)) for course in lang.courses.all()])
            for lang in models.Language.query.order_by(models.Language.id.asc()).all()]


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

    degree = SelectField(u'Angestrebter Abschluss', [validators.Optional()], coerce=int)
    semester = IntegerField(u'Semester', [validators.Optional()])
    origin = SelectField(u'Herkunft', [validators.Required(u'Herkunft muss angegeben werden')], coerce=int)
    coursegroups = SelectField(u'Kurse', [validators.Required(u'Kurs muss angegeben werden')], coerce=int)

    # Hack: The form is evaluated only once; but we want the choices to be in sync with the database values
    # see: http://wtforms.simplecodes.com/docs/0.6.1/fields.html#wtforms.fields.SelectField
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.populate()

    def populate(self):
        self.degree.choices = degrees_to_choicelist()
        self.origin.choices = origins_to_choicelist()
        self.coursegroups.choices = coursegroups_to_choicelist()


class NotificationForm(Form):
    """Represents the form for sending notifications.

       The field's length are limited on purpose.
    """

    mail_subject = TextField('Betreff', [validators.Length(1, 200, u'Betreff muss zwischen 1 und 200 Zeichen enthalten')])
    mail_body = TextAreaField('Nachricht', [validators.Length(1, 2000, u'Nachricht muss zwischen 1 und 2000 Zeichen enthalten')])


# vim: set tabstop=4 shiftwidth=4 expandtab:
