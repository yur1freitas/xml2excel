import tkinter as tk

import customtkinter as ctk

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
    Root,
)
from xml2excel.manager.context import GlobalContext
from xml2excel.utils.path import resource_path

ctk.set_default_color_theme(str(resource_path('assets/themes/shadcn.json')))

ctx = GlobalContext()
app = App()

root = Root(app)
root.pack(fill=tk.Y, expand=True)
root.grid(
    column=1,
    row=0,
    padx=16,
    pady=16,
)


import_files_btn = ImportFilesButton(root, ctx, text='Importar XMLs')
import_files_btn.grid(column=0, row=0, padx=4)

export_files_btn = ExportFilesButton(
    root,
    ctx,
    text='Exportar',
)
export_files_btn.grid(column=1, row=0, padx=4)

number_files_imported = NumberFilesImported(root, ctx)
number_files_imported.grid(column=0, row=1, columnspan=2, pady=4)

index_option = IndexOption(
    root,
    ctx,
    text='Inserir Coluna de Índice?',
)
index_option.grid(column=0, row=2, columnspan=2, pady=4, sticky=tk.W)


merge_option = MergeOption(
    root,
    ctx,
    text='Mesclar Arquivos em um único arquivo?',
)
merge_option.grid(column=0, row=3, columnspan=2, pady=4, sticky=tk.W)

recursive_option = RecursiveOption(
    root,
    ctx,
    text='Buscar em subdiretórios?',
)
recursive_option.grid(column=0, row=4, columnspan=2, pady=4, sticky=tk.W)


prefix_option = PrefixOption(
    root,
    ctx,
)
prefix_option.grid(column=0, row=5, columnspan=2, pady=4, sticky=tk.W)


disable_columns_list = DisableColumnsList(root, ctx, width=300, height=300)
disable_columns_list.grid(column=0, row=6, columnspan=2, pady=4, sticky=tk.NSEW)


if __name__ == '__main__':
    app.mainloop()
