from os import PathLike
from pathlib import Path
from typing import TypeAlias

PathTuple: TypeAlias = tuple[Path, ...]

AnyPath: TypeAlias = str | PathLike[str]
AnyPathTuple: TypeAlias = tuple[AnyPath, ...]
