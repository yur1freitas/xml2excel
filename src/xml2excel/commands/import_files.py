from os.path import isdir, isfile
from pathlib import Path
from typing import Iterator

from pandas import DataFrame

from xml2excel.aliases import AnyPath
from xml2excel.consts import FileGlobs
from xml2excel.utils.flatten_xml import PrefixMode
from xml2excel.utils.path import find_files, isxml
from xml2excel.utils.pd import xml2df


def import_files(
    path: AnyPath,
    recursive: bool = False,
    prefix_mode: PrefixMode = PrefixMode.CLOSEST,
) -> Iterator[tuple[Path, DataFrame]]:
    if isfile(path) and isxml(path):
        yield path, xml2df(filepath=path, prefix_mode=prefix_mode)

    elif isdir(path):
        for filepath in find_files(path, FileGlobs.XML.value, recursive):
            yield filepath, xml2df(filepath=filepath, prefix_mode=prefix_mode)

    else:
        raise ValueError(
            'O caminho especificado não aponta para um diretório ou arquivo'
        )
