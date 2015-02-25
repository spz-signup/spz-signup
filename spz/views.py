# -*- coding: utf-8 -*-

"""The application's views.

   Manages the mapping between routes and their activities.
"""

import socket
import re
import csv
import StringIO
from datetime import datetime, timedelta

from redis import ConnectionError

from sqlalchemy import orm, func, not_

from flask import request, redirect, render_template, url_for, flash, g, make_response
from flask.ext.mail import Message

from spz import app, models, mail, db, token
from spz.decorators import templated, auth_required
from spz.forms import SignupForm, NotificationForm, ApplicantForm, StatusForm, PaymentForm, SearchForm, RestockFormFCFS, RestockFormRnd, PretermForm, UniqueForm
from spz.util.Encoding import UnicodeWriter
from spz.util.WeightedRandomGenerator import WeightedRandomGenerator
from spz.async import queue, async_send


@templated('signup.html')
def index():
    form = SignupForm()

    if g.access:
        flash(u'Angemeldet: Vorzeitige Registrierung möglich. Falls unerwünscht, bitte abmelden.', 'success')

    if form.validate_on_submit():
        applicant = form.get_applicant()
        course = form.get_course()
        one_time_token = request.args.get('token', None)

        # signup at all times only with token or privileged users
        if not course.language.is_open_for_signup() and not token.validate(one_time_token, applicant.mail) and not g.access:
            flash(u'Bitte gedulden Sie sich, die Anmeldung für diese Sprache ist erst möglich in {0}'.format(course.language.until_signup_fmt()), 'danger')
            return dict(form=form)

        if not course.is_allowed(applicant):
            flash(u'Sie haben nicht die vorausgesetzten Sprachtest-Ergebnisse um diesen Kurs zu wählen', 'danger')
            return dict(form=form)

        if applicant.in_course(course) or applicant.active_in_parallel_course(course):
            flash(u'Sie sind bereits im Kurs oder nehmen aktiv an einem Parallelkurs teil', 'danger')
            return dict(form=form)

        # Run the final insert isolated in a transaction, with rollback semantics
        # As of 2015, we simply put everyone into the waiting list by default and then randomly insert, see #39
        try:
            applicant.add_course_attendance(course, form.get_graduation(),
                                            waiting=True, has_to_pay=False)

            db.session.add(applicant)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(u'Ihre Kurswahl konnte nicht registriert werden: {0}'.format(e), 'danger')
            return dict(form=form)

        # Finally redirect the user to an confirmation page, too
        return render_template('confirm.html', applicant=applicant, course=course)

    return dict(form=form)


@templated('licenses.html')
def licenses():
    return None


@templated('internal/overview.html')
def internal():
    return None


@auth_required
@templated('internal/importer.html')
def importer():
    return None


@auth_required
@templated('internal/importer.html')
def registrations():
    if request.method == 'POST':

        fp = request.files['file_name']

        if fp:
            unique_registrations = {models.Registration(line.rstrip('\r\n')) for line in fp}

            try:
                num_deleted = models.Registration.query.delete()
                db.session.add_all(unique_registrations)
                db.session.commit()
                flash(u'Import OK: {0} Einträge gelöscht, {1} Eintrage hinzugefügt'
                      .format(num_deleted, len(unique_registrations)), 'success')
            except Exception as e:
                db.session.rollback()
                flash(u'Konnte Einträge nicht speichern, bitte neu einlesen: {0}'.format(e), 'danger')

            return redirect(url_for('importer'))

    flash(u'Datei konnte nicht gelesen werden', 'danger')
    return None


@auth_required
@templated('internal/importer.html')
def approvals():
    if request.method == 'POST':

        fp = request.files['file_name']

        if fp:
            try:
                filecontent = csv.reader(fp, delimiter=';')  # XXX: hardcoded?

                num_deleted = 0
                if request.form.getlist("delete_old"):  # XXX: hardcoded?. Write a form!
                    num_deleted = models.Approval.query.delete()

                approvals = [models.Approval(line[0], int(line[1])) for line in filecontent]
                db.session.add_all(approvals)
                db.session.commit()
                flash(u'Import OK: {0} Einträge gelöscht, {1} Eintrage hinzugefügt'
                      .format(num_deleted, len(approvals)), 'success')
            except Exception as e:  # csv, index or db could go wrong here..
                db.session.rollback()
                flash(u'Konnte Einträge nicht speichern, bitte neu einlesen: {0}'.format(e), 'danger')

            return redirect(url_for('importer'))

    flash(u'Datei konnte nicht gelesen werden', 'danger')
    return None


