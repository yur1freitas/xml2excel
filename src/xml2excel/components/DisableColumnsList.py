import tkinter as tk
from typing import Callable, cast

import pandas as pd
from customtkinter.windows.widgets.ctk_scrollable_frame import (
    CTkScrollableFrame,
)

from xml2excel.aliases import DataFrameTuple
from xml2excel.components.DisableColumnsItem import DisableColumnsItem
from xml2excel.manager.context import GlobalContext


class DisableColumnsList(CTkScrollableFrame):
    def __init__(self, master, ctx: GlobalContext, **kwargs):
        super().__init__(master, **kwargs)

        self._ctx = ctx
        self.__wrapper = None

        self._ctx.store.trace('data', self._update_list)

    def _update_list(self, data: DataFrameTuple) -> None:
        if data is None:
            return

        self._ctx.config.ignore_columns = []

        for widget in self.winfo_children():
            widget.destroy()

        if len(data) == 0:
            return

        df = pd.concat(data)
        columns = df.columns

        for column in columns:
            item = DisableColumnsItem(
                self,
                text=column,
                command=self._create_command(column),
            )

            item.pack(
                fill=tk.BOTH,
                expand=1,
                pady=2,
            )

    def _create_command(self, column: str) -> Callable:
        config = self._ctx.config

        def command(*args) -> None:
            columns = cast(list[str], config.ignore_columns)

            if column in columns:
                columns.remove(column)
            else:
                columns.append(column)

        return command
