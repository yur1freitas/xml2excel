from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog, QPushButton

from xml2excel.aliases import DataFrameTuple
from xml2excel.commands.export_files import (
    ExportFilesInput,
    export_files,
)
from xml2excel.components import App
from xml2excel.consts import FileExtensions
from xml2excel.utils.path import resolve_filepath


class ExportFilesButton(QPushButton):
    DIALOG_TITLE = 'Exportar'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.instance()
        self.app.store.trace('data', self._update_state)

        self.clicked.connect(self._click)

    def _update_state(self, data: DataFrameTuple) -> None:
        self.setDisabled(data is None)

    @Slot()
    def _click(self):
        store = self.app.store
        config = self.app.config

        if store.data is None:
            return

        if config.merge:
            filepath = QFileDialog.getOpenFileName(
                self,
                caption=self.DIALOG_TITLE,
                filter=FileExtensions.EXCEL,
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
            root = QFileDialog.getExistingDirectory(
                self,
                caption=ExportFilesButton.DIALOG_TITLE,
            )

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