@auth_required
@templated('internal/notifications.html')
def notifications():
    form = NotificationForm()

    if form.validate_on_submit():
        try:
            with mail.connect() as conn:
                for recipient in form.get_recipients():
                    msg = Message(sender=g.user, recipients=[recipient], subject=form.get_subject(),
                                  body=form.get_body(), cc=form.get_cc(), bcc=form.get_bcc(), reply_to=form.get_reply_to())

                    conn.send(msg)

            flash(u'Mail erfolgreich verschickt', 'success')
            return redirect(url_for('internal'))

        except (AssertionError, socket.error) as e:
            flash(u'Mail wurde nicht verschickt: {0}'.format(e), 'danger')

    return dict(form=form)


@auth_required
def export_course(course_id):
    course = models.Course.query.get_or_404(course_id)

    active_no_debt = [attendance.applicant for attendance in course.attendances
                      if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]

    buf = StringIO.StringIO()
    out = UnicodeWriter(buf, delimiter=';')

    # XXX: header -- not standardized
    out.writerow([u'Kursplatz', u'Bewerbernummer', u'Vorname', u'Nachname', u'Mail', u'Matrikelnummer',
                  u'Telefon', u'Studienabschluss', u'Semester', u'Bewerberkreis'])

    maybe = lambda x: x if x else u''

    idx = 1
    for applicant in active_no_debt:
        out.writerow([u'{0}'.format(idx), u'{0}'.format(applicant.id), applicant.first_name,
                      applicant.last_name, applicant.mail, maybe(applicant.tag), maybe(applicant.phone),
                      applicant.degree.name if applicant.degree else u'', u'{0}'.format(maybe(applicant.semester)),
                      applicant.origin.name if applicant.origin else u''])
        idx += 1

    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="Kursliste {0}.csv"'.format(course.full_name())
    resp.mimetype = 'text/csv'

    return resp


@auth_required
def export_language(language_id):
    language = models.Language.query.get_or_404(language_id)

    buf = StringIO.StringIO()
    out = UnicodeWriter(buf, delimiter=';')

    # XXX: header -- not standardized
    out.writerow([u'Kurs', u'Kursplatz', u'Bewerbernummer', u'Vorname', u'Nachname', u'Mail',
                  u'Matrikelnummer', u'Telefon', u'Studienabschluss', u'Semester', u'Bewerberkreis'])

    maybe = lambda x: x if x else u''

    for course in language.courses:
        active_no_debt = [attendance.applicant for attendance in course.attendances
                          if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]

        idx = 1
        for applicant in active_no_debt:
            out.writerow([u'{0}'.format(course.full_name()),
                          u'{0}'.format(idx),
                          u'{0}'.format(applicant.id),
                          applicant.first_name,
                          applicant.last_name,
                          applicant.mail,
                          maybe(applicant.tag),
                          maybe(applicant.phone),
                          applicant.degree.name if applicant.degree else u'',
                          u'{0}'.format(maybe(applicant.semester)),
                          applicant.origin.name if applicant.origin else u''])
            idx += 1

    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="Kursliste {0}.csv"'.format(language.name)
    resp.mimetype = 'text/csv'

    return resp


@auth_required
@templated('internal/lists.html')
def lists():
    # list of tuple (lang, aggregated number of courses, aggregated number of seats)
    lang_misc = db.session.query(models.Language, func.count(models.Language.courses), func.sum(models.Course.limit)) \
                          .join(models.Course, models.Language.courses) \
                          .group_by(models.Language) \
                          .order_by(models.Language.name) \
                          .from_self()  # b/c of eager loading, see: http://thread.gmane.org/gmane.comp.python.sqlalchemy.user/36757

    return dict(lang_misc=lang_misc)


@auth_required
@templated('internal/language.html')
def language(id):
    return dict(language=models.Language.query.get_or_404(id))


@auth_required
@templated('internal/course.html')
def course(id):
    return dict(course=models.Course.query.get_or_404(id))


