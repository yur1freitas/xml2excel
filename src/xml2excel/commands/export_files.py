from dataclasses import dataclass

from xml2excel.aliases import AnyPath, AnyPathTuple
from xml2excel.utils.flatdict2excel import FlatDict2Excel
from xml2excel.utils.xml2flatdict import XMLData


@dataclass
class ExportFilesInput:
    data: tuple[XMLData]
    output: AnyPath | AnyPathTuple
    merge: bool = True
    index: bool = False
    ignore_columns: list[str] | None = None


@dataclass
class ExportFilesOutput:
    merged: bool


def export_files(input: ExportFilesInput) -> ExportFilesOutput:
    if not isinstance(input.data, tuple):
        raise ValueError('O parâmetro "data" deve ser uma tupla de DataFrames')

    if input.merge:
        if isinstance(input.output, tuple):
            raise ValueError(
                'O parâmetro "path" deve ser um caminho de arquivo válido quando merge=True'
            )

        flatdict2excel = FlatDict2Excel(input.output, input.ignore_columns)
        flatdict2excel(*input.data)

        return ExportFilesOutput(merged=input.merge)

    if not isinstance(input.output, tuple):
        raise ValueError(
            'O parâmetro "path" deve ser uma tupla de Path quando merge=False'
        )

    if len(input.data) != len(input.output):
        raise ValueError(
            'O número de DataFrames não corresponde ao número de caminhos de saída'
        )

    for data, filepath in zip(input.data, input.output):
        flatdict2excel = FlatDict2Excel(filepath, input.ignore_columns)
        flatdict2excel(*data)

    return ExportFilesOutput(merged=input.merge)
