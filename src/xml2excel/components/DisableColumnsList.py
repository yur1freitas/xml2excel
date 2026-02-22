import pandas as pd
from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget

from xml2excel.aliases import DataFrameTuple
from xml2excel.components.DisableColumnsItem import DisableColumnsItem
from xml2excel.manager.context import GlobalContext


class DisableColumnsList(QWidget):
    def __init__(self, ctx: GlobalContext, **kwargs):
        super().__init__(**kwargs)

        self._ctx = ctx
        self._ctx.store.trace('data', self._on_data_change)

        self._layout = QVBoxLayout(self)

        self._label = QLabel(text='Colunas Habilitadas: ')
        self._layout.addWidget(self._label)

        self._scrollarea = QScrollArea()
        self._scrollarea.setWidgetResizable(True)
        self._layout.addWidget(self._scrollarea)

        self._scrollarea_widget = QWidget()
        self._scrollarea_layout = QVBoxLayout(self._scrollarea_widget)

        self._scrollarea.setWidget(self._scrollarea_widget)

    def _reset(self):
        self._ctx.config.ignore_columns = []

        for i in range(self._scrollarea_layout.count()):
            item = self._scrollarea_layout.itemAt(i)
            widget = item.widget() if item else None

            if widget:
                widget.setParent(None)

    def _on_data_change(self, data: DataFrameTuple | None) -> None:
        self._reset()

        if not data:
            return

        df = pd.concat(data)

        for column in df.columns:
            item = DisableColumnsItem(self._ctx, text=column)
            self._scrollarea_layout.addWidget(item)
