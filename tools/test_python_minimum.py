# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tools/test_python_minimum.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The oldest Python that pyproject.toml promises is the one the code can be read by and the one the CI tests.

Run it with any Python: it reads every source file with the grammar of the promised minimum (``ast.parse`` with ``feature_version``), looks for standard-library
modules that appeared after it, and checks that the test matrix of the workflow names that minimum."""
from __future__ import annotations

import ast
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".venv", "venv", "node_modules", "build", "dist", "__pycache__", "target"}
# standard-library modules and the Python that added them: using one while promising an older Python breaks at import
NEWER_MODULES = {"tomllib": (3, 11), "zoneinfo": (3, 9)}


def minimum() -> tuple[int, int]:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    found = re.search(r'(?m)^requires-python\s*=\s*">=\s*(\d+)\.(\d+)', text)
    if not found:
        raise AssertionError("pyproject.toml has no requires-python = \">=X.Y\"")
    return int(found.group(1)), int(found.group(2))


def sources() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.py") if not SKIP & set(p.relative_to(ROOT).parts))


class PythonMinimumTests(unittest.TestCase):
    def test_the_promise_is_a_version_this_check_understands(self) -> None:
        self.assertGreaterEqual(minimum(), (3, 8))

    def test_every_source_is_read_by_the_grammar_of_the_minimum(self) -> None:
        low = minimum()
        for path in sources():
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path), feature_version=low)
            except SyntaxError as error:
                self.fail(f"{path.relative_to(ROOT)} uses syntax newer than Python {low[0]}.{low[1]}: {error}")

    def test_no_module_newer_than_the_minimum_is_imported(self) -> None:
        low = minimum()
        for path in sources():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                names = [a.name.split(".")[0] for a in node.names] if isinstance(node, ast.Import) else [node.module.split(".")[0]] if isinstance(node, ast.ImportFrom) and node.module and node.level == 0 else []
                for name in names:
                    if NEWER_MODULES.get(name, (0, 0)) > low:
                        self.fail(f"{path.relative_to(ROOT)} imports {name}, which needs Python {NEWER_MODULES[name][0]}.{NEWER_MODULES[name][1]}")

    def test_the_workflow_tests_the_minimum(self) -> None:
        low = minimum()
        text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        matrix = re.search(r"python-version:\s*\[([^\]]*)\]", text)
        self.assertIsNotNone(matrix, "ci.yml has no matrix of Python versions")
        versions = re.findall(r'"(\d+\.\d+)"', matrix.group(1))
        self.assertIn(f"{low[0]}.{low[1]}", versions)

    def test_this_python_is_not_older_than_the_minimum(self) -> None:
        self.assertGreaterEqual(sys.version_info[:2], minimum())


if __name__ == "__main__":
    unittest.main()
