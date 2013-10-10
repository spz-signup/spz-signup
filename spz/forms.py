# -*- coding: utf-8 -*-

"""The application's sign up forms.

   Manages the mapping between database models and HTML forms.
"""

from sqlalchemy import func
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, SelectMultipleField, IntegerField, TextAreaField, validators

from spz import models, cache


# Cacheable helpers for database fields that are not supposed to change often or quickly
# Do not specify a timeout; so the default one (from the configuration) gets picked up


@cache.cached(key_prefix='degrees')
def degrees_to_choicelist():
    return [(x.id, x.name)
            for x in models.Degree.query.order_by(models.Degree.id.asc()).all()]


@cache.cached(key_prefix='graduations')
def graduations_to_choicelist():
    return [(x.id, x.name)
            for x in models.Graduation.query.order_by(models.Graduation.id.asc()).all()]


@cache.cached(key_prefix='origins')
def origins_to_choicelist():
    return [(x.id, u'{0}'.format(x.name))
            for x in models.Origin.query.order_by(models.Origin.id.asc()).all()]


@cache.cached(key_prefix='course')
def course_to_choicelist():
    return [(course.id, u'{0} {1}{2}'.format(course.language.name, course.level, u' (voll)' if course.is_full() else u''))
            for course in models.Course.query.order_by(models.Course.id.asc()).all()]


class SignupForm(Form):
    """Represents the main sign up form.

       Get's populated with choices from the backend.
       Gathers the user's input and validates it against the provided constraints.

       .. note:: Keep this fully cacheable (i.e. do not query the database for every new form)
    """

    # This should be a BooleanField, because of select-between-two semantics
    sex = SelectField(u'Anrede', [validators.Required(u'Anrede muss angegeben werden')], choices=[(1, u'Herr'), (2, u'Frau')], coerce=int)

    first_name = TextField(u'Vorname', [validators.Length(1, 60, u'Länge muss zwischen 1 und 60 Zeichen sein')])
    last_name = TextField(u'Nachname', [validators.Length(1, 60, u'Länge muss zwischen 1 and 60 sein')])
    phone = TextField(u'Telefon', [validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])
    mail = TextField(u'E-Mail', [validators.Email(u'Valide Mail Adresse wird benötigt'),
                                 validators.Length(max=120, message=u'Länge muss zwischen 1 und 120 Zeichen sein')])
    origin = SelectField(u'Herkunft', [validators.Required(u'Herkunft muss angegeben werden')], coerce=int)

    tag = TextField(u'Identifikation', [validators.Optional(),
                                        validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])

    degree = SelectField(u'Studiengang', [validators.Optional()], coerce=int)
    graduation = SelectField(u'Angestrebter Kursabschluss', [validators.Optional()], coerce=int)
    semester = IntegerField(u'Fachsemester', [validators.Optional()])
    course = SelectField(u'Kurse', [validators.Required(u'Kurs muss angegeben werden')], coerce=int)

    # Hack: The form is evaluated only once; but we want the choices to be in sync with the database values
    # see: http://wtforms.simplecodes.com/docs/0.6.1/fields.html#wtforms.fields.SelectField
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.populate()

    def populate(self):
        self.degree.choices = degrees_to_choicelist()
        self.graduation.choices = graduations_to_choicelist()
        self.origin.choices = origins_to_choicelist()
        self.course.choices = course_to_choicelist()

    # Accessors, to encapsulate the way the form represents and retrieves objects
    # This especially ensures that optional fields only get queried if a value is present

    def get_sex(self):
        return True if self.sex.data == 1 else False

    def get_first_name(self):
        return self.first_name.data

    def get_last_name(self):
        return self.last_name.data

    def get_phone(self):
        return self.phone.data

    def get_mail(self):
        return self.mail.data

    def get_origin(self):
        return models.Origin.query.get(self.origin.data)

    def get_tag(self):
        return self.tag.data.strip() if self.tag.data and len(self.tag.data.strip()) > 0 else None  # Empty String to None

    def get_degree(self):
        return models.Degree.query.get(self.degree.data) if self.degree.data else None

    def get_graduation(self):
        return models.Graduation.query.get(self.graduation.data) if self.graduation.data else None

    def get_semester(self):
        return self.semester.data if self.semester.data else None

    def get_course(self):
        return models.Course.query.get(self.course.data)

    # Creates an applicant or returns it from the system, if already registered.
    def get_applicant(self):
        existing = models.Applicant.query.filter(func.lower(models.Applicant.mail) == func.lower(self.get_mail())).first()

        if existing:  # XXX
            return existing

        return models.Applicant(self.get_mail(), self.get_tag(), self.get_sex(),
                                self.get_first_name(), self.get_last_name(),
                                self.get_phone(), self.get_degree(),
                                self.get_semester(), self.get_origin())


class NotificationForm(Form):
    """Represents the form for sending notifications.

       The field's length are limited on purpose.
    """

    mail_subject = TextField('Betreff', [validators.Length(1, 200, u'Betreff muss zwischen 1 und 200 Zeichen enthalten')])
    mail_body = TextAreaField('Nachricht', [validators.Length(1, 2000, u'Nachricht muss zwischen 1 und 2000 Zeichen enthalten')])
    mail_cc = TextField('CC', [validators.Optional()])
    mail_bcc = TextField('BCC', [validators.Optional()])
    mail_courses = SelectMultipleField(u'Kurse', [validators.Required(u'Kurs muss angegeben werden')], coerce=int)

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.mail_courses.choices = course_to_choicelist()  # See SignupForm for this "trick"

    def get_courses(self):
        return models.Course.query.filter(models.Course.id.in_(self.mail_courses.data)).all()

    def get_recipients(self):
        attendances = [course.applicant_attendances for course in self.get_courses()]
        merged = sum(attendances, [])  # merge list of attendances per course [[], [], ..] into one list
        recipients = [attendance.applicant.mail for attendance in merged if not attendance.waiting]

        return recipients


class ApplicantForm(Form): #TODO mail, phone
    """Represents the form for editing an applicant and his/her attendances.

    """
    applicant = None
    first_name = TextField(u'Vorname', [validators.Length(1, 60, u'Länge muss zwischen 1 und 60 Zeichen sein')])
    last_name = TextField(u'Nachname', [validators.Length(1, 60, u'Länge muss zwischen 1 and 60 sein')])
    phone = TextField(u'Telefon', [validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])
    mail = TextField(u'E-Mail', [validators.Email(u'Valide Mail Adresse wird benötigt'), validators.Length(max=120, message=u'Länge muss zwischen 1 und 120 Zeichen sein')])
    tag = TextField(u'Identifikation', [validators.Optional(), validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])

    origin = SelectField(u'Herkunft', [validators.Required(u'Herkunft muss angegeben werden')], coerce=int)

    semester = IntegerField(u'Fachsemester', [validators.Optional()])

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.origin.choices = origins_to_choicelist()

    def populate(self, applicant):
        self.applicant = applicant
        self.first_name.data = self.applicant.first_name
        self.last_name.data = self.applicant.last_name
        self.mail.data = self.applicant.mail
        self.phone.data = self.applicant.phone
        self.tag.data = self.applicant.tag
        self.origin.data = self.applicant.origin_id

    def get_applicant(self):
        return self.applicant

    def get_courses(self):
        return self.applicant.course if self.applicant else None



# vim: set tabstop=4 shiftwidth=4 expandtab:
