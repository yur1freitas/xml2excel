import tkinter as tk
from enum import StrEnum

import customtkinter as ctk

from xml2excel.manager.context import GlobalContext
from xml2excel.utils.flatten_xml import PrefixMode


class Values(StrEnum):
    NONE = 'Nenhuma'
    CLOSEST = 'Apenas Tag Pai'
    ALL = 'Todas as Tags Pai'


class PrefixOption(ctk.CTkFrame):
    VALUES: list[str] = [
        Values.NONE,
        Values.CLOSEST,
        Values.ALL,
    ]

    def __init__(self, master, ctx: GlobalContext, **kwargs):
        self._ctx = ctx

        super().__init__(master, **kwargs)

        self._label = ctk.CTkLabel(self, text='Modo de Prefixo:')
        self._label.pack(anchor=tk.W, side=tk.TOP)

        self._combobox = ctk.CTkComboBox(
            self, values=self.VALUES, command=self._command
        )
        self._combobox.pack(anchor=tk.W, side=tk.BOTTOM)

        value = self.VALUES[self._ctx.config.prefix_mode]
        self._combobox.set(value)

    def _command(self, value: str) -> None:
        match value:
            case Values.NONE:
                self._ctx.config.prefix_mode = PrefixMode.NONE
            case Values.CLOSEST:
                self._ctx.config.prefix_mode = PrefixMode.CLOSEST
            case Values.ALL:
                self._ctx.config.prefix_mode = PrefixMode.ALL
