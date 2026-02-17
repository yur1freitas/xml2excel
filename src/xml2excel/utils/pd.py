from pathlib import Path
from typing import TypeAlias

import pandas as pd
from lxml import etree

from xml2excel.aliases import AnyPath
from xml2excel.consts import FileExtensions
from xml2excel.utils.flatten_xml import PrefixMode, flatten_xml


def export_df(path: AnyPath, df: pd.DataFrame, **kwargs) -> None:
    ext = Path(path).suffix

    match ext:
        case FileExtensions.EXCEL:
            df.to_excel(path, **kwargs)
        case FileExtensions.CSV:
            df.to_csv(path, **kwargs)
        case _:
            raise ValueError(f'Extensão de arquivo inválida: {ext}')


XMLNamespaces: TypeAlias = dict[str | None, str]


def xml2df(
    filepath: AnyPath,
    xpath: str = './',
    namespaces: XMLNamespaces | None = None,
    prefix_mode: PrefixMode = PrefixMode.CLOSEST,
) -> pd.DataFrame:
    parser = etree.XMLParser(encoding='utf-8', recover=True)

    tree = etree.parse(filepath, parser)
    nodes = tree.findall(xpath, namespaces)

    data = (flatten_xml(node, prefix_mode) for node in nodes)

    return pd.DataFrame(data)
