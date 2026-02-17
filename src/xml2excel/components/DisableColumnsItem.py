import tkinter as tk
from typing import Callable

import customtkinter as ctk


class DisableColumnsItem(ctk.CTkFrame):
    def __init__(
        self,
        master,
        text: str = '',
        command: Callable | None = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self._text: str = text
        self._command = command

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._build()

    def _build(self):
        name = ctk.CTkLabel(self, text=self._text, height=20)

        name.grid(column=0, row=0, sticky=tk.W)

        checkbox = ctk.CTkCheckBox(
            self,
            text='',
            command=self._command,
            width=16,
            height=16,
            checkbox_width=16,
            checkbox_height=16,
        )

        checkbox.grid(column=1, row=0, sticky=tk.E)
        checkbox.select()
