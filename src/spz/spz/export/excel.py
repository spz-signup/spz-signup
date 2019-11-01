# -*- coding: utf-8 -*-

"""Formatter that writes excel files.
"""

import re
from tempfile import NamedTemporaryFile
from openpyxl import Workbook
from openpyxl.worksheet.table import Table
from openpyxl.workbook.child import INVALID_TITLE_REGEX


class ExcelCourseWriter:

    def __init__(self):
        # write_only=True would require additional logic to keep track of sheet dimension so we keep it at False
        # (see sheet.dimensions in end_section())
        self.workbook = Workbook(write_only=False)
        self.workbook._sheets.clear()  # start off with no sheets

    def write_heading(self):
        # TODO
        pass

    def write_element(self, element):
        # TODO
        pass

    def write_row(self, values):
        self.workbook._sheets[-1].append(values)

    def new_section(self, name):
        if self.workbook._sheets:
            self.end_section()
        # Sheet naming is very constrained: some chars are disallowed , names need to be unique & maximum length is 32
        # Openpyxl knows about the first two but not about the last one. It will automatically enforce unique naming by
        # appending an incrementer (e.g. [sheet, sheet] -> [sheet1, sheet2]). This then might cause the length limit to
        # be exceeded: Therefore we use a shorter limit of only 30 characters here.
        name = re.sub(INVALID_TITLE_REGEX, '', name)[:30]
        self.workbook.create_sheet(name)

    def get_data(self):
        if self.workbook._sheets:
            self.end_section()
        with NamedTemporaryFile() as file:
            self.workbook.save(file.name)
            file.seek(0)
            stream = file.read()
        return stream

    def end_section(self):
        sheet = self.workbook._sheets[-1]
        # if there are values: create a table within the excel sheet to simplify sorting by values
        # else: excel considers the file invalid if a table contains only one row so don't
        if sheet.max_row > 1:
            tableName = sheet.title.replace(' ', '_')  # needs to be unique and must not contain spaces
            table = Table(displayName=tableName, ref=sheet.dimensions)
            sheet.add_table(table)
