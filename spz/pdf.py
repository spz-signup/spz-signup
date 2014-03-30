# -*- coding: utf-8 -*-

"""Helper functions for pdf-generator.
"""

import StringIO
from datetime import datetime
from fpdf import FPDF

from flask import make_response

from spz import models
from spz.decorators import auth_required

class ListGenerator(FPDF):
    def header(this):
        now = datetime.now()
        if now.month < 3: semester = u'Wintersemester {0}/{1}'.format(now.year-1, now.year)
        elif now.month < 9: semester = u'Sommersemester {0}'.format(now.year)
        else: semester = u'Wintersemester {0}/{1}'.format(now.year, now.year+1)
        this.set_font('Arial','',10)
        this.cell(0, 5, u'Karlsruher Institut für Technologie (KIT)', 0, 0)
        this.cell(0, 5, semester, 0, 1, 'R')
        this.set_font('Arial','B',10)
        this.cell(0, 5, u'Sprachenzentrum', 0)
        this.cell(0, 5, u'Kursliste', 0, 1, 'R')
    def footer(this):
        this.set_y(-20)
        this.set_font('Arial','',11)
        this.cell(0,7, u'Datum _________________ Unterschrift ____________________________________', 0, 1, 'R')
        this.set_font('Arial','',9)
        this.cell(0, 5, u'Personen, die nicht auf der Liste stehen, haben nicht bezahlt und sind nicht zur Kursteilnahme berechtigt. Dementsprechend können Sie auch keine Teilnahme- oder Prüfungsscheine erhalten.', 0, 1, 'C')
        this.cell(0, 5, u'Nach Kursende bitte abhaken, ob der Teilnehmer regelmäßig anwesend war, ob er die Abschlussprüfung bestanden hat und dann die unterschriebene Liste wieder zurückgeben. Danke!', 0, 1, 'C')


class PresenceGenerator(FPDF):
    def header(this):
        now = datetime.now()
        if now.month < 3: semester = u'Wintersemester {0}/{1}'.format(now.year-1, now.year)
        elif now.month < 9: semester = u'Sommersemester {0}'.format(now.year)
        else: semester = u'Wintersemester {0}/{1}'.format(now.year, now.year+1)
        this.set_font('Arial','',10)
        this.cell(0, 5, u'Karlsruher Institut für Technologie (KIT)', 0, 0)
        this.cell(0, 5, semester, 0, 1, 'R')
        this.set_font('Arial','B',10)
        this.cell(0, 5, u'Sprachenzentrum', 0)
        this.cell(0, 5, u'Anwesenheitsliste', 0, 1, 'R')
    def footer(this):
        this.set_y(-10)
        this.set_font('Arial','',9)
        this.cell(0, 5, u'Diese Liste bildet lediglich eine Hilfe im Unterricht und verbleibt beim Dozenten.', 0, 1, 'C')


@auth_required
def print_language_presence(language_id):
    language = models.Language.query.get_or_404(language_id)
    list = PresenceGenerator('L','mm','A4')

    maybe = lambda x: x if x else u''
    column = [7, 40, 40, 79, 8]

    for course in language.courses:
        active_no_debt = [attendance.applicant for attendance in course.attendances
                          if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]
        active_no_debt.sort()

        list.add_page()
        course_str = u'{0}'.format(course.full_name())
        list.set_font('Arial','B',16)
        list.cell(0, 10, course_str, 0, 1, 'C')

        list.set_font('Arial','',10)
        height = 6

        idx = 1
        list.cell(7, height, u'Nr.', 1)
        list.cell(40, height, u'Nachname', 1)
        list.cell(40, height, u'Vorname', 1)
        list.cell(80, height, u'E-Mail', 1)
        for i in range(14):
            list.cell(column[4], height, '', 1)
        list.ln()
        for applicant in active_no_debt:
            list.cell(7, height, u'{0}'.format(idx), 1, 0, 'R')
            list.cell(40, height, u'{0}'.format(applicant.last_name), 1)
            list.cell(40, height, u'{0}'.format(applicant.first_name), 1)
            list.cell(80, height, applicant.mail, 1)
            for i in range(14):
                list.cell(column[4], height, '', 1)
            list.ln()

            idx += 1

    buf = StringIO.StringIO()
    buf.write(list.output('','S'))
    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="{0}.pdf"'.format(language.name)
    resp.mimetype = 'application/pdf'

    return resp


