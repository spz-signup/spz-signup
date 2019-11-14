# -*- coding: utf-8 -*-

"""Formatter that writes excel files.
"""

from . import TableWriter

from tempfile import NamedTemporaryFile
from openpyxl import load_workbook
from openpyxl.worksheet.cell_range import CellRange
# from openpyxl.workbook.child import INVALID_TITLE_REGEX
# from zipfile import ZipFile


def find_table(workbook, table_name):
    for sheet in workbook.worksheets:
        for table in sheet._tables:
            return (sheet, table)


class ExcelWriter(TableWriter):

    @property
    def mimetype(self):
        return self.workbook.mime_type

    def __init__(self, template):
        TableWriter.__init__(self, template, binary_template=True)

    def parse_template(self, file):
        self.workbook = load_workbook(file)
        (self.sheet, self.table) = find_table(self.workbook, 'DATA')
        self.range = CellRange(self.table.ref)
        expression_row = [self.sheet.cell(*c).value for c in self.range.bottom]
        self.delete_last_row()  # remove row containing template data from output
        return super().parse_template(expression_row)

    def write_row(self, row):
        row_iter = iter(row)
        self.range.expand(down=1)
        for c in self.range.bottom:
            self.sheet.cell(*c).value = next(row_iter)
        self.table.ref = self.range.coord

    def delete_last_row(self):
        self.sheet.delete_rows(self.range.max_row)
        self.range.shrink(bottom=1)

    def get_data(self):
        with NamedTemporaryFile() as file:
            self.workbook.save(file.name)
            file.seek(0)
            stream = file.read()
        return stream
