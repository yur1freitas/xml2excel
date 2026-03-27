import re
import sys
from pathlib import Path
from typing import Iterator

from xml2excel.aliases import AnyPath
from xml2excel.consts import FileExtensions


def isxml(path: AnyPath) -> bool:
    return Path(path).suffix == FileExtensions.XML


DEFAULT_PATH_DELIMITER = '/'


def normalize_path(path: AnyPath) -> Path:
    pattern = r'[\\/]+'

    return Path(re.sub(pattern, DEFAULT_PATH_DELIMITER, str(path)))


def resource_path(path: AnyPath) -> Path:
    if hasattr(sys, '_MEIPASS'):
        return normalize_path(Path(sys._MEIPASS) / path)

    return normalize_path(Path().resolve() / path)


def resolve_filepath(
    root: AnyPath,
    filename: str,
    ext: FileExtensions | None = None,
) -> Path:
    filepath = Path(root) / filename

    if ext is not None:
        filepath = filepath.with_suffix(ext.value)

    return filepath


def find_files(
    root: AnyPath,
    glob: str,
    recursive: bool = True,
) -> Iterator[Path]:
    path = Path(root)

    if recursive:
        return path.rglob(glob)

    return path.glob(glob)