@auth_required
def print_language(language_id):
    language = models.Language.query.get_or_404(language_id)
    list = ListGenerator('L','mm','A4')

    maybe = lambda x: x if x else u''
    column = [7, 40, 40, 20, 80, 30, 15, 15, 15, 15]

    for course in language.courses:
        active_no_debt = [attendance.applicant for attendance in course.attendances
                          if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]
        active_no_debt.sort()

        list.add_page()
        course_str = u'{0}'.format(course.full_name())
        list.set_font('Arial','B',16)
        list.cell(0, 10, course_str, 0, 1, 'C')

        list.set_font('Arial','',10)
        height = 6

        idx = 1
        list.cell(column[0], height, u'Nr.', 1)
        list.cell(column[1], height, u'Nachname', 1)
        list.cell(column[2], height, u'Vorname', 1)
        list.cell(column[3], height, u'Matr.', 1)
        list.cell(column[4], height, u'E-Mail', 1)
        list.cell(column[5], height, u'Telefon', 1)
        list.cell(column[6], height, u'Tln.', 1)
        list.cell(column[7], height, u'Prf.', 1)
        list.cell(column[8], height, u'Note', 1)
        list.cell(column[9], height, u'Punkte', 1, 1)
        for applicant in active_no_debt:
            list.cell(column[0], height, u'{0}'.format(idx), 1, 0, 'R')
            list.cell(column[1], height, u'{0}'.format(applicant.last_name), 1)
            list.cell(column[2], height, u'{0}'.format(applicant.first_name), 1)
            list.cell(column[3], height, maybe(applicant.tag), 1)
            list.cell(column[4], height, applicant.mail, 1)
            list.cell(column[5], height, applicant.phone, 1)
            list.cell(column[6], height, u'', 1)
            list.cell(column[7], height, u'', 1)
            list.cell(column[8], height, u'', 1)
            list.cell(column[9], height, u'', 1, 1)

            idx += 1

    buf = StringIO.StringIO()
    buf.write(list.output('','S'))
    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="{0}.pdf"'.format(language.name)
    resp.mimetype = 'application/pdf'

    return resp


@auth_required
def print_course_presence(course_id):
    course = models.Course.query.get_or_404(course_id)
    
    maybe = lambda x: x if x else u''

    active_no_debt = [attendance.applicant for attendance in course.attendances
                      if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]
    active_no_debt.sort()

    pdf = PresenceGenerator('L','mm','A4')
    pdf.add_page()
    course_str = u'{0}'.format(course.full_name())
    pdf.set_font('Arial','B',16)
    pdf.cell(0, 10, course_str, 0, 1, 'C')

    pdf.set_font('Arial','',10)
    height = 6
    
    idx = 1
    column = [7, 40, 40, 79, 8]
    pdf.cell(column[0], height, u'Nr.', 1)
    pdf.cell(column[1], height, u'Nachname', 1)
    pdf.cell(column[2], height, u'Vorname', 1)
    pdf.cell(column[3], height, u'E-Mail', 1)
    for i in range(14):
        pdf.cell(column[4], height, '', 1)
    pdf.ln()
    for applicant in active_no_debt:
        pdf.cell(column[0], height, u'{0}'.format(idx), 1, 0, 'R')
        pdf.cell(column[1], height, u'{0}'.format(applicant.last_name), 1)
        pdf.cell(column[2], height, u'{0}'.format(applicant.first_name), 1)
        pdf.cell(column[3], height, applicant.mail, 1)
        for i in range(14):
            pdf.cell(column[4], height, '', 1)
        pdf.ln()

        idx += 1

    buf = StringIO.StringIO()
    buf.write(pdf.output('','S'))
    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="{0}.pdf"'.format(course.full_name())
    resp.mimetype = 'application/pdf'

    return resp


@auth_required
def print_course(course_id):
    course = models.Course.query.get_or_404(course_id)
    
    maybe = lambda x: x if x else u''

    active_no_debt = [attendance.applicant for attendance in course.attendances
                      if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]
    active_no_debt.sort()

    pdf = ListGenerator('L','mm','A4')
    pdf.add_page()
    course_str = u'{0}'.format(course.full_name())
    pdf.set_font('Arial','B',16)
    pdf.cell(0, 10, course_str, 0, 1, 'C')


    pdf.set_font('Arial','',10)
    height = 6
    
    idx = 1
    column = [7, 40, 40, 20, 80, 30, 15, 15, 15, 15]
    pdf.cell(column[0], height, u'Nr.', 1)
    pdf.cell(column[1], height, u'Nachname', 1)
    pdf.cell(column[2], height, u'Vorname', 1)
    pdf.cell(column[3], height, u'Matr.', 1)
    pdf.cell(column[4], height, u'E-Mail', 1)
    pdf.cell(column[5], height, u'Telefon', 1)
    pdf.cell(column[6], height, u'Tln.', 1)
    pdf.cell(column[7], height, u'Prf.', 1)
    pdf.cell(column[8], height, u'Note', 1)
    pdf.cell(column[9], height, u'Prozent', 1, 1)
    for applicant in active_no_debt:
        pdf.cell(column[0], height, u'{0}'.format(idx), 1, 0, 'R')
        pdf.cell(column[1], height, u'{0}'.format(applicant.last_name), 1)
        pdf.cell(column[2], height, u'{0}'.format(applicant.first_name), 1)
        pdf.cell(column[3], height, maybe(applicant.tag), 1)
        pdf.cell(column[4], height, applicant.mail, 1)
        pdf.cell(column[5], height, applicant.phone, 1)
        pdf.cell(column[6], height, u'', 1)
        pdf.cell(column[7], height, u'', 1)
        pdf.cell(column[8], height, u'', 1)
        pdf.cell(column[9], height, u'', 1, 1)

        idx += 1

    buf = StringIO.StringIO()
    buf.write(pdf.output('','S'))
    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="{0}.pdf"'.format(course.full_name())
    resp.mimetype = 'application/pdf'

    return resp



@auth_required
def print_bill(applicant_id, course_id):
    class BillGenerator(FPDF):
        def header(this):
            this.zwischenraum = 21
            this.teiler = u''
            this.rahmen = 0
            this.breite = 128
            now = datetime.now()
            if now.month < 3: semester = u'Wintersemester {0}/{1}'.format(now.year-1, now.year)
            elif now.month < 9: semester = u'Sommersemester {0}'.format(now.year)
            else: semester = u'Wintersemester {0}/{1}'.format(now.year, now.year+1)
            this.set_font('Arial','',10)
            #fpdf.cell(w,h=0,txt='',border=0,ln=0,align='',fill=0,link='')
            this.cell(80, 5, u'Karlsruher Institut für Technologie (KIT)', 0, 0)
            this.cell(48, 5, semester, 0, 0, 'R')
            this.cell(this.zwischenraum, 5, this.teiler, this.rahmen, 0, 'C')
            this.cell(80, 5, u'Karlsruher Institut für Technologie (KIT)', 0, 0)
            this.cell(48, 5, semester, 0, 1, 'R')
            this.set_font('Arial','B',10)
            this.cell(80, 5, u'Sprachenzentrum', 0, 0)
            this.set_font('Arial','',10)
            this.cell(48, 5, datetime.now().strftime("%d.%m.%Y"), 0, 0, 'R')
            this.cell(this.zwischenraum, 5, this.teiler, this.rahmen, 0, 'C')
            this.set_font('Arial','B',10)
            this.cell(80, 5, u'Sprachenzentrum', 0, 0)
            this.set_font('Arial','',10)
            this.cell(48, 5, datetime.now().strftime("%d.%m.%Y"), 0, 1, 'R')
        def footer(this):
            this.set_y(-15)
            this.set_font('Arial','',8)
            this.cell(this.breite, 4, u'Diese Quittung wurde maschinell ausgestellt und ist ohne Unterschrift gültig.', 0, 0, 'C')
            this.cell(this.zwischenraum, 4, this.teiler, this.rahmen, 0, 'C')
            this.cell(this.breite, 4, u'Diese Quittung wurde maschinell ausgestellt und ist ohne Unterschrift gültig.', 0, 1, 'C')
            this.cell(this.breite, 4, u'Exemplar für den Teilnehmer.', 0, 0, 'C')
            this.cell(this.zwischenraum, 4, this.teiler, this.rahmen, 0, 'C')
            this.cell(this.breite, 4, u'Exemplar für das Sprachenzentrum.', 0, 1, 'C')

    attendance = models.Attendance.query.get_or_404((applicant_id, course_id))

    bill = BillGenerator('L','mm','A4')
    bill.add_page()
#   fpdf.cell(w,h=0,txt='',border=0,ln=0,align='',fill=0,link='')
    title = u'Quittung'
    sex_str = u'{0}'.format(u'Herr' if attendance.applicant.sex else u'Frau')
    applicant_str = u'{0} {1}'.format(attendance.applicant.first_name, attendance.applicant.last_name)
    tag_str = u'Matrikelnummer {0}'.format(attendance.applicant.tag) if attendance.applicant.tag else u''
    now = datetime.now()
    str1 = u'für die Teilnahme am Kurs:'
    course_str = u'{0}'.format(attendance.course.full_name())
    amount_str = u'{0} Euro'.format(attendance.amountpaid)
    str2 = u'bezahlt.'
    str3 = u'Stempel'
    code = u'A{0}C{1}'.format(applicant_id, course_id)
    bill.cell(bill.breite, 6, code, 0, 0, 'R')
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, code, 0, 1, 'R')
    bill.ln(20)
    bill.set_font('','B',16)
    bill.cell(bill.breite, 8, title, 0, 0, 'C')
    bill.cell(bill.zwischenraum, 8, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 8, title, 0, 1, 'C')
    bill.ln(20)

    bill.set_font('','',12)
    bill.cell(bill.breite, 6, sex_str, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, sex_str, 0, 1)
    bill.cell(bill.breite, 6, applicant_str, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, applicant_str, 0, 1)
    bill.cell(bill.breite, 6, tag_str, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, tag_str, 0, 1)
    bill.cell(bill.breite, 6, u'hat am {0}'.format(now.strftime("%d.%m.%Y")), 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, u'hat am {0}'.format(now.strftime("%d.%m.%Y")), 0, 1)
    bill.cell(bill.breite, 6, str1, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, str1, 0, 1)
    bill.set_font('','B',12)
    bill.cell(bill.breite, 6, course_str, 0, 0, 'C')
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, course_str, 0, 1, 'C')
    bill.cell(bill.breite, 6, amount_str, 0, 0, 'C')
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, amount_str, 0, 1, 'C')
    bill.set_font('','',12)
    bill.cell(bill.breite, 6, str2, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, str2, 0, 1)

    bill.ln(30)
    bill.cell(bill.breite, 6, str3, 0, 0, 'C')
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, str3, 0, 1, 'C')

    buf = StringIO.StringIO()
    buf.write(bill.output('','S'))

    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="Quittung {0}.pdf"'.format(attendance.applicant.last_name)
    resp.mimetype = 'application/pdf'

    return resp


# vim: set tabstop=4 shiftwidth=4 expandtab:
