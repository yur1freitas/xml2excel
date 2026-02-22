import sys

from PySide6 import QtAsyncio, QtCore
from PySide6.QtWidgets import QGridLayout, QWidget
from qt_material import apply_stylesheet

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
    Window,
)
from xml2excel.manager.context import GlobalContext


def main():
    ctx = GlobalContext()

    app = App(sys.argv)
    window = Window()

    apply_stylesheet(app, theme='dark_blue.xml')

    root = QWidget()

    root_layout = QGridLayout(root)
    root.setLayout(root_layout)
    window.setCentralWidget(root)

    root_layout.setColumnStretch(0, 1)
    root_layout.setColumnStretch(1, 1)
    root_layout.setColumnStretch(2, 1)

    widget = QWidget()
    layout = QGridLayout(widget)

    import_files_btn = ImportFilesButton(ctx, text='Importar XMLs')
    export_files_btn = ExportFilesButton(ctx, text='Exportar')

    number_files_imported = NumberFilesImported(ctx)

    merge_option = MergeOption(ctx, text='Mesclar arquivos na exportação?')
    index_option = IndexOption(
        ctx, text='Incluir coluna de índice? (importe novamente para atualizar)'
    )
    recursive_option = RecursiveOption(
        ctx,
        text='Analisar subdiretórios ao importar?',
    )

    prefix_option = PrefixOption(ctx)

    disable_columns_list = DisableColumnsList(ctx)
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
        widget,
        0,
        1,
        alignment=QtCore.Qt.AlignmentFlag.AlignTop,
    )

    window.show()

    QtAsyncio.run(handle_sigint=True)


if __name__ == '__main__':
    main()
