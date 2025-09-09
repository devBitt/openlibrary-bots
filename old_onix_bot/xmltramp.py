from typing import TypeAlias, Any, Union, Iterator
from io import StringIO
from urllib.request import urlopen
import xml.parsers.expat

# In Python 3, "unicode" == str
unicode: TypeAlias = str


class Node:
    def __init__(self, name: str, attrs: dict[str, str] | None = None, children: list[Any] | None = None) -> None:
        self._name = name
        self._attrs = attrs or {}
        self._children = children or []

    def __getitem__(self, key: Union[int, str]) -> Any:
        if isinstance(key, int):
            return self._children[key]
        return self._attrs.get(key)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._children)

    def __repr__(self) -> str:
        return f"<Node {self._name} {self._attrs} children={len(self._children)}>"


def seed(source: Any) -> Node:
    parser = xml.parsers.expat.ParserCreate()
    stack: list[Node] = []

    def start_element(name: str, attrs: dict[str, str]) -> None:
        node = Node(name, dict(attrs))
        if stack:
            stack[-1]._children.append(node)
        stack.append(node)

    def end_element(name: str) -> None:
        if len(stack) > 1:
            stack.pop()

    def char_data(data: str) -> None:
        if stack and data.strip():
            stack[-1]._children.append(data)

    parser.StartElementHandler = start_element
    parser.EndElementHandler = end_element
    parser.CharacterDataHandler = char_data

    if isinstance(source, (str, bytes)):
        parser.Parse(source, True)
    else:
        parser.Parse(source.read(), True)

    return stack[0]


def parse(text: str) -> Node:
    return seed(StringIO(text))


def load(url: str) -> Node:
    return seed(urlopen(url))


# === Simple unittest ===
def unittest() -> None:
    doc = parse("<doc>a<baz>f<b>o</b>ob<b>a</b>r</baz>a</doc>")
    print("Parsed root:", doc)
    for child in doc:
        print("Child:", child)


if __name__ == "__main__":
    unittest()
