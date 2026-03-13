from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
)

from xml2excel.aliases import DataFrameTuple
from xml2excel.commands.export_files import (
    ExportFilesInput,
    export_files,
)
from xml2excel.components import App
from xml2excel.consts import FileExtensions, FileGlobs
from xml2excel.utils.path import resolve_filepath


class ExportFilesButton(QPushButton):
    DIALOG_TITLE = 'Exportar'

    def __init__(self, text: str):
        super().__init__()

        self.setObjectName(self.__class__.__name__)

        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(8, 0, 8, 0)

        self._layout.setColumnStretch(0, 1)
        self._layout.setColumnStretch(3, 1)

        self._icon = QFrame()
        self._icon.setFixedSize(16, 16)
        self._icon.setObjectName('Icon')

        self._label = QLabel(text)
        self._label.setObjectName('Label')

        self._layout.addWidget(self._icon, 0, 1)
        self._layout.addWidget(self._label, 0, 2)

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
            filepath = QFileDialog.getSaveFileName(
                self,
                caption=self.DIALOG_TITLE,
                filter=FileGlobs.EXCEL,
            )[0]

            if filepath:
                export_files(
                    ExportFilesInput(
                        output=Path(filepath).with_suffix(FileExtensions.EXCEL),
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
