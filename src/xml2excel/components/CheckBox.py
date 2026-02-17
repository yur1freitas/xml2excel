from customtkinter import CTkCheckBox


class CheckBox(CTkCheckBox):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('width', 20)
        kwargs.setdefault('height', 20)
        kwargs.setdefault('checkbox_width', 20)
        kwargs.setdefault('checkbox_height', 20)

        super().__init__(master, **kwargs)
