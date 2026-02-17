from os import PathLike
from pathlib import Path
from typing import TypeAlias

from pandas import DataFrame

PathTuple: TypeAlias = tuple[Path, ...]

AnyPath: TypeAlias = str | PathLike[str]
AnyPathTuple: TypeAlias = tuple[AnyPath, ...]

DataFrameTuple: TypeAlias = tuple[DataFrame, ...]
