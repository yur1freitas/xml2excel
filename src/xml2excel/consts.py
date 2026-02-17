from enum import StrEnum


class FileExtensions(StrEnum):
    EXCEL = '.xlsx'
    CSV = '.csv'
    XML = '.xml'


class FileGlobs(StrEnum):
    EXCEL = '*.xlsx'
    CSV = '*.csv'
    XML = '*.xml'