@auth_required
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
            flash(u'Der Bewerber wurde aktualisiert', 'success')

            add_to = form.get_add_to()
            remove_from = form.get_remove_from()

            if add_to and remove_from:
                flash(u'Bitte im Moment nur entweder eine Teilnahme hinzufügen oder nur eine Teilnahme löschen', 'danger')
            elif add_to:
                return redirect(url_for('add_attendance', applicant_id=applicant.id, course_id=add_to.id))
            elif remove_from:
                return redirect(url_for('remove_attendance', applicant_id=applicant.id, course_id=remove_from.id))

        except Exception as e:
            db.session.rollback()
            flash(u'Der Bewerber konnte nicht aktualisiert werden: {0}'.format(e), 'danger')
            return dict(form=form)

    form.populate(applicant)
    return dict(form=form)


@auth_required
@templated('internal/applicants/search_applicant.html')
def search_applicant():
    form = SearchForm()

    applicants = []

    if form.validate_on_submit():
        applicants = models.Applicant.query.filter(models.Applicant.first_name.like(u'%{0}%'.format(form.token.data))
                                                   | models.Applicant.last_name.like(u'%{0}%'.format(form.token.data))
                                                   | models.Applicant.mail.like(u'%{0}%'.format(form.token.data))
                                                   | models.Applicant.tag.like(u'%{0}%'.format(form.token.data)))

    return dict(form=form, applicants=applicants)


@auth_required
def add_attendance(applicant_id, course_id):  # TODO: make forms, csrf
    applicant = models.Applicant.query.get_or_404(applicant_id)
    course = models.Course.query.get_or_404(course_id)

    if applicant.in_course(course) or applicant.active_in_parallel_course(course):
        flash(u'Der Teilnehmer ist bereits im Kurs oder nimmt aktiv an einem Parallelkurs teil', 'danger')
        return redirect(url_for('applicant', id=applicant_id))

    try:
        # Graduation optional, waits and pays by default
        applicant.add_course_attendance(course, None, True, True)
        db.session.commit()
        flash(u'Der Teilnehmer wurde in den Kurs eingetragen. Bitte jetzt Status setzen und überprüfen.', 'success')

        if not course.is_allowed(applicant):
            flash(u'Der Teilnehmer hat eigentlich nicht die entsprechenden Sprachtest-Ergebnisse. Teilnehmer wurde trotzdem eingetragen.', 'warning')

        return redirect(url_for('status', applicant_id=applicant_id, course_id=course_id))
    except Exception as e:
        db.session.rollback()
        flash(u'Der Teilnehmer konnte nicht für den Kurs eingetragen werden: {0}'.format(e), 'danger')

    return redirect(url_for('applicant', id=applicant_id))


@auth_required
def remove_attendance(applicant_id, course_id):  # TODO: make forms, csrf
    attendance = models.Attendance.query.get_or_404((applicant_id, course_id))

    try:
        attendance.applicant.remove_course_attendance(attendance.course)
        db.session.commit()
        flash(u'Der Bewerber wurde aus dem Kurs genommen', 'success')
        return redirect(url_for('applicant', id=applicant_id))
    except Exception as e:
        db.session.rollback()
        flash(u'Der Bewerber konnte nicht aus dem Kurs genommen werden: {0}'.format(e), 'danger')
        return redirect(url_for('applicant', id=applicant_id))

    return redirect(url_for('internal'))


@auth_required
@templated('internal/applicants/applicant_attendances.html')
def applicant_attendances(id):
    return dict(applicant=models.Applicant.query.get_or_404(id))


@auth_required
@templated('internal/payments.html')
def payments():
    form = PaymentForm()

    if form.validate_on_submit():
        code = form.confirmation_code.data
        match = re.search(r'^A(?P<a_id>\d{1,})C(?P<c_id>\d{1,})$', code)  # 'A#C#'

        if match:
            a_id, c_id = match.group('a_id', 'c_id')
            return redirect(url_for('status', applicant_id=a_id, course_id=c_id))

        flash(u'Belegungsnummer ungültig', 'danger')

    stat_list = db.session.query(models.Attendance.paidbycash,
                                 func.sum(models.Attendance.amountpaid),
                                 func.count(),
                                 func.avg(models.Attendance.amountpaid),
                                 func.min(models.Attendance.amountpaid),
                                 func.max(models.Attendance.amountpaid)) \
                          .filter(not_(models.Attendance.waiting), models.Attendance.has_to_pay) \
                          .group_by(models.Attendance.paidbycash)

    desc = ['cash', 'sum', 'count', 'avg', 'min', 'max']
    stats = [dict(zip(desc, tup)) for tup in stat_list]

    return dict(form=form, stats=stats)


