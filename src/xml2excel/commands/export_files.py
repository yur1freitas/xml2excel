from dataclasses import dataclass

import pandas as pd

from xml2excel.aliases import AnyPath, AnyPathTuple, DataFrameTuple
from xml2excel.utils.pd import export_df


@dataclass
class ExportFilesInput:
    data: DataFrameTuple
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

        data = pd.concat(input.data, ignore_index=True)

        if input.ignore_columns is not None:
            data = data.drop(
                columns=input.ignore_columns, inplace=False, errors='ignore'
            )

        data = data.dropna(how='all')

        export_df(input.output, data, index=input.index)

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
        if input.ignore_columns is not None:
            data = data.drop(columns=input.ignore_columns, errors='ignore')

        data = data.dropna(how='all')

        export_df(data, filepath, index=input.index)

    return ExportFilesOutput(merged=input.merge)
