from enum import StrEnum
from pathlib import Path

from PySide6.QtCore import QObject, Signal

from xml2excel.aliases import AnyPath
from xml2excel.utils.path import resource_path


class Themes(StrEnum):
    DARK = 'dark'
    LIGHT = 'light'


class DarkTheme(StrEnum):
    TEXT = '#e5e5e5'
    TEXT_DISABLED = '#b2b2b2'
    BACKGROUND = '#0a0a0a'
    BORDER = '#282828'
    PRIMARY = '#1c1c1c'
    CHECK_ICON = f'url({resource_path("icons/check_dark.svg")})'
    CHEVRON_DOWN_ICON = f'url({resource_path("icons/chevron-down_dark.svg")})'
    FOLDER_UP_ICON = f'url({resource_path("icons/folder-up_dark.svg")})'
    FILE_DOWN_ICON = f'url({resource_path("icons/file-down_dark.svg")})'


class LightTheme(StrEnum):
    TEXT = '#171717'
    TEXT_DISABLED = '#4a4a4a'
    BACKGROUND = '#ffffff'
    BORDER = '#e5e5e5'
    PRIMARY = '#f5f5f5'
    CHECK_ICON = f'url({resource_path("icons/check_light.svg")})'
    CHEVRON_DOWN_ICON = f'url({resource_path("icons/chevron-down_light.svg")})'
    FOLDER_UP_ICON = f'url({resource_path("icons/folder-up_light.svg")})'
    FILE_DOWN_ICON = f'url({resource_path("icons/file-down_light.svg")})'


class Theme(QObject):
    changed = Signal(Themes)

    def __init__(self):
        super().__init__()

        self.theme = Themes.LIGHT

    def toggle(self):
        theme = Themes.DARK if self.theme == Themes.LIGHT else Themes.LIGHT

        self.theme = theme
        self.changed.emit(theme)

    def read_stylesheet(self, path: AnyPath) -> str | None:
        colors = DarkTheme if self.theme == Themes.DARK else LightTheme

        theme = {color.name: color.value for color in colors}

        stylesheet = None

        if Path(path).exists():
            with open(path, 'r', encoding='utf-8') as file:
                stylesheet = file.read().format(**theme)

        return stylesheet
