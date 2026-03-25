from collections import defaultdict
from enum import IntEnum
from typing import Iterable, TypeAlias, cast

from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from xml2excel.aliases import AnyPath
from xml2excel.utils.flatdict import flatdict

WorksheetId: TypeAlias = int | None


class CustomWorksheet(Worksheet):
    def __init__(self):
        super().__init__()

        self.row_idx = 0
        self.column_idx = 0
        self.column_position = dict[str, int]()

    def next_row(self):
        self.row_idx += 1

    def get_column_position(self, name: str) -> int | None:
        if name in self.column_position:
            return self.column_position[name]

    def add_column(self, name: str, value: int | float | str) -> None:
        column_index = self.get_column_position(name)

        if column_index:
            self.write(self.row_idx, column_index, value)
        else:
            self.write(0, self.column_idx, name)
            self.write(self.row_idx, self.column_idx, value)

            self.column_position[name] = self.column_idx
            self.column_idx += 1


class CustomWorksheetGenerator:
    def __init__(self, workbook: Workbook) -> None:
        self._workbook = workbook

    def __call__(self) -> CustomWorksheet:
        worksheet = self._workbook.add_worksheet(
            worksheet_class=CustomWorksheet
        )

        return cast(CustomWorksheet, worksheet)


class ColumnPrefixStyle(IntEnum):
    NONE = 0
    PARENT = 1
    HIERARCHICAL = 2


class FlatDict2Excel:
    def __init__(
        self,
        filepath: AnyPath,
        ignore_columns: Iterable[str] = [],
        column_prefix_style: ColumnPrefixStyle = ColumnPrefixStyle.HIERARCHICAL,
    ):
        self.filepath = filepath
        self.ignore_columns = set(ignore_columns)
        self.column_prefix_style = column_prefix_style

        self.workbook = Workbook(filepath)
        self.worksheets = defaultdict[WorksheetId, CustomWorksheet](
            CustomWorksheetGenerator(self.workbook)
        )

    def _resolve_primitive(
        self,
        id: WorksheetId,
        key: str,
        value: int | float | str,
    ) -> None:
        worksheet = self.worksheets[id]
        worksheet.add_column(key, value)

    def _resolve_list(self, id: WorksheetId, key: str, value: list) -> None:
        new_id = len(self.worksheets)

        for item in value:
            if isinstance(item, (str, int, float)):
                self._resolve_primitive(id, key, item)

            elif isinstance(item, list) and len(item) > 0:
                self._resolve_list(id, key, item)

            elif isinstance(item, flatdict) and len(item) > 0:
                self._resolve_dict(new_id, item)

    def _resolve_dict(self, id: WorksheetId, target: flatdict) -> None:
        worksheet = self.worksheets[id]
        worksheet.next_row()

        for key, value in target.iteritems():
            if self._can_ignore_column(key):
                continue

            column_name = self._resolve_column_name(key, target._delimiter)

            if isinstance(value, (int, float, str)):
                self._resolve_primitive(id, column_name, value)

            elif isinstance(value, list):
                self._resolve_list(id, column_name, value)

    def _can_ignore_column(self, key: str) -> bool:
        if len(self.ignore_columns) > 0:
            for column_name in self.ignore_columns:
                if key.startswith(column_name):
                    return True

        return False

    def _resolve_column_name(self, key: str, delimiter: str) -> str:
        match self.column_prefix_style:
            case ColumnPrefixStyle.NONE:
                return key.split(delimiter)[-1]
            case ColumnPrefixStyle.PARENT:
                return delimiter.join(key.split(delimiter)[-2:])
            case _:
                return key

    def __call__(self, *args: flatdict):
        for arg in args:
            if len(arg) > 0:
                self._resolve_dict(None, arg)

        self.workbook.close()
