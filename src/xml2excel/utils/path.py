import sys
from pathlib import Path

from xml2excel.aliases import AnyPath, PathTuple
from xml2excel.consts import FileExtensions


def isxml(path: AnyPath) -> bool:
    return Path(path).suffix == FileExtensions.XML


def resource_path(path: AnyPath) -> Path:
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / path

    return Path().resolve() / path


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
) -> PathTuple:
    path = Path(root)

    if recursive:
        return tuple(path.rglob(glob))

    return tuple(path.glob(glob))
