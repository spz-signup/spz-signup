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
        if now.month < 4: semester = u'Wintersemester {0}/{1}'.format(now.year-1, now.year)
        elif now.month < 9: semester = u'Sommersemester {0}.format(now.year)'
        else: semester = u'Wintersemester {0}/{1}'.format(now.year, now.year+1)
        this.set_font('Arial','',10)
        this.cell(0, 5, u'Karlsruher Institut für Technologie (KIT)', 0, 0)
        this.cell(0, 5, semester, 0, 1, 'R')
        this.set_font('Arial','B',10)
        this.cell(0, 5, u'Sprachenzentrum', 0, 1)
    def footer(this):
        this.set_font('Arial','',10)
        this.set_y(-30)
        now = datetime.now()
        this.multi_cell(200, 4, u'Personen, die nicht auf der Liste stehen, haben nicht bezahlt und sind nicht an der Kursteilnahme berechtigt. Dementsprechend könnten Sie auch keine Teilnahme- oder Prüfungsscheine erhalten.', 0, 0)
        this.multi_cell(200, 4, u'Nach Kursende bitte abhaken, ob der Teilnehmer regelmäßig anwesend war, ob er die Abschlussprüfung bestanden hat - falls es eine gab - und dann die Liste wieder zurückgeben. Danke!', 0, 0)
        this.cell(0, 4, now.strftime("%d.%m.%Y %H:%M:%S"), 0, 1, 'R')


@auth_required
def print_language(language_id):
    language = models.Language.query.get_or_404(language_id)
    list = ListGenerator('L','mm','A4')

    maybe = lambda x: x if x else u''

    for course in language.courses:
        active_no_debt = [attendance.applicant for attendance in course.attendances
                          if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]
        list.add_page()
        course_str = u'{0} {1}'.format(course.language.name, course.level)
        list.set_font('Arial','B',16)
        list.cell(0, 10, course_str, 0, 1, 'C')

        list.set_font('Arial','',10)
        hight = 6

        idx = 1
        list.cell(7, hight, u'Nr.', 1)
        list.cell(40, hight, u'Nachname', 1)
        list.cell(40, hight, u'Vorname', 1)
        list.cell(20, hight, u'Matr.', 1)
        list.cell(80, hight, u'E-Mail', 1)
        list.cell(30, hight, u'Telefon', 1)
        list.cell(10, hight, u'Tln.', 1)
        list.cell(10, hight, u'Prf.', 1)
        list.cell(15, hight, u'Note', 1)
        list.cell(15, hight, u'Punkte', 1, 1)
        for applicant in active_no_debt:
            list.cell(7, hight, u'{0}'.format(idx), 1, 0, 'R')
            list.cell(40, hight, u'{0}'.format(applicant.last_name), 1)
            list.cell(40, hight, u'{0}'.format(applicant.first_name), 1)
            list.cell(20, hight, maybe(applicant.tag), 1)
            list.cell(80, hight, applicant.mail, 1)
            list.cell(30, hight, applicant.phone, 1)
            list.cell(10, hight, u'', 1)
            list.cell(10, hight, u'', 1)
            list.cell(15, hight, u'', 1)
            list.cell(15, hight, u'', 1, 1)

            idx += 1

    buf = StringIO.StringIO()
    buf.write(list.output('','S'))
    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="{0}.pdf"'.format(language.name)
    resp.mimetype = 'application/pdf'

    return resp


