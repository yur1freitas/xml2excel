from os.path import isdir, isfile

from xml2excel.aliases import AnyPath, AnyPathTuple, DataFrameTuple
from xml2excel.consts import FileGlobs
from xml2excel.utils.flatten_xml import PrefixMode
from xml2excel.utils.path import find_files, isxml
from xml2excel.utils.pd import xml2df


def import_files(
    path: AnyPath,
    recursive: bool = False,
    prefix_mode: PrefixMode = PrefixMode.CLOSEST,
) -> tuple[DataFrameTuple, AnyPathTuple]:
    if isfile(path) and isxml(path):
        data = xml2df(filepath=path, prefix_mode=prefix_mode)

        return (data,), (path,)

    if isdir(path):
        filepaths = find_files(path, FileGlobs.XML.value, recursive=recursive)

        data = tuple(
            [
                xml2df(filepath=filepath, prefix_mode=prefix_mode)
                for filepath in filepaths
            ]
        )

        return data, filepaths

    raise ValueError(
        'O caminho especificado não aponta para um diretório ou arquivo'
    )
