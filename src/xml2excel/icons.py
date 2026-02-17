from enum import Enum

from PIL import Image

from xml2excel.utils.path import resource_path


class Icons(Enum):
    FOLDER_UP = Image.open(resource_path('public/folder-up.png'))
    FILE_DOWN = Image.open(resource_path('public/file-down.png'))
