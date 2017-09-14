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

from sqlalchemy import and_, func, not_

from flask import request, redirect, render_template, url_for, flash, make_response
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from spz import app, models, db, token, tasks
from spz.decorators import templated
import spz.forms as forms
from spz.util.Filetype import mime_from_filepointer
from spz.mail import generate_status_mail


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
    form = forms.SignupForm(show_all_courses=current_user.is_authenticated)
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
            '{0}!'.format(course.language.until_signup_fmt()),
            user_has_special_rights
        )
        err |= check_precondition_with_auth(
            course.is_allowed(applicant),
            'Sie haben nicht die vorausgesetzten Sprachtest-Ergebnisse um diesen Kurs zu wählen! '
            '(Hinweis: Der Datenabgleich mit Ilias erfolgt regelmäßig, '
            'jedoch nicht automatisch sondern manuell.)',  # 2*15m, just in case
            user_has_special_rights
        )
        err |= check_precondition_with_auth(
            not applicant.in_course(course) and not applicant.active_in_parallel_course(course),
            'Sie sind bereits für diesen Kurs oder einem Parallelkurs angemeldet!',
            user_has_special_rights
        )
        err |= check_precondition_with_auth(
            not applicant.over_limit(),
            'Sie haben das Limit an Bewerbungen bereits erreicht!',
            user_has_special_rights
        )
        err |= check_precondition_with_auth(
            not course.is_overbooked(),  # no transaction guarantees here, but overbooking is some sort of soft limit
            'Der Kurs ist hoffnungslos überbelegt. Darum werden keine Registrierungen mehr entgegengenommen!',
            user_has_special_rights
        )
        if err:
            return dict(form=form)

        # Run the final insert isolated in a transaction, with rollback semantics
        # As of 2015, we simply put everyone into the waiting list by default and then randomly insert, see #39
        try:
            waiting = not preterm
            informed_about_rejection = waiting and course.language.is_open_for_signup_fcfs(time)
            applicant.add_course_attendance(
                course,
                form.get_graduation(),
                waiting=waiting,
                has_to_pay=applicant.has_to_pay(),
                informed_about_rejection=informed_about_rejection
            )
            db.session.add(applicant)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Ihre Kurswahl konnte nicht registriert werden: {0}'.format(e), 'negative')
            return dict(form=form)

        # Preterm signups are in by default and management wants us to send mail immediately
        try:
            tasks.send_slow.delay(generate_status_mail(applicant, course, time))
        except (AssertionError, socket.error, ConnectionError) as e:
            flash('Eine Bestätigungsmail konnte nicht verschickt werden: {0}'.format(e), 'negative')

        # Finally redirect the user to an confirmation page, too
        return render_template('confirm.html', applicant=applicant, course=course)

    return dict(form=form)


@templated('licenses.html')
def licenses():
    return None


@templated('signoff.html')
def signoff():
    form = forms.SignoffForm()
    if form.validate_on_submit():
        applicant = form.get_applicant()
        course = form.get_course()
        signoff_id = form.get_signoff_id()
        if (applicant is not None):
            if applicant.matches_signoff_id(signoff_id):
                if applicant.in_course(course):
                    if course.language.is_open_for_self_signoff(datetime.utcnow()):
                        try:
                            applicant.remove_course_attendance(course)

                            attends = len([attendance for attendance in applicant.attendances if not attendance.waiting])
                            if applicant.is_student() and attends > 0:
                                free_course = False
                                for attendance in applicant.attendances:
                                    if attendance.has_to_pay is False and not attendance.waiting:
                                        free_course = True
                                if not free_course:
                                    applicant.attendances[0].has_to_pay = False
                            db.session.commit()
                            flash('Abmeldung erfolgreich!', 'positive')
                        except Exception as e:
                            db.session.rollback()
                            flash('Konnte nicht erfolgreich abmelden, bitte erneut versuchen:{0}'.format(e), 'negative')
                        try:
                            tasks.send_slow.delay(generate_status_mail(applicant, course, datetime.utcnow()))
                        except (AssertionError, socket.error, ConnectionError) as e:
                            flash('Eine Bestätigungsmail konnte nicht verschickt werden: {0}'.format(e), 'negative')
                    else:
                        flash('Abmeldefrist abgelaufen: Zur Abmeldung bitte mit Ihrem '
                              'Fachbereichsleiter reden!', 'negative')

                else:
                    flash('Abmeldung fehlgeschlagen: Sie können sich nicht von einem Kurs '
                          'abmelden, für den Sie nicht angemeldet waren!', 'negative')
            else:
                flash('Abmeldung fehlgeschlagen: Ungültige Abmelde-ID!', 'negative')
        else:
            flash('Abmeldung fehlgeschlagen: E-Mailadresse nicht vorhanden.', 'negative')

    return dict(form=form)


