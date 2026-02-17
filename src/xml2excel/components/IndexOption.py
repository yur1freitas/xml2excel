from xml2excel.components.CheckBox import CheckBox
from xml2excel.manager.context import GlobalContext


class IndexOption(CheckBox):
    def __init__(self, master, ctx: GlobalContext, **kwargs):
        self._ctx = ctx

        super().__init__(master, command=self._command, **kwargs)

        if self._ctx.config.index:
            self.select()

        if self._text_label:
            self._text_label.configure(wraplength=300)

    def _command(self):
        self._ctx.config.index = bool(self.get())
