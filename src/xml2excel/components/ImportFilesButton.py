from PySide6.QtCore import QThread, Slot
from PySide6.QtWidgets import QFileDialog, QPushButton

from xml2excel.aliases import AnyPath, AnyPathTuple, DataFrameTuple
from xml2excel.commands.import_files import import_files
from xml2excel.components import App
from xml2excel.utils.flatten_xml import PrefixMode
from xml2excel.utils.worker import Worker


class ImportFilesWorker(Worker):
    def __init__(
        self,
        path: AnyPath,
        recursive: bool = False,
        prefix_mode: PrefixMode = PrefixMode.CLOSEST,
    ):
        super().__init__()

        self.path = path
        self.recursive = recursive
        self.prefix_mode = prefix_mode

    def run(self):
        self.started.emit()

        output = import_files(
            path=self.path,
            recursive=self.recursive,
            prefix_mode=self.prefix_mode,
        )

        self.progress.emit(output)

        self.finished.emit()


class ImportFilesButton(QPushButton):
    DIALOG_TITLE = 'Importar XMLs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.instance()
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
                self.setEnabled(False)

            @Slot(tuple)
            def on_progress(output: tuple[DataFrameTuple, AnyPathTuple]):
                data, filepaths = output

                store.data = data
                store.filepaths = filepaths

            @Slot()
            def on_finished():
                self.setEnabled(True)

                self._thread.quit()
                self._worker.deleteLater()

            self._worker.started.connect(on_started)
            self._worker.progress.connect(on_progress)
            self._worker.finished.connect(on_finished)

            self._thread.start()
