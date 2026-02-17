from dataclasses import dataclass
from os.path import isdir, isfile

from xml2excel.aliases import AnyPath, AnyPathTuple, DataFrameTuple
from xml2excel.consts import FileGlobs
from xml2excel.utils.flatten_xml import PrefixMode
from xml2excel.utils.path import find_files, isxml
from xml2excel.utils.pd import xml2df


@dataclass
class ImportFilesInput:
    path: AnyPath
    recursive: bool = False
    prefix_mode: PrefixMode = PrefixMode.CLOSEST


@dataclass
class ImportFilesOutput:
    data: DataFrameTuple
    filepaths: AnyPathTuple


def import_files(input: ImportFilesInput) -> ImportFilesOutput:
    if isfile(input.path) and isxml(input.path):
        data = xml2df(filepath=input.path, prefix_mode=input.prefix_mode)

        return ImportFilesOutput(data=(data,), filepaths=(input.path,))

    if isdir(input.path):
        filepaths = find_files(
            input.path, FileGlobs.XML.value, recursive=input.recursive
        )

        data = tuple(
            [
                xml2df(filepath=filepath, prefix_mode=input.prefix_mode)
                for filepath in filepaths
            ]
        )

        return ImportFilesOutput(data=data, filepaths=filepaths)

    raise ValueError(
        'O caminho especificado não aponta para um diretório ou arquivo'
    )
