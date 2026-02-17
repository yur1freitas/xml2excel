import tkinter as tk
from tkinter import ttk

import customtkinter as ctk


class ScrollArea(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        canvas = tk.Canvas(self)
        scrollbar = ctk.CTkScrollbar(
            self,
            command=canvas.yview,
        )
        scrollable = tk.Frame(canvas)

        scrollable.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')),
        )

        canvas.create_window((0, 0), window=scrollable, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = canvas
        self.scrollbar = scrollbar
        self.scrollable = scrollable