@login_required
@templated('internal/overview.html')
def internal():
    logs = models.LogEntry.get_visible_log(current_user, 200)
    return dict(logs=logs)


@login_required
@templated('internal/registrations.html')
def registrations():
    form = forms.TagForm()
    return dict(form=form)


@login_required
@templated('internal/registrations.html')
def registrations_import():
    form = forms.TagForm()
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

                return redirect(url_for('registrations'))

            flash('Falscher Dateitype {0}, bitte nur Text oder CSV Dateien verwenden'.format(mime), 'danger')
            return None

    flash('Datei konnte nicht gelesen werden', 'negative')
    return dict(form=form)


@login_required
@templated('internal/registrations.html')
def registrations_verify():
    form = forms.TagForm()

    if form.validate_on_submit():
        tag = form.get_tag()
        tag_exists = models.verify_tag(tag)

    return dict(form=form, tag_exists=tag_exists, tag=tag)


@login_required
@templated('internal/approvals.html')
def approvals():
    form = forms.TagForm()
    return dict(form=form)


@login_required
@templated('internal/approvals.html')
def approvals_import():
    if request.method == 'POST':
        fp = request.files['file_name']
        if fp:
            mime = mime_from_filepointer(fp)
            if mime == 'text/plain':
                try:
                    priority = bool(request.form.getlist("priority"))
                    approvals = extract_approvals(fp, priority)

                    num_deleted = 0
                    if request.form.getlist("delete_old"):
                        # only remove sticky entries because
                        num_deleted = models.Approval.query.filter(and_(
                            models.Approval.sticky == True,
                            models.Approval.priority == priority
                        )).delete()  # NOQA
                    # add approvals
                    db.session.add_all(approvals)
                    db.session.commit()
                    flash('Import OK: {0} Einträge gelöscht, {1} Eintrage hinzugefügt'
                          .format(num_deleted, len(approvals)), 'success')
                except Exception as e:  # csv, index or db could go wrong here..
                    db.session.rollback()
                    flash('Konnte Einträge nicht speichern, bitte neu einlesen: {0}'.format(e), 'negative')
                return dict(form=forms.TagForm())

            flash('Falscher Dateitype {0}, bitte nur Text oder CSV Dateien verwenden'.format(mime), 'danger')
            return redirect(url_for('approvals'))

    flash('Datei konnte nicht gelesen werden', 'negative')
    return redirect(url_for('approvals'))


def extract_approvals(fp, priority):
    """Extracts approvals of a file

       :param fp: filepointe to the file
       :param priority: if the approval entries are priority entries
    """
    # strip all known endings ('\r', '\n', '\r\n') and remove empty lines
    # and duplicates and header lines
    stripped_lines = (
        line.decode('utf-8', 'ignore').rstrip('\r').rstrip('\n').rstrip('\r').strip()
        for line in fp.readlines()
    )
    filtered_lines = (
        line
        for line in stripped_lines
        if line and not line.startswith('"Name";"Benutzername";"Matrikelnummer"') and
        not line.startswith('"Name";"Login";"Matriculation number"')
    )
    filecontent = csv.reader(filtered_lines, delimiter=';')  # XXX: hardcoded?

    # set columns indices depending on file type (ILIAS or selfmade)
    ilias_export = bool(request.form.getlist("ilias_export"))
    # create list of sticky Approvals, so that background jobs don't remove them
    approvals = []
    for line in filecontent:
        # set rating and tag depending on file type (ILIAS or selfmade)
        if ilias_export:
            # test if all params are existent, if not skip entry
            if line[1] == '' or line[3] == '' or line[4] == '':
                continue
            # calc params
            rating = max(
                0,
                min(
                    int(100 * int(line[3]) / int(line[4])),
                    100
                )
            )
            # set tag depending if an immatriculation number is existing. If not set tag to account name
            if not line[2] == '':
                tag = line[2]
            else:
                tag = line[1]
        else:
            rating = int(line[1])
            tag = line[0]
        approvals.append(
            models.Approval(
                tag=tag,
                percent=rating,
                sticky=True,
                priority=priority
            )
        )
    return approvals


