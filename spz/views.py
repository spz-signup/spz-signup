# -*- coding: utf-8 -*-

"""The application's views.

   Manages the mapping between routes and their activities.
"""

import socket
import csv

from flask import request, redirect, render_template, url_for, flash
from flask.ext.mail import Message
from sqlalchemy.orm.exc import FlushError


from spz import app, models, mail, db
from spz.decorators import templated, auth_required
from spz.headers import upheaders
from spz.forms import SignupForm, NotificationForm


@upheaders
@templated('signup.html')
def index():
    form = SignupForm()

<<<<<<< HEAD
    if form.validate_on_submit():
        erg = BerErg(form)
        flash(u'Ihre Angaben waren plausibel', 'success')
        return render_template('confirm.html', erg=erg)

    return dict(form=form)


#hier werden die Teilnahmebedingunen geprüft 
def BerErg(form):
    

    bestApproval = 0
    course = models.Course.query.get(form.course.data)
    language = models.Language.query.get(course.language_id)

    kurs = 'Kurs: %s %s (kurs_id=%s) ' % (language.name, course.level, course.id)
    history = [kurs]

    if language.name == 'English':
        isEnglish = 'Englisch'
        approval = [a.percent for a in models.Approval.query.filter_by(tag = form.tag.data).all()]
        if len(approval) == 0:
            history.append(u'für Englisch nicht zugelassen (link zur Anmeldemaske ohne Englischkurse) ')
            return dict (history=history)
        
        bestApproval = max(approval) if approval else 0
        if bestApproval < 50: # dummy value
            history.append('fuer Englisch dieser Stufe nicht zugelassen (link zur Anmeldemaske mit eingeschraenkten Englischkursen) ')
            return  dict (history=history) ## TODO Tabelle mit Kursen um Grenzen erweitern
    else:
        isEnglish = 'nicht Englisch'
         

    occupancy = models.Attendance.query.filter_by(course_id = form.course.data).count()
    c = models.Course.query.filter_by(id = form.course.data).first()
    regularOffer = c.limit
    howFull = 'Ihr Platz %s von %s' % (occupancy, regularOffer)
    if occupancy > regularOffer:
        s = models.StateOfAtt.query.filter_by(name = 'Warteliste')
        history.append(u'Warteliste')
#        insertAttendance(c,s)
    else:
        history.append(u'Fester Platz')
    

    isStudent = True if models.Registration.query.filter_by(rnumber = form.tag.data).first() else False
    if not isStudent:
        s = models.StateOfAtt.query.filter_by(name = 'Bar zu bezahlen')
        history.append(u'Gebührenpflichtig')
    else:
        history.append(u'Auf der Matrikelliste')
=======
    evaluated = []  # XXX: remove this
>>>>>>> d005e0ce2a62d0bc4970d4ae75a34746188c6b2d

    if form.validate_on_submit():
        applicant = form.get_applicant()
        course = form.get_course()

        if course.is_english() and not course.is_allowed(applicant):
            flash(u'Sie haben nicht die vorausgesetzten Englischtest Ergebnisse um diesen Kurs zu wählen', 'danger')
            return dict(form=form)

        # TODO:
        #if course.full():
            #waiting
        #else:
            #attends
        status = models.StateOfAtt.query.first()


        if applicant.has_to_pay():
            evaluated.append(">>> has to pay")

        # Run the final insert isolated in a transaction, with rollback semantics
        try:
            # TODO: check if already in this course
            applicant.add_course_attendance(course, status, form.get_graduation())
            db.session.add(applicant)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(u'Ihre Kurswahl konnte nicht registriert werden: {0}'.format(e), 'danger')
            return dict(form=form)

        # TODO: send mail now

        return render_template('confirm.html', evaluated=evaluated)

    return dict(form=form)

<<<<<<< HEAD
        # belege Kurs
        try:
            retrievedFromSystem.add_course_attendance(c, s, g)
            db.session.commit()
        except (FlushError) as e:
            db.session.rollback()
            flash(u'Diesen Kurs haben Sie bereits belegt): {0}'.format(e), 'danger')                
    else:
        numberOfAtt = 0
        mail = form.mail.data
        tag = form.tag.data
        sex = True if form.sex.data == 1 else False
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data

        # for KIT students only
        degree = models.Degree.query.get_or_404(form.degree.data) if form.degree.data else None
        semester = form.semester.data if form.semester.data else None
        origin  = models.Origin.query.get_or_404(form.origin.data) if form.origin.data else None
            
        applicant = models.Applicant(mail, tag, sex, first_name, last_name, phone, degree, semester, origin)
        applicant.add_course_attendance(c, s, g)
        
        db.session.add(applicant)
        db.session.commit()


    erg = dict(a=who, b=mat, c=mail, d=course, e=stud, f=englishApproval, g=NOA, h=howFull, i=isEnglish, j=price)
    return history
    return erg