@auth_required
def print_course(course_id):
    course = models.Course.query.get_or_404(course_id)
    
    # class ListGenerator(FPDF):
        # def header(this):
            # now = datetime.now()
            # if now.month < 4: semester = u'Wintersemester {0}/{1}'.format(now.year-1, now.year)
            # elif now.month < 9: semester = u'Sommersemester {0}.format(now.year)'
            # else: semester = u'Wintersemester {0}/{1}'.format(now.year, now.year+1)
            # this.set_font('Arial','',10)
            # this.cell(0, 5, u'Karlsruher Institut für Technologie (KIT)', 0, 0)
            # this.cell(0, 5, semester, 0, 1, 'R')
            # this.set_font('Arial','B',10)
            # this.cell(0, 5, u'Sprachenzentrum', 0, 1)
        # def footer(this):
            # this.set_y(-35)
            # now = datetime.now()
            # this.cell(0, 10, now.strftime("%d.%m.%Y %H:%M:%S"), 0, 1, 'R')
            # this.multi_cell(200, 4, u'Personen, die nicht auf der Liste stehen, haben nicht bezahlt und sind nicht an der Kursteilnahme berechtigt. Dementsprechend könnten Sie auch keine Teilnahme- oder Prüfungsscheine erhalten.', 0, 0)
            # this.multi_cell(200, 4, u'Nach Kursende bitte abhaken, ob der Teilnehmer regelmäßig anwesend war, ob er die Abschlussprüfung bestanden hat - falls es eine gab - und dann die Liste wieder zurückgeben. Danke!', 0, 0)
            
    maybe = lambda x: x if x else u''

    active_no_debt = [attendance.applicant for attendance in course.attendances
                      if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]

    pdf = ListGenerator('L','mm','A4')
    pdf.add_page()
    course_str = u'{0} {1}'.format(course.language.name, course.level)
    pdf.set_font('Arial','B',16)
    pdf.cell(0, 10, course_str, 0, 1, 'C')


    pdf.set_font('Arial','',10)
    hight = 6
    
    idx = 1
    pdf.cell(7, hight, u'Nr.', 1)
    pdf.cell(40, hight, u'Nachname', 1)
    pdf.cell(40, hight, u'Vorname', 1)
    pdf.cell(20, hight, u'Matr.', 1)
    pdf.cell(80, hight, u'E-Mail', 1)
    pdf.cell(30, hight, u'Telefon', 1)
    pdf.cell(10, hight, u'Tln.', 1)
    pdf.cell(10, hight, u'Prf.', 1)
    pdf.cell(15, hight, u'Note', 1)
    pdf.cell(15, hight, u'Punkte', 1, 1)
    for applicant in active_no_debt:
        pdf.cell(7, hight, u'{0}'.format(idx), 1, 0, 'R')
        pdf.cell(40, hight, u'{0}'.format(applicant.last_name), 1)
        pdf.cell(40, hight, u'{0}'.format(applicant.first_name), 1)
        pdf.cell(20, hight, maybe(applicant.tag), 1)
        pdf.cell(80, hight, applicant.mail, 1)
        pdf.cell(30, hight, applicant.phone, 1)
        pdf.cell(10, hight, u'', 1)
        pdf.cell(10, hight, u'', 1)
        pdf.cell(15, hight, u'', 1)
        pdf.cell(15, hight, u'', 1, 1)

        idx += 1

    buf = StringIO.StringIO()
    buf.write(pdf.output('','S'))
    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="{0} {1}.pdf"'.format(course.language.name, course.level)
    resp.mimetype = 'application/pdf'

    return resp



@auth_required
def print_bill(applicant_id, course_id):

    class BillGenerator(FPDF):
        def header(this):
            now = datetime.now()
            if now.month < 4: semester = u'Wintersemester {0}/{1}'.format(now.year-1, now.year)
            elif now.month < 9: semester = u'Sommersemester {0}.format(now.year)'
            else: semester = u'Wintersemester {0}/{1}'.format(now.year, now.year+1)
            this.set_font('Arial','',10)
            #fpdf.cell(w,h=0,txt='',border=0,ln=0,align='',fill=0,link='')
            this.cell(0, 5, u'Karlsruher Institut für Technologie (KIT)', 0, 0)
            this.cell(0, 5, semester, 0, 1, 'R')
            this.set_font('Arial','B',10)
            this.cell(0, 5, u'Sprachenzentrum', 0, 0)
            this.set_font('Arial','',10)
            this.cell(0, 5, datetime.now().strftime("%d.%m.%Y"), 0, 1, 'R')
        def footer(this):
            this.set_y(-15)
            this.set_font('Arial','',8)
            this.cell(0, 4, u'Diese Quittung wurde maschinell ausgestellt und ist ohne Unterschrift gültig.', 0, 0, 'C')

    attendance = models.Attendance.query.get_or_404((applicant_id, course_id))

    bill = BillGenerator('P','mm','A5')
    bill.add_page()
#   fpdf.cell(w,h=0,txt='',border=0,ln=0,align='',fill=0,link='')
    applicant_str = u'{0} {1} {2}'.format(u'Herr' if attendance.applicant.sex else u'Frau', attendance.applicant.first_name, attendance.applicant.last_name)
    now = datetime.now()
    course_str = u'für die Teilnahme am Kurs:\n{0} {1}'.format(attendance.course.language.name, attendance.course.level)
    amount_str = u'{0} Euro bezahlt.'.format(attendance.amountpaid)
    code = u'A{0}C{1}'.format(applicant_id, course_id)
    bill.cell(0, 6, code, 0, 1, 'R')
    bill.ln(40)
    bill.set_font('','',12)
    bill.cell(0, 6, applicant_str, 0, 1)
    bill.cell(0, 6, u'hat am {0}'.format(now.strftime("%d.%m.%Y")), 0, 1)
    bill.multi_cell(0, 6, course_str, 0, 1)
    bill.cell(0, 6, amount_str, 0, 1)
    bill.ln(30)

    buf = StringIO.StringIO()
    buf.write(bill.output('','S'))

    resp = make_response(buf.getvalue())
    resp.headers['Content-Disposition'] = u'attachment; filename="Quittung {0}.pdf"'.format(attendance.applicant.last_name)
    resp.mimetype = 'application/pdf'

    return resp


# vim: set tabstop=4 shiftwidth=4 expandtab: