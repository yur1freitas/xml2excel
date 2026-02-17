import tkinter as tk
from pathlib import Path
from tkinter.filedialog import askdirectory, asksaveasfilename

from xml2excel.aliases import DataFrameTuple
from xml2excel.commands.export_files import (
    ExportFilesInput,
    export_files,
)
from xml2excel.consts import FileExtensions
from xml2excel.manager.context import GlobalContext
from xml2excel.utils.path import resolve_filepath

from .Button import Button


class ExportFilesButton(Button):
    DIALOG_TITLE = 'Exportar'

    def __init__(self, master, ctx: GlobalContext, **kwargs):
        self._ctx = ctx

        super().__init__(
            master, state=tk.DISABLED, command=self._command, **kwargs
        )

        self._ctx.store.trace('data', self._update_state)

    def _update_state(self, data: DataFrameTuple) -> None:
        state = tk.NORMAL if data is not None else tk.DISABLED
        self.configure(state=state)

    def _command(self, *args):
        store = self._ctx.store
        config = self._ctx.config

        if store.data is None:
            return

        if config.merge:
            filepath = asksaveasfilename(
                title=self.DIALOG_TITLE,
                defaultextension=FileExtensions.EXCEL,
            )

            if filepath:
                export_files(
                    ExportFilesInput(
                        output=filepath,
                        data=store.data,
                        index=config.index,
                        merge=config.merge,
                        ignore_columns=config.ignore_columns,
                    )
                )

            return

        if store.filepaths is not None:
            root = askdirectory(title=ExportFilesButton.DIALOG_TITLE)

            if root:
                resolved_filepaths = tuple(
                    resolve_filepath(
                        root=root,
                        filename=Path(filepath).name,
                        ext=FileExtensions.EXCEL,
                    )
                    for filepath in store.filepaths
                )

                export_files(
                    ExportFilesInput(
                        output=resolved_filepaths,
                        data=store.data,
                        index=config.index,
                        merge=config.merge,
                        ignore_columns=config.ignore_columns,
                    )
                )
