import sys

from PySide6 import QtAsyncio, QtCore
from PySide6.QtWidgets import QGridLayout, QWidget

from xml2excel.components import (
    App,
    DisableColumnsList,
    ExportFilesButton,
    ImportFilesButton,
    IndexOption,
    MergeOption,
    NumberFilesImported,
    PrefixOption,
    RecursiveOption,
    ToggleThemeButton,
    Window,
)
from xml2excel.utils.path import resource_path


def main():
    app = App(sys.argv)
    window = Window()

    app.load_stylesheet(resource_path('styles/global.qss'))

    root = QWidget()
    root_layout = QGridLayout(root)

    root.setLayout(root_layout)
    window.setCentralWidget(root)

    root_layout.setColumnStretch(0, 1)
    root_layout.setColumnStretch(1, 1)
    root_layout.setColumnStretch(3, 1)

    widget = QWidget()
    layout = QGridLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)

    toggle_theme_btn = ToggleThemeButton()

    import_files_btn = ImportFilesButton(text='Importar XMLs')
    export_files_btn = ExportFilesButton(text='Exportar')

    number_files_imported = NumberFilesImported()

    merge_option = MergeOption(text='Mesclar arquivos na exportação?')
    index_option = IndexOption(
        text='Incluir coluna de índice? (importe novamente para atualizar)'
    )
    recursive_option = RecursiveOption(
        text='Analisar subdiretórios ao importar?',
    )

    prefix_option = PrefixOption()

    disable_columns_list = DisableColumnsList()
    disable_columns_list.setFixedHeight(300)

    layout.addWidget(import_files_btn, 0, 0)
    layout.addWidget(export_files_btn, 0, 1)

    layout.addWidget(
        number_files_imported,
        1,
        0,
        1,
        2,
        alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
    )

    layout.addWidget(merge_option, 2, 0, 1, 2)
    layout.addWidget(index_option, 3, 0, 1, 2)
    layout.addWidget(recursive_option, 4, 0, 1, 2)

    layout.addWidget(prefix_option, 5, 0, 1, 2)

    layout.addWidget(disable_columns_list, 6, 0, 4, 2)

    root_layout.addWidget(
        toggle_theme_btn,
        0,
        2,
        alignment=QtCore.Qt.AlignmentFlag.AlignTop,
    )

    root_layout.addWidget(
        widget,
        0,
        1,
        alignment=QtCore.Qt.AlignmentFlag.AlignTop,
    )

    window.show()

    QtAsyncio.run(handle_sigint=True)


if __name__ == '__main__':
    main()