@login_required
@templated('internal/approvals.html')
def approvals_check():
    form = forms.TagForm()

    if form.validate_on_submit():
        tag = form.get_tag()
        approvals = models.Approval.get_for_tag(tag)
    return dict(form=form, tag=tag, approvals=approvals)


@login_required
@templated('internal/notifications.html')
def notifications():
    form = forms.NotificationForm()

    if form.validate_on_submit():
        # get attachement data once
        at_mime = ''
        at_data = None
        at_name = ''
        if form.get_attachment():
            # detect MIME data since browser tend to send messy data,
            # e.g. https://bugzilla.mozilla.org/show_bug.cgi?id=373621
            at_mime = mime_from_filepointer(form.get_attachment())
            at_data = form.get_attachment().read()
            at_name = form.get_attachment().filename

        try:
            for recipient in form.get_recipients():
                msg = Message(
                    sender=current_user.email,
                    recipients=[recipient],
                    subject=form.get_subject(),
                    body=form.get_body(),
                    cc=form.get_cc(),
                    bcc=form.get_bcc(),
                    reply_to=form.get_reply_to(),
                    charset='utf-8'
                )
                if form.get_attachment():
                    msg.attach(at_name, at_mime, at_data)
                tasks.send_slow.delay(msg)

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
    form = forms.ApplicantForm()

    if form.validate_on_submit():

        try:
            applicant.first_name = form.first_name.data
            applicant.last_name = form.last_name.data
            applicant.phone = form.phone.data
            applicant.mail = form.mail.data
            applicant.tag = form.tag.data
            applicant.origin = form.get_origin()
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
    form = forms.SearchForm()

    applicants = []

    if form.validate_on_submit():
        # split query into words, each word has to match at least one of the following attributes:
        #  - first name
        #  - second name
        #  - mail address
        #  - tag
        parts = form.query.data.split(' ')
        query = None
        for p in parts:
            p = p.strip()
            if p:
                ilike_str = '%{0}%'.format(p.replace('\\', '\\\\').replace('%', '\\%'))
                subquery = (
                    models.Applicant.first_name.ilike(ilike_str)
                    | models.Applicant.last_name.ilike(ilike_str)
                    | models.Applicant.mail.ilike(ilike_str)
                    | models.Applicant.tag.ilike(ilike_str)
                )
                if query is None:
                    query = subquery
                else:
                    query = query & subquery
        if query is not None:
            applicants = models.Applicant.query.filter(query)

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
            tasks.send_slow.delay(generate_status_mail(applicant, course, restock=True))
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
            tasks.send_slow.delay(generate_status_mail(applicant, course))
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
    form = forms.PaymentForm()

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
    form = forms.StatusForm()

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
                tasks.send_quick.delay(generate_status_mail(applicant, course))
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
        i = tasks.cel.control.inspect()
        everything = i.scheduled()
        jobs = everything[next(iter(everything.keys()))]
    except ConnectionError as e:
        flash('Jobabfrage nicht möglich: {0}'.format(e), 'warning')

    work = []
    for job in jobs:
        request = job['request']
        payload = '{}({}, {})'.format(request['name'], request['args'], request['kwargs'])

        task = {'id': request['id'], 'started': request['time_start'], 'payload': payload, 'priority': job['priority']}
        work.append(task)

    return dict(tasks=work)


@login_required
@templated('internal/preterm.html')
def preterm():
    form = forms.PretermForm()

    token = None

    if form.validate_on_submit():
        token = form.get_token()

        try:
            tasks.send_quick.delay(
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


@login_required
@templated('internal/unique.html')
def unique():
    form = forms.UniqueForm()

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
    form = forms.LoginForm()

    if form.validate_on_submit():
        user = models.User.get_by_login(form.user.data, form.password.data)
        if user:
            login_user(user, remember=True)
            return redirect(url_for('internal'))
        flash('Du kommst hier net rein!', 'negative')

    return dict(form=form)


def logout():
    logout_user()
    flash('Tschau!', 'success')
    return redirect(url_for('login'))
