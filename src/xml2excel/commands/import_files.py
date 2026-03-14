from os.path import isdir, isfile
from pathlib import Path
from typing import Iterator

from xml2excel.aliases import AnyPath
from xml2excel.consts import FileGlobs
from xml2excel.utils.path import find_files, isxml
from xml2excel.utils.xml2flatdict import XMLData, xml2flatdict


def import_files(
    path: AnyPath,
    recursive: bool = False,
) -> Iterator[tuple[Path, XMLData]]:
    if isfile(path) and isxml(path):
        yield path, xml2flatdict(path)

    elif isdir(path):
        for filepath in find_files(path, FileGlobs.XML.value, recursive):
            yield filepath, xml2flatdict(filepath)

    else:
        raise ValueError(
            'O caminho especificado não aponta para um diretório ou arquivo'
        )
