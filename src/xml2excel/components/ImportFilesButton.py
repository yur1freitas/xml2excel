from PySide6.QtCore import QThread, Slot
from PySide6.QtWidgets import QFileDialog, QPushButton

from xml2excel.commands.import_files import (
    ImportFilesInput,
    ImportFilesOutput,
    import_files,
)
from xml2excel.components import App
from xml2excel.utils.worker import Worker


class ImportFilesWorker(Worker):
    def __init__(self, input: ImportFilesInput):
        super().__init__()

        self.input = input

    def run(self):
        self.started.emit()

        output = import_files(self.input)
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
            input = ImportFilesInput(
                path=dirpath,
                recursive=config.recursive,
                prefix_mode=config.prefix_mode,
            )

            self._thread = QThread()

            self._worker = ImportFilesWorker(input)
            self._worker.moveToThread(self._thread)

            self._thread.started.connect(self._worker.run)
            self._thread.finished.connect(self._thread.deleteLater)

            @Slot()
            def on_started():
                self.setEnabled(False)

            @Slot(ImportFilesOutput)
            def on_progress(output: ImportFilesOutput):
                store.data = output.data
                store.filepaths = output.filepaths

            @Slot()
            def on_finished():
                self.setEnabled(True)

                self._thread.quit()
                self._worker.deleteLater()

            self._worker.started.connect(on_started)
            self._worker.progress.connect(on_progress)
            self._worker.finished.connect(on_finished)

            self._thread.start()
