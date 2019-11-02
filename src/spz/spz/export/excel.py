# -*- coding: utf-8 -*-

"""Formatter that writes excel files.
"""

# import re
from tempfile import NamedTemporaryFile
from openpyxl import load_workbook
# from openpyxl.worksheet.table import Table
# from openpyxl.workbook.child import INVALID_TITLE_REGEX

from spz import app


class ExcelCourseWriter:

    def __init__(self, template):
        self.load_template(template)

    def load_template(self, template):
        with app.open_resource('templates/' + template, 'rb') as file:
            self.workbook = load_workbook(file)
            fill_in = self.workbook.defined_names['FILL_IN']
            self.row_definitions = [app.jinja_env.compile_expression(e) for e in fill_in.comment.split(';')]
            # for now there is only suport for one fill_in range
            (sheet, range) = next(fill_in.destinations)
            self.row_iterator = iter(self.workbook[sheet][range])

    def process(self, courses):
        for course in courses:  # write data
            for applicant in course.course_list:
                self.write_element({'course': course, 'applicant': applicant})

    def write_element(self, element):
        row = next(self.row_iterator)
        cell_iterator = iter(row)
        for definition in self.row_definitions:
            next(cell_iterator).value = definition(element)

    """
    def new_section(self, name):
        if self.workbook._sheets:
            self.end_section()
        # Sheet naming is very constrained: some chars are disallowed , names need to be unique & maximum length is 32
        # Openpyxl knows about the first two but not about the last one. It will automatically enforce unique naming by
        # appending an incrementer (e.g. [sheet, sheet] -> [sheet1, sheet2]). This then might cause the length limit to
        # be exceeded: Therefore we use a shorter limit of only 30 characters here.
        name = re.sub(INVALID_TITLE_REGEX, '', name)[:30]
        self.workbook.create_sheet(name)
    """

    def get_data(self):
        with NamedTemporaryFile() as file:
            self.workbook.save(file.name)
            file.seek(0)
            stream = file.read()
        return stream

    @property
    def mimetype(self):
        return self.workbook.mime_type
