from collections import OrderedDict, deque
from enum import IntEnum
from typing import TypeAlias

from lxml import etree

FlattenedXML: TypeAlias = OrderedDict[str, str]


class PrefixMode(IntEnum):
    NONE = 0
    CLOSEST = 1
    ALL = 2


def add_prefix(name: str, prefix: str | None = None) -> str:
    return f'{prefix}:{name}' if prefix is not None else name


def get_tag(node: etree.Element) -> str:
    tag = node.tag

    if not isinstance(tag, str):
        raise ValueError(f'A tag deve ser uma string: {tag}')

    return tag.split('}')[-1]


def flatten_xml(
    node: etree.Element,
    prefix_mode: PrefixMode = PrefixMode.CLOSEST,
) -> FlattenedXML:
    stack = deque[tuple[etree.Element, str | None]]([(node, None)])
    out: FlattenedXML = OrderedDict()

    while stack:
        node, parent_tag = stack.popleft()

        node_tag = get_tag(node)
        current_tag = (
            add_prefix(name=node_tag, prefix=parent_tag)
            if prefix_mode == PrefixMode.ALL
            else node_tag
        )

        for name, value in node.attrib.items():
            key = (
                add_prefix(name=name, prefix=current_tag)
                if prefix_mode != PrefixMode.NONE
                else name
            )
            out[key] = value

        txt = (node.text or '').strip()
        if txt:
            key = (
                add_prefix(name=current_tag, prefix=parent_tag)
                if prefix_mode == PrefixMode.CLOSEST
                else current_tag
            )

            out[key] = txt

        for child in node:
            stack.append((child, current_tag))

    return out
