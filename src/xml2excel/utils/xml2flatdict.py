from collections import defaultdict
from typing import Iterator, TypeAlias, Union, cast

from lxml import etree

from xml2excel.aliases import AnyPath
from xml2excel.utils.flatdict import flatdict

XMLData: TypeAlias = flatdict[Union[str, list, 'XMLData']]


class DeepVisits:
    def __init__(self) -> None:
        self.depth = 0
        self.visits = defaultdict(set)

    def up(self) -> tuple[int, set[str]]:
        prev_depth = self.depth + 1

        if prev_depth in self.visits:
            self.visits.pop(prev_depth)

        self.depth -= 1

        return self.depth, self.visits[self.depth]

    def down(self) -> tuple[int, set[str]]:
        self.depth += 1

        return self.depth, self.visits[self.depth]


def xml2flatdict(
    filepath: AnyPath,
    attrs: bool = False,
    namespace: bool = False,
) -> XMLData:
    tree = etree.iterparse(
        filepath,
        events=('start', 'end'),
        encoding='utf-8',
        recover=True,
        remove_blank_text=True,
    )

    tree = cast(Iterator[tuple[str, etree.Element]], tree)

    visits = DeepVisits()

    out = flatdict()
    stack = [out]

    is_text_value = False

    for event, elem in tree:
        qname = etree.QName(str(elem.tag))
        tag = qname.localname

        if event == 'end':
            if not is_text_value:
                stack.pop()

            visits.up()
            elem.clear()

            is_text_value = False

            continue

        value = elem.text if elem.text is not None else flatdict()
        target: flatdict | list = stack[-1]

        _, tags = visits.down()

        is_text_value = bool(elem.text)

        if isinstance(value, flatdict):
            if attrs:
                value.update({f'@{k}': v for k, v in elem.attrib.items()})

            if namespace:
                value.update({'@ns': elem.nsmap.get(None)})

        if tag in tags:
            if isinstance(target, flatdict) and tag in target:
                prop_value = target[tag]

                if isinstance(prop_value, list):
                    prop_value.append(value)
                else:
                    target[tag] = [target[tag], value]
        else:
            target[tag] = value

        if not is_text_value:
            stack.append(value)

        tags.add(tag)

    return out
