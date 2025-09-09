# old_onix_bot/onix-import.py
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional, Any, List

# Ensure the current folder is in sys.path so we can import xmltramp
sys.path.append(str(Path(__file__).parent))

import xmltramp


def read_onix_file(path: str | Path) -> Optional[str]:
    """
    Reads an ONIX XML file and returns its content as a string.
    Returns None if the file doesn't exist.
    """
    file_path = Path(path)
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return None

    with file_path.open("r", encoding="utf-8") as f:
        return f.read()


def parse_onix(content: str) -> Any:
    """
    Parses ONIX XML content and returns an xmltramp node.
    """
    return xmltramp.parse(content)


def process_onix_file(path: str | Path) -> None:
    """
    Read and parse a single ONIX XML file.
    """
    content = read_onix_file(path)
    if content is None:
        return

    try:
        root = parse_onix(content)
        print(f"Parsed root node: {root}")
        # Optionally, you can print children:
        for child in getattr(root, "_dir", []):
            print(f"Child: {child}")
    except Exception as e:
        print(f"Error parsing {path}: {e}")


def main(args: Optional[List[str]] = None) -> None:
    """
    Entry point for ONIX importer.
    """
    if args is None:
        args = sys.argv[1:]

    if not args:
        print("Usage: python onix-import.py <onix_file.xml>")
        sys.exit(1)

    for filename in args:
        process_onix_file(filename)


if __name__ == "__main__":
    main()
