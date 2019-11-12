# -*- coding: utf-8 -*-

"""Export module for course lists.

   Formatters are loaded dynamically by their file name.
"""

from flask import make_response
from spz import app


class TableWriter:

    def parse_template_row(self, row):
        self.row_template = [app.jinja_env.compile_expression(e) for e in row]

    def write_element(self, element):
        row = self.generate_row(element)
        self.write_row(row)

    def generate_row(self, element):
        return [cell_template(element) for cell_template in self.row_template]


def binary_template_expected(f):
    f.binary_template = True
    return f


from .excel import ExcelWriter  # noqa
from .csv import CSVWriter  # noqa


course_formatters = {
    'excel': ExcelWriter,
    'csv': CSVWriter
}


def init_formatter(lookup_table, format):
    formatter = lookup_table.get(format.formatter)()
    binary = hasattr(formatter.load_template_file, 'binary_template')
    mode = 'rb' if binary else 'r'
    if format.template:
        with app.open_resource('templates/' + format.template, mode) as file:
            formatter.load_template_file(file)
    return formatter


def export_course_list(courses, format, filename='Kursliste'):
    formatter = init_formatter(course_formatters, format)
    for course in courses:
        for applicant in course.course_list:
            formatter.write_element({'course': course, 'applicant': applicant})

    resp = make_response(formatter.get_data())
    resp.headers['Content-Disposition'] = 'attachment; filename="{0}.{1}"'.format(filename, format.extension)
    resp.mimetype = formatter.mimetype

    return resp
