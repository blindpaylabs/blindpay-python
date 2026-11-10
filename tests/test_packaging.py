"""Packaging regression guards: what ships in the wheel and what it reports about itself."""

from pathlib import Path

import blindpay

PACKAGE_DIR = Path(blindpay.__file__).parent


class TestPackaging:
    def test_py_typed_marker_lives_inside_the_package(self):
        # The wheel packages only src/blindpay, so a marker at the repo root never reaches users (PEP 561).
        assert (PACKAGE_DIR / "py.typed").is_file()