@auth_required
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


@auth_required
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
            flash(u'Der Status wurde aktualisiert', 'success')
        except Exception as e:
            db.session.rollback()
            flash(u'Der Status konnte nicht aktualisiert werden: {0}'.format(e), 'danger')
            return dict(form=form, attendance=attendance)

    form.populate(attendance)
    return dict(form=form, attendance=attendance)


@auth_required
@templated('internal/statistics.html')
def statistics():
    return None


@auth_required
@templated('internal/statistics/free_courses.html')
def free_courses():
    rv = models.Course.query.join(models.Language.courses) \
                      .order_by(models.Language.name, models.Course.level, models.Course.alternative)

    return dict(courses=rv)


@auth_required
@templated('internal/statistics/origins_breakdown.html')
def origins_breakdown():
    rv = db.session.query(models.Origin, func.count()) \
                   .join(models.Applicant, models.Attendance) \
                   .filter(not_(models.Attendance.waiting)) \
                   .group_by(models.Origin) \
                   .order_by(models.Origin.name)

    return dict(origins_breakdown=rv)


@auth_required
@templated('internal/statistics/task_queue.html')
def task_queue():
    jobs = []
    try:
        jobs = queue.jobs
    except ConnectionError as e:
        flash(u'Jobabfrage nicht möglich: {0}'.format(e), 'danger')

    tasks = []
    for job in jobs:
        payload = ''

        try:
            args = job.args[0]

            # if the argument is a flask.ext.Message we know how to get its most interesting information
            if isinstance(args, Message):
                payload = u'{0}, {1}'.format(args.recipients, args.subject)

            # otherwise we have to show the description for now -- XXX: support more tasks
            else:
                payload = args

        except IndexError:
            payload = job.args

        task = {'id': job.id, 'status': job.get_status(), 'created_at': job.created_at, 'payload': payload}
        tasks.append(task)

    return dict(tasks=tasks)


@auth_required
@templated('internal/preterm.html')
def preterm():
    form = PretermForm()

    token = None

    if form.validate_on_submit():
        token = form.get_token()

        try:
            msg = Message(sender=app.config['PRIMARY_MAIL'],
                          recipients=[form.mail.data.encode('utf-8')],
                          subject=u'[Sprachenzentrum] URL für prioritäre Anmeldung',
                          body=u'{0}'.format(url_for('index', token=token, _external=True)))

            mail.send(msg)
            flash(u'Eine Mail mit der Token URL wurde an {0} verschickt'.format(form.mail.data), 'success')

        except (AssertionError, socket.error) as e:
            flash(u'Eine Bestätigungsmail konnte nicht verschickt werden: {0}'.format(e), 'danger')

    # always show preterm signups in this view
    attendances = models.Attendance.query \
                        .join(models.Course, models.Language, models.Applicant) \
                        .filter(models.Attendance.registered < models.Language.signup_begin) \
                        .order_by(models.Applicant.last_name, models.Applicant.first_name)

    return dict(form=form, token=token, preterm_signups=attendances)


@auth_required
@templated('internal/duplicates.html')
def duplicates():
    taglist = db.session.query(models.Applicant.tag) \
                        .filter(models.Applicant.tag != None, models.Applicant.tag != '') \
                        .group_by(models.Applicant.tag) \
                        .having(func.count(models.Applicant.id) > 1)

    doppelganger = [models.Applicant.query.filter_by(tag=duptag) for duptag in map(lambda tup: tup[0], taglist)]

    return dict(doppelganger=doppelganger)


# This is the first-come-first-served policy view
@auth_required
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
            flash(u'Kurse bestmöglichst mit Nachrückern gefüllt', 'success')
        except Exception as e:
            db.session.rollback()
            flash(u'Die Kurse konnten nicht mit Nachrückern gefüllt werden: {0}'.format(e), 'danger')
            return redirect(url_for('restock_fcfs'))

        if len(restocked_attendances) == 0:
            flash(u'Die Kurse konnten nicht mit Nachrückern gefüllt werden, da keine freien Plätze mehr vorhanden sind', 'warning')
            return redirect(url_for('restock_fcfs'))

        try:
            with mail.connect() as conn:
                for attendance in restocked_attendances:
                    msg = Message(sender=g.user, recipients=[attendance.applicant.mail],
                                  reply_to=attendance.course.language.reply_to,
                                  subject=u'[Sprachenzentrum] Freier Platz im Kurs {0}'.
                                          format(attendance.course.full_name()),
                                  body=render_template('mails/restockmail.html', attendance=attendance))

                    conn.send(msg)

            flash(u'Mails erfolgreich verschickt', 'success')
            return redirect(url_for('internal'))

        except (AssertionError, socket.error) as e:
            flash(u'Mails konnten nicht verschickt werden: {0}'.format(e), 'danger')

    return dict(form=form)


