from typing import Any

from PySide6.QtCore import QObject, Signal


class Worker(QObject):
    started = Signal()
    progress = Signal(Any)
    finished = Signal()

    def run(self):
        pass
