import tkinter as tk

import customtkinter as ctk

from xml2excel.utils.path import resource_path


class App(ctk.CTk):
    DEFAULT_TITLE = 'Conversor de XML para Excel'

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        photo = tk.PhotoImage(file=resource_path('assets/xml2excel.png'))
        self.iconphoto(True, photo)

        self.title(self.DEFAULT_TITLE)
        self.geometry('1280x720')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