=======
>>>>>>> d005e0ce2a62d0bc4970d4ae75a34746188c6b2d

@upheaders
@templated('licenses.html')
def licenses():
    return None


@upheaders
@templated('internal/overview.html')
def internal():
    return None


@upheaders
@auth_required
@templated('internal/statistics.html')
def statistics():
    return None


@upheaders
@auth_required
@templated('internal/datainput.html')
def datainput():
    return None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@upheaders
@auth_required
@templated('internal/datainput/matrikelnummer.html')
def matrikelnummer():
    if request.method == 'POST':
        fp = request.files['file_name']
        if fp:
            lst = {models.Registration(line.rstrip('\r\n')) for line in fp}
            gel = models.Registration.query.delete()
            db.session.add_all(lst)
            db.session.commit()
            flash(u'Dateiname war OK %s Zeilen gelöscht %s Zeilen gelesen' % (gel, len(lst)), 'success')

            return redirect(url_for('internal'))
        flash(u'%s: Wrong file name' % (fp.filename), 'warning')
        return redirect(url_for('matrikelnummer'))
    return None


@upheaders
@auth_required
@templated('internal/datainput/zulassungen.html')
def zulassungen():
    if request.method == 'POST':
        fp = request.files['file_name']
        if fp:
            filecontent = csv.reader(fp, delimiter=';')
            try: 
                lst = [models.Approval(line[0], line[1]) for line in filecontent]
                gel = models.Approval.query.delete()
                db.session.add_all(lst)
                db.session.commit()
#                anz = models.Approval.query.count()
                flash(u' %s Zeilen gelöscht %s Zeilen aus %s gelesen' % (gel, len(lst), fp.filename), 'success')
            except (IndexError, csv.Error) as e:
                flash(u'Zulassungen konnten nicht eingelesen werden (\';\' als Trenner verwenden): {0}'.format(e), 'danger')                

            return redirect(url_for('internal'))
        flash(u'%s: Wrong file name' % (fp.filename), 'warning')
        return redirect(url_for('zulassungen'))
    return None


@upheaders
@auth_required
@templated('internal/notifications.html')
def notifications():
    form = NotificationForm()

    if form.validate_on_submit():
        try:
            # TODO(daniel): extract recipients from courses; sender from config
            msg = Message(subject=form.mail_subject.data, body=form.mail_body.data, recipients=None, sender=None)
            mail.send(msg)
            flash(u'Mail erfolgreich verschickt', 'success')
            return redirect(url_for('internal'))

        except (AssertionError, socket.error) as e:
            flash(u'Mail wurde nicht verschickt: {0}'.format(e), 'danger')

    return dict(form=form)


@upheaders
@auth_required
@templated('internal/all_courses.html')
def all_courses():
    return dict(courses=models.Course.query.order_by(models.Course.id.asc()).all())


@upheaders
@auth_required
@templated('internal/course_attendances.html')
def course_attendances(id):
    course = models.Course.query.get_or_404(id)
    attendances = db.session.query(models.Applicant, models.Attendance).filter(models.Applicant.id==models.Attendance.applicant_id).filter(models.Attendance.course_id==id).all()
    return dict(c=course, a=attendances)


@upheaders
@auth_required
@templated('internal/lists.html')
def lists():
    return dict(languages=models.Language.query.order_by(models.Language.name).all())


@upheaders
@auth_required
@templated('internal/applicant.html')
def applicant(id):
    return dict(applicant = models.Applicant.query.get_or_404(id))


@upheaders
@auth_required
@templated('internal/language.html')
def language(id):
    return dict(language=models.Language.query.get_or_404(id))


@upheaders
@auth_required
@templated('internal/course.html')
def course(id):
    return dict(course=models.Course.query.get_or_404(id))


# vim: set tabstop=4 shiftwidth=4 expandtab:
