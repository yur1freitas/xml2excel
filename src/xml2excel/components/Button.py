from customtkinter import CTkButton


class Button(CTkButton):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('height', 32)

        super().__init__(master, **kwargs)
