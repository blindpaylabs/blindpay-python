"""Every ```python block in README.md, wrapped into ``tests/readme_snippets.py`` so pyright (strict) and mypy check it.

Each block becomes the body of an ``async def``. Names a block uses but doesn't define (``blindpay``, ``request``,
``secret``, ...) become typed parameters. The committed file must equal the rendered one, so a README edit that isn't
re-rendered fails here, and a README snippet that doesn't type-check fails the type-check job. Re-render with:

    uv run --python 3.13 python tests/test_readme_snippets.py
"""

import re
import textwrap
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUTPUT = Path(__file__).resolve().parent / "readme_snippets.py"

# Free names README snippets rely on, with the type a reader would have in hand.
PARAMETERS: Dict[str, str] = {
    "blindpay": "BlindPay",
    "blindpay_sync": "BlindPaySync",
    "quote_input": "CreateTransferQuoteInput",
    "request": "Any",
    "secret": "str",
    "raw_body": "bytes",
    "abort": "Callable[[int], NoReturn]",
}

HEADER = '''"""GENERATED from README.md by tests/test_readme_snippets.py. Do not edit: edit the README and re-render."""
# ruff: noqa
# pyright: reportUnusedImport=false, reportUnusedVariable=false, reportUnusedFunction=false

from typing import Any, Callable, NoReturn

from blindpay import BlindPay, BlindPaySync, CreateTransferQuoteInput
'''


def blocks() -> List[str]:
    return re.findall(r"^```python\n(.*?)^```", README.read_text(), flags=re.S | re.M)


def _defines(name: str, block: str) -> bool:
    return bool(re.search(rf"(^|\s)({name}\s*=|as\s+{name}\b)", block, flags=re.M))


def render() -> str:
    functions: List[str] = []
    for number, block in enumerate(blocks(), start=1):
        params = [
            f"{name}: {annotation}"
            for name, annotation in PARAMETERS.items()
            if re.search(rf"\b{name}\b", block) and not _defines(name, block)
        ]
        signature = f"async def readme_block_{number}({', '.join(params)}) -> None:"
        functions.append(signature + "\n" + textwrap.indent(block.rstrip("\n"), "    ") + "\n")
    return HEADER + "\n\n" + "\n\n".join(functions)


def test_every_readme_block_is_rendered():
    assert len(blocks()) >= 10
    assert OUTPUT.read_text() == render(), "README.md changed: re-render with `python tests/test_readme_snippets.py`"


if __name__ == "__main__":
    OUTPUT.write_text(render())
