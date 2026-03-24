from pathlib import Path

from PySide6.QtCore import QThread, Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
)

from xml2excel.aliases import AnyPath
from xml2excel.commands.import_files import import_files
from xml2excel.components import App
from xml2excel.utils.flatdict2excel import ColumnPrefixStyle
from xml2excel.utils.worker import Worker
from xml2excel.utils.xml2flatdict import XMLData


class ImportFilesWorker(Worker):
    def __init__(
        self,
        path: AnyPath,
        recursive: bool = False,
        prefix_mode: ColumnPrefixStyle = ColumnPrefixStyle.PARENT,
    ):
        super().__init__()

        self.path = path
        self.recursive = recursive
        self.prefix_mode = prefix_mode

    def run(self):
        self.started.emit()

        for data in import_files(path=self.path, recursive=self.recursive):
            self.progress.emit(data)

        self.finished.emit()


class ImportFilesButton(QPushButton):
    DIALOG_TITLE = 'Importar XMLs'

    def __init__(self, text: str):
        super().__init__()

        self.setObjectName(self.__class__.__name__)

        self.app = App.instance()

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

        self.clicked.connect(self._runtask)

    @Slot()
    def _runtask(self) -> None:
        store = self.app.store
        config = self.app.config

        dirpath = QFileDialog.getExistingDirectory(
            self,
            caption=self.DIALOG_TITLE,
        )

        if dirpath:
            store.data = ()
            store.filepaths = ()

            self._thread = QThread()

            self._worker = ImportFilesWorker(
                path=dirpath,
                recursive=config.recursive,
                prefix_mode=config.prefix_mode,
            )

            self._worker.moveToThread(self._thread)

            self._thread.started.connect(self._worker.run)
            self._thread.finished.connect(self._thread.deleteLater)

            @Slot()
            def on_started():
                store.pending = True
                self.setEnabled(False)

            @Slot(tuple)
            def on_progress(data: tuple[Path, XMLData]):
                filepath, df = data

                store.data = (*store.data, df)  # type: ignore

                if store.filepaths is not None:
                    store.filepaths = (*store.filepaths, filepath)
                else:
                    store.filepaths = (filepath,)

            @Slot()
            def on_finished():
                store.pending = False
                self.setEnabled(True)

                self._thread.quit()
                self._worker.deleteLater()

            self._worker.started.connect(on_started)
            self._worker.progress.connect(on_progress)
            self._worker.finished.connect(on_finished)

            self._thread.start()
