"""Tool registry for your mini harness. list_dir is done as an example; you write the rest."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable


class ToolError(Exception):
    pass


def safe_path(root: str, rel: str) -> str:
    """Resolve rel inside root and refuse anything that escapes it.
    TODO: this version trusts the model completely. Make it reject '../', absolute paths and symlinks out."""
    return os.path.join(root, rel)


def list_dir(root: str, path: str) -> str:
    p = safe_path(root, path)
    if not os.path.isdir(p):
        raise ToolError(f"no such directory: {path}")
    return "\n".join(sorted(os.listdir(p)))


def read_file(root: str, path: str) -> str:
    """TODO: return the file's text. Refuse secret files such as .env."""
    raise ToolError("read_file is not implemented yet")


def run_tests(root: str, target: str) -> str:
    """TODO: run `python -m pytest -q <target>` in root and return the tail of the output and the exit code."""
    raise ToolError("run_tests is not implemented yet")


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    params: dict
    run: Callable[..., str]
    needs_approval: bool = False  # True = the harness must ask a human before running it


TOOLS = {
    t.name: t
    for t in [
        Tool("list_dir", "List a directory in the repository ('.' for the root).", {"path": "string"}, list_dir),
        # TODO: register read_file and run_tests. Which one executes code, and so needs approval?
    ]
}
