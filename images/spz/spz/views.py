# -*- coding: utf-8 -*-

"""The application's views.

   Manages the mapping between routes and their activities.
"""

import socket
import re
import csv
import io
from datetime import datetime

from redis import ConnectionError

from sqlalchemy import orm, func, not_

from flask import request, redirect, render_template, url_for, flash, make_response
from flask.ext.login import current_user, login_required, login_user, logout_user
from flask.ext.mail import Message

from spz import app, models, db, token
from spz.decorators import templated
from spz.forms import *  # NOQA
from spz.models import Attendance
from spz.util.Filetype import mime_from_filepointer
from spz.util.WeightedRandomGenerator import WeightedRandomGenerator
from spz.async import async_send_slow, async_send_quick, cel


def generate_status_mail(applicant, course, time=None, restock=False):
    """Generate mail to notify applicants about their new attendance status."""
    time = time or datetime.utcnow()
    attendance = Attendance.query \
        .filter(Attendance.applicant_id == applicant.id, Attendance.course_id == course.id) \
        .first()

    if attendance:
        # applicant is (somehow) registered for this course
        if attendance.waiting:
            # applicant is waiting, let's figure out if we are in RND or FCFS phase
            if course.language.is_open_for_signup_rnd(time):
                subject_status = 'Verlosungspool'
                template = 'mails/poolmail.html'
            else:
                subject_status = 'Warteliste'
                template = 'mails/waitinglistmail.html'
        else:
            # :) applicant is signed up for the course
            # let's differ according to the reason (normal procedure or manual restock)
            if restock:
                subject_status = 'Platz durch Nachrückverfahren'
                template = 'mails/restockmail.html'
            else:
                subject_status = 'Erfolgreiche Anmeldung'
                template = 'mails/registeredmail.html'
    else:
        # no registration exists => assuming she got kicked out
        subject_status = 'Platzverlust'
        template = 'mails/kickoutmail.html'

    return Message(
        sender=app.config['PRIMARY_MAIL'],
        reply_to=course.language.reply_to,
        recipients=[applicant.mail],
        subject='[Sprachenzentrum] Kurs {0} - {1}'.format(course.full_name(), subject_status),
        body=render_template(
            template,
            applicant=applicant,
            course=course,
            has_to_pay=attendance.has_to_pay if attendance else False,
            date=datetime.now()
        ),
        charset='utf-8'
    )


def check_precondition_with_auth(cond, msg, auth=False):
    """Check precondition and flash message if not satisfied.

    Returns True (=error) when the condition is not satisfied.

    Condition check can be overwritten when `auth` is True in which case no
    error is returned and only a warning will be shown to the user.
    """
    if not cond:
        if auth:
            flash('{0} (Überschrieben durch Fachleiterzugang!)'.format(msg), 'warning')
            return False
        else:
            flash(msg, 'negative')
            return True
    else:
        return False


