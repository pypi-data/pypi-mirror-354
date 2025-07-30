import json
import pathlib
from typing import Any


def read_fixture(name: str) -> dict[str, Any]:
    return json.loads(read_fixture_raw(name))


def read_fixture_raw(name: str) -> str:
    return pathlib.Path(f"test_fixtures/{name}").read_text(encoding="utf-8")
