# -*- coding: utf-8 -*-

"""Helper functions for pdf-generator.
"""

from datetime import datetime
from fpdf import FPDF

from flask import make_response
from flask.ext.login import login_required

from spz import app, models


class BasePDF(FPDF):
    def header(self):
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Karlsruher Institut für Technologie (KIT)', 0, 0)
        self.cell(0, 5, app.config['SEMESTER_NAME'], 0, 1, 'R')
        self.set_font('Arial', 'B', 10)
        self.cell(0, 5, 'Sprachenzentrum', 0)

    def get_column_size(self):
        return self.column_size

    def get_header_texts(self):
        return self.header_texts


class CourseGenerator(BasePDF):
    column_size = [7, 40, 40, 20, 80, 30, 15, 15, 15, 15]
    header_texts = ["Nr.", "Nachname", "Vorname", "Matr.", "E-Mail", "Telefon", "Tln.", "Prf.", "Note", "Prozent"]

    def header(self):
        super(CourseGenerator, self).header()
        self.cell(0, 5, 'Kursliste', 0, 0, 'R')
        self.ln()

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', '', 11)
        self.cell(
            0,
            7,
            'Datum _________________ Unterschrift ____________________________________',
            0,
            1,
            'R'
        )
        self.set_font('Arial', '', 9)
        self.cell(
            0,
            5,
            'Personen, die nicht auf der Liste stehen, '
            'haben nicht bezahlt und sind nicht zur Kursteilnahme berechtigt. '
            'Dementsprechend können Sie auch keine Teilnahme- oder Prüfungsscheine erhalten.',
            0,
            1,
            'C'
        )
        self.cell(
            0,
            5,
            'Nach Kursende bitte abhaken, ob der Teilnehmer regelmäßig anwesend war, '
            'ob er die Abschlussprüfung bestanden hat und dann die unterschriebene Liste wieder zurückgeben. Danke!',
            0,
            1,
            'C'
        )


class PresenceGenerator(BasePDF):
    column_size = [7, 40, 40, 20, 80, 6]
    header_texts = ["Nr.", "Nachname", "Vorname", "Matr.", "E-Mail", ""]

    def header(self):
        super(PresenceGenerator, self).header()
        self.cell(0, 5, 'Anwesenheitsliste', 0, 0, 'R')
        self.ln()

    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Diese Liste bildet lediglich eine Hilfe im Unterricht und verbleibt beim Dozenten.', 0, 1, 'C')


def list_presence(pdflist, course):
    column = pdflist.get_column_size()
    header = pdflist.get_header_texts()

    def maybe(x):
        return x if x else ''

    active_no_debt = [attendance.applicant for attendance in course.attendances
                      if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]
    active_no_debt.sort()

    pdflist.add_page()

    pdflist.set_font('Arial', 'B', 16)
    pdflist.cell(0, 10, '{0}'.format(course.full_name()), 0, 1, 'C')
    pdflist.set_font('Arial', '', 10)
    height = 6

    idx = 1
    for c, h in zip(column, header):
        pdflist.cell(c, height, h, 1)
    for i in range(13):
        pdflist.cell(column[-1], height, '', 1)
    pdflist.ln()
    for applicant in active_no_debt:
        content = [idx, applicant.last_name, applicant.first_name, maybe(applicant.tag), applicant.mail, ""]
        for c, co in zip(column, content):
            pdflist.cell(c, height, '{0}'.format(co), 1)
        for i in range(13):
            pdflist.cell(column[-1], height, '', 1)
        pdflist.ln()

        idx += 1
    return


@login_required
def print_course_presence(course_id):
    pdflist = PresenceGenerator('L', 'mm', 'A4')
    course = models.Course.query.get_or_404(course_id)
    list_presence(pdflist, course)

    resp = make_response(pdflist.output('', 'S'))
    resp.headers['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(course.full_name())
    resp.mimetype = 'application/pdf'

    return resp


@login_required
def print_language_presence(language_id):
    language = models.Language.query.get_or_404(language_id)
    pdflist = PresenceGenerator('L', 'mm', 'A4')
    for course in language.courses:
        list_presence(pdflist, course)

    resp = make_response(pdflist.output('', 'S'))
    resp.headers['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(language.name)
    resp.mimetype = 'application/pdf'

    return resp


def list_course(pdflist, course):
    column = pdflist.get_column_size()
    header = pdflist.get_header_texts()

    def maybe(x):
        return x if x else ''

    active_no_debt = [attendance.applicant for attendance in course.attendances
                      if not attendance.waiting and (not attendance.has_to_pay or attendance.amountpaid > 0)]
    active_no_debt.sort()

    pdflist.add_page()
    course_str = '{0}'.format(course.full_name())
    pdflist.set_font('Arial', 'B', 16)
    pdflist.cell(0, 10, course_str, 0, 1, 'C')

    pdflist.set_font('Arial', '', 10)
    height = 6

    idx = 1
    for c, h in zip(column, header):
        pdflist.cell(c, height, h, 1)
    pdflist.ln()
    for applicant in active_no_debt:
        content = [
            idx,
            applicant.last_name,
            applicant.first_name,
            maybe(applicant.tag),
            applicant.mail,
            applicant.phone,
            "",
            "",
            "",
            ""
        ]
        for c, co in zip(column, content):
            pdflist.cell(c, height, '{0}'.format(co), 1)
        pdflist.ln()
        idx += 1
    return


@login_required
def print_course(course_id):
    pdflist = CourseGenerator('L', 'mm', 'A4')
    course = models.Course.query.get_or_404(course_id)
    list_course(pdflist, course)

    resp = make_response(pdflist.output('', 'S'))
    resp.headers['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(course.full_name())
    resp.mimetype = 'application/pdf'

    return resp


@login_required
def print_language(language_id):
    language = models.Language.query.get_or_404(language_id)
    pdflist = CourseGenerator('L', 'mm', 'A4')
    for course in language.courses:
        list_course(pdflist, course)

    resp = make_response(pdflist.output('', 'S'))
    resp.headers['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(language.name)
    resp.mimetype = 'application/pdf'

    return resp


@login_required
def print_bill(applicant_id, course_id):
    class BillGenerator(FPDF):
        def header(this):
            this.zwischenraum = 21
            this.teiler = ''
            this.rahmen = 0
            this.breite = 128
            now = datetime.now()
            if now.month < 3:
                semester = 'Wintersemester {0}/{1}'.format(now.year-1, now.year)
            elif now.month < 9:
                semester = 'Sommersemester {0}'.format(now.year)
            else:
                semester = 'Wintersemester {0}/{1}'.format(now.year, now.year+1)
            this.set_font('Arial', '', 10)
            # fpdf.cell(w,h=0,txt='',border=0,ln=0,align='',fill=0,link='')
            this.cell(80, 5, 'Karlsruher Institut für Technologie (KIT)', 0, 0)
            this.cell(48, 5, semester, 0, 0, 'R')
            this.cell(this.zwischenraum, 5, this.teiler, this.rahmen, 0, 'C')
            this.cell(80, 5, 'Karlsruher Institut für Technologie (KIT)', 0, 0)
            this.cell(48, 5, semester, 0, 1, 'R')
            this.set_font('Arial', 'B', 10)
            this.cell(80, 5, 'Sprachenzentrum', 0, 0)
            this.set_font('Arial', '', 10)
            this.cell(48, 5, datetime.now().strftime("%d.%m.%Y"), 0, 0, 'R')
            this.cell(this.zwischenraum, 5, this.teiler, this.rahmen, 0, 'C')
            this.set_font('Arial', 'B', 10)
            this.cell(80, 5, 'Sprachenzentrum', 0, 0)
            this.set_font('Arial', '', 10)
            this.cell(48, 5, datetime.now().strftime("%d.%m.%Y"), 0, 1, 'R')

        def footer(this):
            this.set_y(-15)
            this.set_font('Arial', '', 8)
            this.cell(
                this.breite,
                4,
                'Diese Quittung wurde maschinell ausgestellt und ist ohne Unterschrift gültig.',
                0,
                0,
                'C'
            )
            this.cell(this.zwischenraum, 4, this.teiler, this.rahmen, 0, 'C')
            this.cell(
                this.breite,
                4,
                'Diese Quittung wurde maschinell ausgestellt und ist ohne Unterschrift gültig.',
                0,
                1,
                'C'
            )
            this.cell(this.breite, 4, 'Exemplar für den Teilnehmer.', 0, 0, 'C')
            this.cell(this.zwischenraum, 4, this.teiler, this.rahmen, 0, 'C')
            this.cell(this.breite, 4, 'Exemplar für das Sprachenzentrum.', 0, 1, 'C')

    attendance = models.Attendance.query.get_or_404((applicant_id, course_id))

    bill = BillGenerator('L', 'mm', 'A4')
    bill.add_page()
#   fpdf.cell(w,h=0,txt='',border=0,ln=0,align='',fill=0,link='')
    title = 'Quittung'
    sex_str = '{0}'.format('Herr' if attendance.applicant.sex else 'Frau')
    applicant_str = '{0} {1}'.format(attendance.applicant.first_name, attendance.applicant.last_name)
    tag_str = 'Matrikelnummer {0}'.format(attendance.applicant.tag) if attendance.applicant.tag else ''
    now = datetime.now()
    str1 = 'für die Teilnahme am Kurs:'
    course_str = '{0}'.format(attendance.course.full_name())
    amount_str = '{0} Euro'.format(attendance.amountpaid)
    str2 = 'bezahlt.'
    str3 = 'Stempel'
    code = 'A{0}C{1}'.format(applicant_id, course_id)
    bill.cell(bill.breite, 6, code, 0, 0, 'R')
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, code, 0, 1, 'R')
    bill.ln(20)
    bill.set_font('', 'B', 16)
    bill.cell(bill.breite, 8, title, 0, 0, 'C')
    bill.cell(bill.zwischenraum, 8, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 8, title, 0, 1, 'C')
    bill.ln(20)

    bill.set_font('', '', 12)
    bill.cell(bill.breite, 6, sex_str, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, sex_str, 0, 1)
    bill.cell(bill.breite, 6, applicant_str, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, applicant_str, 0, 1)
    bill.cell(bill.breite, 6, tag_str, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, tag_str, 0, 1)
    bill.cell(bill.breite, 6, 'hat am {0}'.format(now.strftime("%d.%m.%Y")), 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, 'hat am {0}'.format(now.strftime("%d.%m.%Y")), 0, 1)
    bill.cell(bill.breite, 6, str1, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, str1, 0, 1)
    bill.set_font('', 'B', 12)
    bill.cell(bill.breite, 6, course_str, 0, 0, 'C')
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, course_str, 0, 1, 'C')
    bill.cell(bill.breite, 6, amount_str, 0, 0, 'C')
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, amount_str, 0, 1, 'C')
    bill.set_font('', '', 12)
    bill.cell(bill.breite, 6, str2, 0, 0)
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, str2, 0, 1)

    bill.ln(30)
    bill.cell(bill.breite, 6, str3, 0, 0, 'C')
    bill.cell(bill.zwischenraum, 6, bill.teiler, bill.rahmen, 0, 'C')
    bill.cell(bill.breite, 6, str3, 0, 1, 'C')

    resp = make_response(bill.output('', 'S'))
    resp.headers['Content-Disposition'] = 'attachment; filename="Quittung {0}.pdf"' \
        .format(attendance.applicant.last_name)
    resp.mimetype = 'application/pdf'

    return resp