@templated('signup.html')
def index():
    form = SignupForm()
    time = datetime.utcnow()

    if current_user.is_authenticated:
        flash('Angemeldet: Vorzeitige Registrierung möglich. Falls unerwünscht, bitte abmelden.', 'success')

    if form.validate_on_submit():
        applicant = form.get_applicant()
        course = form.get_course()
        one_time_token = request.args.get('token', None)
        user_has_special_rights = current_user.is_authenticated and current_user.can_edit_course(course)

        # signup at all times only with token or privileged users
        preterm = applicant.mail and \
            one_time_token and \
            token.validate_once(
                token=one_time_token,
                payload_wanted=applicant.mail,
                namespace='preterm',
                db_model=models.Applicant,
                db_column=models.Applicant.mail
            )
        err = check_precondition_with_auth(
            course.language.is_open_for_signup(time) or preterm,
            'Bitte gedulden Sie sich, die Anmeldung für diese Sprache ist erst möglich in '
            '{0}'.format(course.language.until_signup_fmt()),
            user_has_special_rights
        )
        err |= check_precondition_with_auth(
            course.is_allowed(applicant),
            'Sie haben nicht die vorausgesetzten Sprachtest-Ergebnisse um diesen Kurs zu wählen',
            user_has_special_rights
        )
        err |= check_precondition_with_auth(
            not applicant.in_course(course) and not applicant.active_in_parallel_course(course),
            'Sie sind bereits für diesen Kurs oder einem Parallelkurs angemeldet',
            user_has_special_rights
        )
        err |= check_precondition_with_auth(
            not applicant.over_limit(),
            'Sie haben das Limit an Bewerbungen bereits erreicht',
            user_has_special_rights
        )
        if err:
            return dict(form=form)

        # Run the final insert isolated in a transaction, with rollback semantics
        # As of 2015, we simply put everyone into the waiting list by default and then randomly insert, see #39
        try:
            waiting = not preterm
            applicant.add_course_attendance(
                course,
                form.get_graduation(),
                waiting=waiting,
                has_to_pay=applicant.has_to_pay()
            )

            db.session.add(applicant)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Ihre Kurswahl konnte nicht registriert werden: {0}'.format(e), 'negative')
            return dict(form=form)

        # Preterm signups are in by default and management wants us to send mail immediately
        try:
            async_send_slow.delay(generate_status_mail(applicant, course, time))
        except (AssertionError, socket.error, ConnectionError) as e:
            flash('Eine Bestätigungsmail konnte nicht verschickt werden: {0}'.format(e), 'negative')

        # Finally redirect the user to an confirmation page, too
        return render_template('confirm.html', applicant=applicant, course=course)

    return dict(form=form)


@templated('licenses.html')
def licenses():
    return None


@templated('internal/overview.html')
def internal():
    return None


@login_required
@templated('internal/importer.html')
def importer():
    return None


@login_required
@templated('internal/importer.html')
def registrations():
    if request.method == 'POST':

        fp = request.files['file_name']

        if fp:
            mime = mime_from_filepointer(fp)
            if mime == 'text/plain':
                # strip all known endings ('\r', '\n', '\r\n') and remove empty lines
                # and duplicates
                stripped_lines = (
                    line.decode('utf-8', 'ignore').rstrip('\r').rstrip('\n').rstrip('\r').strip()
                    for line in fp.readlines()
                )
                filtered_lines = (
                    line
                    for line in stripped_lines
                    if line
                )
                unique_registrations = {
                    models.Registration.from_cleartext(line)
                    for line in filtered_lines
                }

                try:
                    num_deleted = models.Registration.query.delete()
                    db.session.add_all(unique_registrations)
                    db.session.commit()
                    flash('Import OK: {0} Einträge gelöscht, {1} Eintrage hinzugefügt'
                          .format(num_deleted, len(unique_registrations)), 'success')
                except Exception as e:
                    db.session.rollback()
                    flash('Konnte Einträge nicht speichern, bitte neu einlesen: {0}'.format(e), 'negative')

                return redirect(url_for('importer'))

            flash('Falscher Dateitype {0}, bitte nur Text oder CSV Dateien verwenden'.format(mime), 'danger')
            return None

    flash('Datei konnte nicht gelesen werden', 'negative')
    return None


@login_required
@templated('internal/importer.html')
def approvals():
    if request.method == 'POST':

        fp = request.files['file_name']

        if fp:
            mime = mime_from_filepointer(fp)
            if mime == 'text/plain':
                try:
                    filecontent = csv.reader(fp, delimiter=';')  # XXX: hardcoded?

                    num_deleted = 0
                    if request.form.getlist("delete_old"):
                        num_deleted = models.Approval.query.delete()

                    approvals = [models.Approval(line[0], int(line[1])) for line in filecontent]
                    db.session.add_all(approvals)
                    db.session.commit()
                    flash('Import OK: {0} Einträge gelöscht, {1} Eintrage hinzugefügt'
                          .format(num_deleted, len(approvals)), 'success')
                except Exception as e:  # csv, index or db could go wrong here..
                    db.session.rollback()
                    flash('Konnte Einträge nicht speichern, bitte neu einlesen: {0}'.format(e), 'negative')

                return redirect(url_for('importer'))

            flash('Falscher Dateitype {0}, bitte nur Text oder CSV Dateien verwenden'.format(mime), 'danger')
            return None

    flash('Datei konnte nicht gelesen werden', 'negative')
    return None


@login_required
@templated('internal/notifications.html')
def notifications():
    form = NotificationForm()

    if form.validate_on_submit():
        try:
            for recipient in form.get_recipients():
                async_send_slow.delay(
                    Message(
                        sender=current_user.email,
                        recipients=[recipient],
                        subject=form.get_subject(),
                        body=form.get_body(),
                        cc=form.get_cc(),
                        bcc=form.get_bcc(),
                        reply_to=form.get_reply_to(),
                        charset='utf-8'
                    )
                )

            flash('Mail erfolgreich verschickt', 'success')
            return redirect(url_for('internal'))

        except (AssertionError, socket.error) as e:
            flash('Mail wurde nicht verschickt: {0}'.format(e), 'negative')

    return dict(form=form)


@login_required
def export_course(course_id):
    course = models.Course.query.get_or_404(course_id)

    active_no_debt = [attendance.applicant for attendance in course.attendances
                      if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]

    buf = io.StringIO()
    out = csv.writer(buf, delimiter=";", dialect=csv.excel)

    # XXX: header -- not standardized
    out.writerow(['Kursplatz', 'Bewerbernummer', 'Vorname', 'Nachname', 'Mail', 'Matrikelnummer',
                  'Telefon', 'Studienabschluss', 'Semester', 'Bewerberkreis'])

    def maybe(x):
        return x if x else ''

    idx = 1
    for applicant in active_no_debt:
        out.writerow(['{0}'.format(idx), '{0}'.format(applicant.id), applicant.first_name,
                      applicant.last_name, applicant.mail, maybe(applicant.tag), maybe(applicant.phone),
                      applicant.degree.name if applicant.degree else '', '{0}'.format(maybe(applicant.semester)),
                      applicant.origin.name if applicant.origin else ''])
        idx += 1

    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = 'attachment; filename="Kursliste {0}.csv"'.format(course.full_name())
    resp.mimetype = 'text/csv'

    return resp


@login_required
def export_language(language_id):
    language = models.Language.query.get_or_404(language_id)

    buf = io.StringIO()
    out = csv.writer(buf, delimiter=";", dialect=csv.excel)

    # XXX: header -- not standardized
    out.writerow(['Kurs', 'Kursplatz', 'Bewerbernummer', 'Vorname', 'Nachname', 'Mail',
                  'Matrikelnummer', 'Telefon', 'Studienabschluss', 'Semester', 'Bewerberkreis'])

    def maybe(x):
        return x if x else ''

    for course in language.courses:
        active_no_debt = [attendance.applicant for attendance in course.attendances
                          if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]

        idx = 1
        for applicant in active_no_debt:
            out.writerow(['{0}'.format(course.full_name()),
                          '{0}'.format(idx),
                          '{0}'.format(applicant.id),
                          applicant.first_name,
                          applicant.last_name,
                          applicant.mail,
                          maybe(applicant.tag),
                          maybe(applicant.phone),
                          applicant.degree.name if applicant.degree else '',
                          '{0}'.format(maybe(applicant.semester)),
                          applicant.origin.name if applicant.origin else ''])
            idx += 1

    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = 'attachment; filename="Kursliste {0}.csv"'.format(language.name)
    resp.mimetype = 'text/csv'

    return resp


@login_required
@templated('internal/lists.html')
def lists():
    # list of tuple (lang, aggregated number of courses, aggregated number of seats)
    lang_misc = db.session.query(models.Language, func.count(models.Language.courses), func.sum(models.Course.limit)) \
        .join(models.Course, models.Language.courses) \
        .group_by(models.Language) \
        .order_by(models.Language.name) \
        .from_self()  # b/c of eager loading, see: http://thread.gmane.org/gmane.comp.python.sqlalchemy.user/36757

    return dict(lang_misc=lang_misc)


@login_required
@templated('internal/language.html')
def language(id):
    return dict(language=models.Language.query.get_or_404(id))


@login_required
@templated('internal/course.html')
def course(id):
    return dict(course=models.Course.query.get_or_404(id))


@login_required
@templated('internal/applicant.html')
def applicant(id):
    applicant = models.Applicant.query.get_or_404(id)
    form = ApplicantForm()

    if form.validate_on_submit():

        try:
            applicant.first_name = form.first_name.data
            applicant.last_name = form.last_name.data
            applicant.phone = form.phone.data
            applicant.mail = form.mail.data
            applicant.tag = form.tag.data
            applicant.origin = form.get_origin()
            applicant.sex = form.get_sex()
            applicant.degree = form.get_degree()
            applicant.semester = form.get_semester()

            db.session.commit()
            flash('Der Bewerber wurde aktualisiert', 'success')

            add_to = form.get_add_to()
            remove_from = form.get_remove_from()
            notify = form.get_send_mail()

            if add_to and remove_from:
                flash(
                    'Bitte im Moment nur entweder eine Teilnahme hinzufügen oder nur eine Teilnahme löschen',
                    'negative'
                )
            elif add_to:
                return add_attendance(applicant_id=applicant.id, course_id=add_to.id, notify=notify)
            elif remove_from:
                return remove_attendance(applicant_id=applicant.id, course_id=remove_from.id, notify=notify)

        except Exception as e:
            db.session.rollback()
            flash('Der Bewerber konnte nicht aktualisiert werden: {0}'.format(e), 'negative')
            return dict(form=form)

    form.populate(applicant)
    return dict(form=form)


@login_required
@templated('internal/applicants/search_applicant.html')
def search_applicant():
    form = SearchForm()

    applicants = []

    if form.validate_on_submit():
        applicants = models.Applicant.query.filter(
            models.Applicant.first_name.like('%{0}%'.format(form.token.data)) |
            models.Applicant.last_name.like('%{0}%'.format(form.token.data)) |
            models.Applicant.mail.like('%{0}%'.format(form.token.data)) |
            models.Applicant.tag.like('%{0}%'.format(form.token.data))
        )

    return dict(form=form, applicants=applicants)


@login_required
def add_attendance(applicant_id, course_id, notify):
    applicant = models.Applicant.query.get_or_404(applicant_id)
    course = models.Course.query.get_or_404(course_id)

    if applicant.in_course(course) or applicant.active_in_parallel_course(course):
        flash('Der Teilnehmer ist bereits im Kurs oder nimmt aktiv an einem Parallelkurs teil', 'negative')
        return redirect(url_for('applicant', id=applicant_id))

    try:
        applicant.add_course_attendance(course, None, False, applicant.has_to_pay())
        db.session.commit()
        flash('Der Teilnehmer wurde in den Kurs eingetragen. Bitte jetzt Status setzen und überprüfen.', 'success')

        if not course.is_allowed(applicant):
            flash(
                'Der Teilnehmer hat eigentlich nicht die entsprechenden Sprachtest-Ergebnisse.'
                'Teilnehmer wurde trotzdem eingetragen.',
                'warning'
            )

    except Exception as e:
        db.session.rollback()
        flash('Der Teilnehmer konnte nicht für den Kurs eingetragen werden: {0}'.format(e), 'negative')
        return redirect(url_for('applicant', id=applicant_id))

    if notify:
        try:
            async_send_slow.delay(generate_status_mail(applicant, course, restock=True))
            flash('Mail erfolgreich verschickt', 'success')
        except (AssertionError, socket.error, ConnectionError) as e:
            flash('Mail konnte nicht verschickt werden: {0}'.format(e), 'negative')

    return redirect(url_for('status', applicant_id=applicant_id, course_id=course_id))


@login_required
def remove_attendance(applicant_id, course_id, notify):
    attendance = models.Attendance.query.get_or_404((applicant_id, course_id))
    applicant = attendance.applicant
    course = attendance.course

    try:
        attendance.applicant.remove_course_attendance(attendance.course)
        db.session.commit()
        flash('Der Bewerber wurde aus dem Kurs genommen', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Der Bewerber konnte nicht aus dem Kurs genommen werden: {0}'.format(e), 'negative')
        return redirect(url_for('applicant', id=applicant_id))

    if notify:
        try:
            async_send_slow.delay(generate_status_mail(applicant, course))
            flash('Mail erfolgreich verschickt', 'success')
        except (AssertionError, socket.error, ConnectionError) as e:
            flash('Mail konnte nicht verschickt werden: {0}'.format(e), 'negative')

    return redirect(url_for('applicant', id=applicant_id))


@login_required
@templated('internal/applicants/applicant_attendances.html')
def applicant_attendances(id):
    return dict(applicant=models.Applicant.query.get_or_404(id))


@login_required
@templated('internal/payments.html')
def payments():
    form = PaymentForm()

    if form.validate_on_submit():
        code = form.confirmation_code.data
        match = re.search(r'^A(?P<a_id>\d{1,})C(?P<c_id>\d{1,})$', code)  # 'A#C#'

        if match:
            a_id, c_id = match.group('a_id', 'c_id')
            return redirect(url_for('status', applicant_id=a_id, course_id=c_id))

        flash('Belegungsnummer ungültig', 'negative')

    stat_list = db.session.query(models.Attendance.paidbycash,
                                 func.sum(models.Attendance.amountpaid),
                                 func.count(),
                                 func.avg(models.Attendance.amountpaid),
                                 func.min(models.Attendance.amountpaid),
                                 func.max(models.Attendance.amountpaid)) \
                          .filter(not_(models.Attendance.waiting), models.Attendance.has_to_pay) \
                          .group_by(models.Attendance.paidbycash)

    desc = ['cash', 'sum', 'count', 'avg', 'min', 'max']
    stats = [dict(list(zip(desc, tup))) for tup in stat_list]

    return dict(form=form, stats=stats)


@login_required
@templated('internal/outstanding.html')
def outstanding():
    # XXX: discounted /2
    outstanding = db.session.query(models.Attendance) \
                            .join(models.Course, models.Applicant) \
                            .filter(not_(models.Attendance.waiting),
                                    not_(models.Applicant.discounted),
                                    models.Attendance.has_to_pay,
                                    models.Attendance.amountpaid < models.Course.price)

    return dict(outstanding=outstanding)


@login_required
@templated('internal/status.html')
def status(applicant_id, course_id):
    attendance = models.Attendance.query.get_or_404((applicant_id, course_id))
    form = StatusForm()

    if form.validate_on_submit():
        try:
            attendance.graduation = form.get_graduation()
            attendance.payingdate = datetime.utcnow()
            attendance.waiting = form.waiting.data
            attendance.has_to_pay = form.has_to_pay.data
            attendance.applicant.discounted = form.discounted.data
            attendance.paidbycash = form.paidbycash.data
            attendance.amountpaid = form.amountpaid.data
            db.session.commit()
            flash('Der Status wurde aktualisiert', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Der Status konnte nicht aktualisiert werden: {0}'.format(e), 'negative')
            return dict(form=form, attendance=attendance)

        if form.notify_change.data:
            try:
                course = attendance.course
                applicant = attendance.applicant
                async_send_quick.delay(generate_status_mail(applicant, course))
                flash('Mail erfolgreich verschickt', 'success')
            except (AssertionError, socket.error, ConnectionError) as e:
                flash('Mail konnte nicht verschickt werden: {0}'.format(e), 'negative')

    form.populate(attendance)
    return dict(form=form, attendance=attendance)


@login_required
@templated('internal/statistics.html')
def statistics():
    return None


@login_required
@templated('internal/statistics/free_courses.html')
def free_courses():
    rv = models.Course.query.join(models.Language.courses) \
                      .order_by(models.Language.name, models.Course.level, models.Course.alternative)

    return dict(courses=rv)


@login_required
@templated('internal/statistics/origins_breakdown.html')
def origins_breakdown():
    rv = db.session.query(models.Origin, func.count()) \
                   .join(models.Applicant, models.Attendance) \
                   .filter(not_(models.Attendance.waiting)) \
                   .group_by(models.Origin) \
                   .order_by(models.Origin.name)

    return dict(origins_breakdown=rv)


@login_required
@templated('internal/statistics/task_queue.html')
def task_queue():
    jobs = []
    try:
        i = cel.control.inspect()
        everything = i.scheduled()
        jobs = everything[next(iter(everything.keys()))]
    except ConnectionError as e:
        flash('Jobabfrage nicht möglich: {0}'.format(e), 'warning')

    tasks = []
    for job in jobs:
        request = job['request']
        payload = '{}({}, {})'.format(request['name'], request['args'], request['kwargs'])

        task = {'id': request['id'], 'started': request['time_start'], 'payload': payload, 'priority': job['priority']}
        tasks.append(task)

    return dict(tasks=tasks)


@login_required
@templated('internal/preterm.html')
def preterm():
    form = PretermForm()

    token = None

    if form.validate_on_submit():
        token = form.get_token()

        try:
            async_send_quick.delay(
                Message(
                    sender=app.config['PRIMARY_MAIL'],
                    recipients=[form.mail.data],
                    subject='[Sprachenzentrum] URL für prioritäre Anmeldung',
                    body='{0}'.format(url_for('index', token=token, _external=True)),
                    charset='utf-8'
                )
            )

            flash('Eine Mail mit der Token URL wurde an {0} verschickt'.format(form.mail.data), 'success')

        except (AssertionError, socket.error) as e:
            flash('Eine Bestätigungsmail konnte nicht verschickt werden: {0}'.format(e), 'negative')

    # always show preterm signups in this view
    attendances = models.Attendance.query \
                        .join(models.Course, models.Language, models.Applicant) \
                        .filter(models.Attendance.registered < models.Language.signup_begin) \
                        .order_by(models.Applicant.last_name, models.Applicant.first_name)

    return dict(form=form, token=token, preterm_signups=attendances)


@login_required
@templated('internal/duplicates.html')
def duplicates():
    taglist = db.session.query(models.Applicant.tag) \
        .filter(models.Applicant.tag is not None, models.Applicant.tag != '') \
        .group_by(models.Applicant.tag) \
        .having(func.count(models.Applicant.id) > 1)

    doppelganger = [models.Applicant.query.filter_by(tag=duptag) for duptag in [tup[0] for tup in taglist]]

    return dict(doppelganger=doppelganger)


# This is the first-come-first-served policy view
@login_required
@templated('internal/restock_fcfs.html')
def restock_fcfs():
    form = RestockFormFCFS()

    if form.validate_on_submit():
        courses = form.get_courses()
        restocked_attendances = []

        try:
            for course in courses:
                restocked_attendances.extend(course.restock())

            db.session.commit()
            flash('Kurse bestmöglichst mit Nachrückern gefüllt', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Die Kurse konnten nicht mit Nachrückern gefüllt werden: {0}'.format(e), 'negative')
            return redirect(url_for('restock_fcfs'))

        if len(restocked_attendances) == 0:
            flash(
                'Die Kurse konnten nicht mit Nachrückern gefüllt werden, da keine freien Plätze mehr vorhanden sind',
                'negative'
            )
            return redirect(url_for('restock_fcfs'))

        try:
            for attendance in restocked_attendances:
                async_send_slow.delay(
                    generate_status_mail(attendance.applicant, attendance.course)
                )

            flash('Mails erfolgreich verschickt', 'success')
            return redirect(url_for('internal'))

        except (AssertionError, socket.error) as e:
            flash('Mails konnten nicht verschickt werden: {0}'.format(e), 'negative')

    return dict(form=form)


# This is the weighted-random-selection policy view
@login_required
@templated('internal/restock_rnd.html')
def restock_rnd():
    form = RestockFormRnd()

    if form.validate_on_submit():
        # eager loading, see (search for 'subqueryload'):
        # http://docs.sqlalchemy.org/en/rel_0_9/orm/loading_relationships.html
        to_assign = models.Attendance.query \
            .options(orm.subqueryload(models.Attendance.applicant).subqueryload(models.Applicant.attendances)) \
            .filter_by(waiting=True) \
            .all()

        # Interval filtering in Python instead of SQL because it's not portable (across SQLite, Postgres, ..)
        # implementable in standard SQL
        # See: https://groups.google.com/forum/#!msg/sqlalchemy/AneqcriykeI/j4sayzZP1qQJ
        w_open = app.config['RANDOM_WINDOW_OPEN_FOR']

        def between(x, lhs, rhs):
            return lhs < x < rhs

        to_assign = [
            att
            for att
            in to_assign
            if between(att.registered, att.course.language.signup_begin, att.course.language.signup_begin + w_open)
        ]

        # (attendance, weight) tuples from query would be possible, too;
        # eager loading already takes care of not issuing tons of sql queries here
        now = datetime.utcnow()
        weights = [
            1.0 / max(
                1.0,
                len([
                    att
                    for att
                    in attendance.applicant.attendances
                    if att.course.language.signup_end >= now
                ])
            )
            for attendance
            in to_assign
        ]

        # keep track of which attendances we set to active/waiting
        handled_attendances = []

        stats = {'filled': 0, 'paying': 0, 'all': len(to_assign)}

        while to_assign:
            assert len(to_assign) == len(weights)

            # weighted random selection
            gen = WeightedRandomGenerator(weights)
            idx = next(gen)

            # remove attendance and weight from possible candidates as to not select again;  guarantees termination
            attendance = to_assign.pop(idx)
            del weights[idx]

            if attendance.applicant.active_in_parallel_course(attendance.course):
                continue

            # keep default waiting status
            if len(attendance.course.get_active_attendances()) >= attendance.course.limit:
                if form.notify_waiting.data:
                    handled_attendances.append(attendance)
                continue

            attendance.has_to_pay = attendance.applicant.has_to_pay()
            attendance.waiting = False
            handled_attendances.append(attendance)

        try:
            db.session.commit()
            flash('{0} Teilnahmen (von {1} Wartenden) konnten aktiviert werden. Davon sind zu zahlen: {2}.'
                  .format(sum([1 for a in handled_attendances if not a.waiting]), stats['all'],
                          sum([1 for a in handled_attendances if a.has_to_pay])), 'success')
        except Exception as e:
            db.session.rollback()
            flash(
                'Das Füllen des Systems mit Teilnahmen nach dem Zufallsprinzip konnte nicht durchgeführt werden: '
                '{0}'.format(e),
                'negative'
            )
            return redirect(url_for('restock_rnd'))

        # Send mails (async) only if the commit was successfull -- be conservative here
        try:
            for attendance in handled_attendances:
                async_send_slow.delay(generate_status_mail(attendance.applicant, attendance.course))

            if handled_attendances:  # only show if there are attendances that we handled
                flash('Mails erfolgreich verschickt', 'success')
        except (AssertionError, socket.error, ConnectionError) as e:
            flash('Mails wurden nicht verschickt: {0}'.format(e), 'negative')

    return dict(form=form)


@login_required
@templated('internal/unique.html')
def unique():
    form = UniqueForm()

    if form.validate_on_submit():
        courses = form.get_courses()
        deleted = 0

        try:
            waiting_but_active_parallel = [
                attendance
                for course
                in courses
                for attendance
                in course.get_waiting_attendances()
                if attendance.applicant.active_in_parallel_course(course)
            ]

            for attendance in waiting_but_active_parallel:
                db.session.delete(attendance)
                deleted += 1

            db.session.commit()
            flash('Kurse von {0} wartenden Teilnahmen mit aktiven Parallelkurs bereinigt'.format(deleted), 'success')
        except Exception as e:
            db.session.rollback()
            flash(
                'Die Kurse konnten nicht von wartenden Teilnahmen mit aktiven Parallelkurs bereinigt werden: '
                '{0}'.format(e),
                'negative'
            )
            return redirect(url_for('unique'))

    return dict(form=form)


@templated('internal/login.html')
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = models.User.get_by_login(form.user.data, form.password.data)
        if user:
            login_user(user)
            return redirect(url_for('internal'))
        flash('Du kommst hier net rein!', 'negative')

    return dict(form=form)


def logout():
    logout_user()
    flash('Tschau!', 'success')
    return redirect(url_for('login'))