# This is the weighted-random-selection policy view
@auth_required
@templated('internal/restock_rnd.html')
def restock_rnd():
    form = RestockFormRnd()
    if form.validate_on_submit():
        # eager loading, see (search for 'subqueryload'): http://docs.sqlalchemy.org/en/rel_0_9/orm/loading_relationships.html
        to_assign = models.Attendance.query \
                                     .options(orm.subqueryload(models.Attendance.applicant).subqueryload(models.Applicant.attendances)) \
                                     .filter_by(waiting=True) \
                                     .all()

        # TODO: filter the random selection range, e.g.:

                              #.filter(models.Attendance.registered.between(models.Language.signup_begin,
                              #                                             models.Language.signup_begin + timedelta(hours=app.config["RANDOM_WINDOW_OPEN_FOR"]))) \

        # (attendance, weight) tuples from query would be possible, too; eager loading already takes care of not issuing tons of sql queries here
        weights = [1.0 / len(attendance.applicant.attendances) for attendance in to_assign]

        stats = {'filled': 0, 'paying': 0, 'all': len(to_assign), 'del_overbooked': 0, 'del_parallel': 0}

        while to_assign:
            assert len(to_assign) == len(weights)

            # weighted random selection
            gen = WeightedRandomGenerator(weights)
            idx = gen.next()

            # remove attendance and weight from possible candidates as to not select again;  guarantees termination
            attendance = to_assign.pop(idx)
            del weights[idx]

            # no chance to get into course; management wants us to delete the attendance completely from the system
            if attendance.course.is_overbooked():
                db.session.delete(attendance)
                stats['del_overbooked'] += 1
                continue

            # no chance to get into course, delete attendance
            if attendance.applicant.active_in_parallel_course(attendance.course):
                db.session.delete(attendance)
                stats['del_parallel'] += 1
                continue

            # keep default waiting status
            if len(attendance.course.get_active_attendances()) >= attendance.course.limit:
                continue

            attendance.has_to_pay = attendance.applicant.has_to_pay()
            attendance.waiting = False

            stats['filled'] += 1
            stats['paying'] += 1 if attendance.has_to_pay else 0

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(u'Das Füllen des Systems mit Teilnahmen nach dem Zufallsprinzip konnte nicht durchgeführt werden: {0}'.format(e), 'danger')
            return redirect(url_for('restock_rnd'))

        # TODO: send mails
        flash(u'{0} Teilnahmen (von {1} Wartenden) konnten zugewiesen werden. Davon sind {2} Zahlende.' \
                u'Teilnahmen gelöscht: {3} (da überbucht), {4} (da bereits aktiv in Parallelkurs)' \
                .format(stats['filled'], stats['all'], stats['paying'], stats['del_overbooked'], stats['del_parallel']), 'success')

    return dict(form=form)


@auth_required
@templated('internal/unique.html')
def unique():
    form = UniqueForm()

    if form.validate_on_submit():
        courses = form.get_courses()
        deleted = 0

        try:
            waiting_but_active_parallel = [attendance for course in courses for attendance in course.get_waiting_attendances()
                                           if attendance.applicant.active_in_parallel_course(course)]

            for attendance in waiting_but_active_parallel:
                db.session.delete(attendance)
                deleted += 1

            db.session.commit()
            flash(u'Kurse von {0} wartenden Teilnahmen mit aktiven Parallelkurs bereinigt'.format(deleted), 'success')
        except Exception as e:
            db.session.rollback()
            flash(u'Die Kurse konnten nicht von wartenden Teilnahmen mit aktiven Parallelkurs bereinigt werden: {0}'.format(e), 'danger')
            return redirect(url_for('unique'))

    return dict(form=form)


# vim: set tabstop=4 shiftwidth=4 expandtab:
