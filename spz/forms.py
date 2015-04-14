# -*- coding: utf-8 -*-

"""The application's sign up forms.

   Manages the mapping between database models and HTML forms.
"""

from datetime import datetime

from sqlalchemy import func
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, SelectMultipleField, IntegerField, TextAreaField, BooleanField, validators

from spz import app, models, cache, token


# Cacheable helpers for database fields that are not supposed to change often or quickly
# Do not specify a timeout; so the default one (from the configuration) gets picked up


@cache.cached(key_prefix='degrees')
def degrees_to_choicelist():
    return [(x.id, x.name)
            for x in models.Degree.query.order_by(models.Degree.id.asc())]


@cache.cached(key_prefix='graduations')
def graduations_to_choicelist():
    return [(x.id, x.name)
            for x in models.Graduation.query.order_by(models.Graduation.id.asc())]


@cache.cached(key_prefix='origins')
def origins_to_choicelist():
    return [(x.id, u'{0}'.format(x.name))
            for x in models.Origin.query.order_by(models.Origin.id.asc())]


@cache.cached(key_prefix='languages')
def languages_to_choicelist():
    return [(x.id, u'{0}'.format(x.name))
            for x in models.Language.query.order_by(models.Language.name.asc())]


@cache.cached(key_prefix='upcoming_courses')
def upcoming_courses_to_choicelist():
    available = models.Course.query.join(models.Language.courses) \
                                   .order_by(models.Language.name, models.Course.level, models.Course.alternative)

    upcoming = filter(lambda course: course.language.signup_end >= datetime.utcnow(), available)

    return [(course.id, u'{0} {1}'.format(course.full_name(), u' (Warteliste)' if course.is_full() else u''))
            for course in upcoming]


@cache.cached(key_prefix='all_courses')
def all_courses_to_choicelist():
    courses = models.Course.query.join(models.Language.courses) \
                                 .order_by(models.Language.name, models.Course.level, models.Course.alternative)

    return [(course.id, u'{0}'.format(course.full_name()))
            for course in courses]


class SignupForm(Form):
    """Represents the main sign up form.

       Get's populated with choices from the backend.
       Gathers the user's input and validates it against the provided constraints.

       .. note:: Keep this fully cacheable (i.e. do not query the database for every new form)
    """

    # This should be a BooleanField, because of select-between-two semantics
    sex = SelectField(u'Anrede', [validators.Required(u'Anrede muss angegeben werden')],
                      choices=[(1, u'Herr'), (2, u'Frau')], coerce=int)

    first_name = TextField(u'Vorname', [validators.Length(1, 60, u'Länge muss zwischen 1 und 60 Zeichen sein')])
    last_name = TextField(u'Nachname', [validators.Length(1, 60, u'Länge muss zwischen 1 and 60 sein')])
    phone = TextField(u'Telefon', [validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])
    mail = TextField(u'E-Mail', [validators.Email(u'Valide Mail Adresse wird benötigt'),
                                 validators.Length(max=120, message=u'Länge muss zwischen 1 und 120 Zeichen sein')])
    origin = SelectField(u'Bewerberkreis', [validators.Required(u'Herkunft muss angegeben werden')], coerce=int)

    tag = TextField(u'Matrikelnummer', [validators.Optional(),
                                        validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])

    degree = SelectField(u'Studienabschluss', [validators.Optional()], coerce=int)
    graduation = SelectField(u'Kursabschluss', [validators.Optional()], coerce=int)
    semester = IntegerField(u'Fachsemester', [validators.Optional()])
    course = SelectField(u'Kurse', [validators.Required(u'Kurs muss angegeben werden')], coerce=int)

    # Hack: The form is evaluated only once; but we want the choices to be in sync with the database values
    # see: http://wtforms.simplecodes.com/docs/0.6.1/fields.html#wtforms.fields.SelectField
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self._populate()

    def _populate(self):
        self.degree.choices = degrees_to_choicelist()
        self.graduation.choices = graduations_to_choicelist()
        self.origin.choices = origins_to_choicelist()
        self.course.choices = upcoming_courses_to_choicelist()

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
        return self.tag.data.strip() if self.tag.data and len(self.tag.data.strip()) > 0 else None  # Empty to None

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

        if existing:  # XXX: Return the applicant based on the assumption that the mail _address_ alone is an identidy
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
    mail_reply_to = SelectField('Antwort an', [validators.Required(u'Reply-To muss angegeben werden')], coerce=int)
    only_active = BooleanField('Nur an Aktive')
    only_have_to_pay = BooleanField('Nur an nicht Bezahlte')

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        # See SignupForm for this "trick"
        self.mail_courses.choices = all_courses_to_choicelist()
        self.mail_reply_to.choices = self._reply_to_choices()

    def get_courses(self):
        return models.Course.query.filter(models.Course.id.in_(self.mail_courses.data))

    # TODO: refactor by using the course's get_active_attendances member function
    def get_recipients(self):
        flatten = lambda x: sum(x, [])
        attendances = flatten([course.attendances for course in self.get_courses()])  # single list of attendances

        if self.only_active.data:
            attendances = [att for att in attendances if not att.waiting]

        if self.only_have_to_pay.data:
            attendances = [att for att in attendances if not att.waiting and att.has_to_pay
                           and not att.applicant.discounted and att.amountpaid < att.course.price]

        recipients = [attendance.applicant.mail.encode('utf-8') for attendance in attendances]
        return list(set(recipients))  # One mail per recipient, even if in multiple recipient courses

    def get_body(self):
        return self.mail_body.data.encode('utf-8')

    def get_subject(self):
        return self.mail_subject.data.encode('utf-8')

    @staticmethod
    def _unique_mails_from_str(s):
        return list(set([mail.strip().encode('utf-8') for mail in s.split(',') if '@' in mail]))  # XXX

    def get_cc(self):
        return self._unique_mails_from_str(self.mail_cc.data)

    def get_bcc(self):
        return self._unique_mails_from_str(self.mail_bcc.data)

    def get_reply_to(self):
        return dict(self._reply_to_choices()).get(self.mail_reply_to.data)

    @staticmethod
    def _reply_to_choices():
        # Start index by 1 instead of 0, for the form submitting to be consistent
        return [(idx, mail.encode('utf-8')) for (idx, mail) in enumerate(app.config['REPLY_TO'], 1)]


class ApplicantForm(Form):  # TODO: refactor: lots of code dup. here
    """Represents the form for editing an applicant and his/her attendances.

    """
    applicant = None  # really needed?
    first_name = TextField(u'Vorname', [validators.Length(1, 60, u'Länge muss zwischen 1 und 60 Zeichen sein')])
    last_name = TextField(u'Nachname', [validators.Length(1, 60, u'Länge muss zwischen 1 and 60 sein')])
    phone = TextField(u'Telefon', [validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])
    mail = TextField(u'E-Mail', [validators.Email(u'Valide Mail Adresse wird benötigt'), validators.Length(max=120, message=u'Länge muss zwischen 1 und 120 Zeichen sein')])
    tag = TextField(u'Matrikelnummer', [validators.Optional(), validators.Length(max=20, message=u'Länge darf maximal 20 Zeichen sein')])

    origin = SelectField(u'Bewerberkreis', [validators.Required(u'Bewerberkreis muss angegeben werden')], coerce=int)

    sex = SelectField(u'Anrede', [validators.Required(u'Anrede muss angegeben werden')],
                      choices=[(1, u'Herr'), (2, u'Frau')], coerce=int)
    degree = SelectField(u'Studienabschluss', [validators.Optional()], coerce=int)
    semester = IntegerField(u'Fachsemester', [validators.Optional()])

    add_to = SelectField(u'Teilnahme hinzufügen', [validators.Optional()], coerce=int, choices=[])
    remove_from = SelectField(u'Teilnahme löschen', [validators.Optional()], coerce=int, choices=[])
    send_mail = BooleanField(u'Mail verschicken')

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.origin.choices = origins_to_choicelist()
        self.degree.choices = degrees_to_choicelist()
        self.add_to.choices = all_courses_to_choicelist()
        self.remove_from.choices = all_courses_to_choicelist()

    def populate(self, applicant):
        self.applicant = applicant
        self.first_name.data = self.applicant.first_name
        self.last_name.data = self.applicant.last_name
        self.mail.data = self.applicant.mail
        self.phone.data = self.applicant.phone
        self.tag.data = self.applicant.tag
        self.origin.data = self.applicant.origin_id
        self.sex.data = 1 if self.applicant.sex else 2
        self.degree.data = self.applicant.degree.id if self.applicant.degree else None
        self.semester.data = self.applicant.semester

        in_courses_ids = map(lambda attendance: attendance.course.id, applicant.attendances)
        self.add_to.choices = filter(lambda (idx, _): idx not in in_courses_ids, self.add_to.choices)
        self.remove_from.choices = filter(lambda (idx, _): idx in in_courses_ids, self.remove_from.choices)

    def get_applicant(self):
        return self.applicant

    def get_attendances(self):
        return self.applicant.attendances if self.applicant else None

    def get_add_to(self):
        return models.Course.query.get(self.add_to.data) if self.add_to.data else None

    def get_remove_from(self):
        return models.Course.query.get(self.remove_from.data) if self.remove_from.data else None

    def get_sex(self):
        return True if self.sex.data == 1 else False

    def get_origin(self):
        return models.Origin.query.get(self.origin.data)

    def get_degree(self):
        return models.Degree.query.get(self.degree.data) if self.degree.data else None

    def get_semester(self):
        return self.semester.data if self.semester.data else None

    def get_send_mail(self):
        return self.send_mail.data


class StatusForm(Form):
    """Represents the form for applicants attendances and payments.

    """

    graduation = SelectField(u'Kursabschluss', [validators.Optional()], coerce=int)
    registered = TextField(u'Registrierungsdatum')
    payingdate = TextField(u'Zahlungsdatum')
    waiting = BooleanField(u'Warteliste')
    has_to_pay = BooleanField(u'Zahlungspflichtig')
    discounted = BooleanField(u'Ermäßigt')
    paidbycash = BooleanField(u'Zahlungsart: Bar')
    amountpaid = IntegerField(u'Zahlbetrag', [validators.NumberRange(min=0, message=u'Keine negativen Beträge')])
    notify_change = BooleanField(u'Mail verschicken')

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self._populate()

    def _populate(self):
        self.graduation.choices = graduations_to_choicelist()

    def populate(self, attendance):
        self.graduation.data = attendance.graduation.id if attendance.graduation else None
        self.registered.data = attendance.registered
        self.payingdate.data = attendance.payingdate
        self.waiting.data = attendance.waiting
        self.has_to_pay.data = attendance.has_to_pay
        self.discounted.data = attendance.applicant.discounted
        self.paidbycash.data = attendance.paidbycash
        self.amountpaid.data = attendance.amountpaid

    def get_graduation(self):
        return models.Graduation.query.get(self.graduation.data) if self.graduation.data else None


class PaymentForm(Form):
    """Represents a PaymentForm to input the attendance

    """

    confirmation_code = TextField('Code', [validators.Length(min=4, message=u'Länge muss mindestens 4 Zeichen lang sein')])


class SearchForm(Form):
    """Represents a form to search for specific applicants.
    """

    token = TextField(u'Suchen', [validators.Required(u'Suchparameter muss angegeben werden')])


class LanguageForm(Form):
    """Represents a form for working with courses based on the user's language selection.
    """

    language = SelectField(u'Sprache', [validators.Required(u'Die Sprache muss angegeben werden')], coerce=int)

    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        self._populate()

    def _populate(self):
        self.language.choices = languages_to_choicelist()

    def get_courses(self):
        return models.Language.query.get(self.language.data).courses


class RestockFormFCFS(LanguageForm):
    """Represents a form to fill languages and courses with waiting applicants, respecting their signup timestamp.
       This is the first-come-first-serve policy.
    """
    pass


class RestockFormRnd(Form):
    """Represents a form to fill languages and courses with waiting applicants, using weighted random selection from all attendances.
        This is the weighted-random policy.
    """
    notify_waiting = BooleanField('Mail an Wartende verschicken')


class UniqueForm(LanguageForm):
    """Represents a form to fill languages and courses with waiting applicants.
    """
    pass


class PretermForm(Form):
    """Represents a form to generate a preterm signup token.
    """

    mail = TextField(u'E-Mail', [validators.Email(u'Valide Mail Adresse wird benötigt'),
                                 validators.Length(max=120, message=u'Länge muss zwischen 1 und 120 Zeichen sein')])

    def get_token(self):
        return token.generate(self.mail.data)


# vim: set tabstop=4 shiftwidth=4 expandtab:
