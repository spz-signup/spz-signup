# -*- coding: utf-8 -*-

"""Export module for course lists.
"""

from flask import make_response
from spz import app


class TemplatedWriter:

    def __init__(self, template=None, binary_template=True):
        if template:
            mode = 'rb' if binary_template else 'r'
            with app.open_resource('templates/' + template, mode) as file:
                self.template = self.parse_template(file)

    def parse_template(self, file):
        return None

    def write_element(self, element):
        pass

    def begin_section(self, title):
        pass

    def end_section(self, title):
        pass

    def get_data(self):
        pass


class TableWriter(TemplatedWriter):

    def __init__(self, template=None, binary_template=True):
        TemplatedWriter.__init__(self, template, binary_template)

    def parse_template(self, expression_list):
        return [app.jinja_env.compile_expression(e) for e in expression_list]

    def write_element(self, element):
        row = self.generate_row(element)
        self.write_row(row)

    def generate_row(self, element):
        return [cell_template(element) for cell_template in self.template]

    def write_row(self, row):
        pass


from .excel import ExcelWriter, ExcelZipWriter, SingleSectionExcelWriter  # noqa
from .csv import CSVWriter  # noqa


course_formatters = {
    'excel': ExcelWriter,
    'single-excel': SingleSectionExcelWriter,
    'zip-excel': ExcelZipWriter,
    'csv': CSVWriter
}


def init_formatter(lookup_table, format):
    return lookup_table.get(format.formatter)(format.template)


def export_course_list(courses, format, filename='Kursliste'):
    formatter = init_formatter(course_formatters, format)
    for course in courses:
        formatter.begin_section(course.full_name)
        for applicant in course.course_list:
            formatter.write_element(dict(course=course, applicant=applicant))
        formatter.end_section(course.full_name)

    resp = make_response(formatter.get_data())
    resp.headers['Content-Disposition'] = 'attachment; filename="{0}.{1}"'.format(filename, formatter.extension)
    resp.mimetype = formatter.mimetype

    return resp
