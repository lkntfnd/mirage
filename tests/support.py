"""Shared helpers for the check.py tests."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable, Dict, Iterator, List, Tuple

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "skills" / "mirage" / "scripts" / "check.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "valid"

_spec = importlib.util.spec_from_file_location("mirage_check", SCRIPT)
check = importlib.util.module_from_spec(_spec)
# dataclasses resolves string annotations through sys.modules, so register before executing.
sys.modules["mirage_check"] = check
_spec.loader.exec_module(check)


def run(*argv: object) -> Tuple[int, str, str]:
    """Run check.py's main in-process; return (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = check.main([str(arg) for arg in argv])
    return code, out.getvalue(), err.getvalue()


def errors(root: Path, *extra: str) -> List[dict]:
    code, out, _ = run("check", "--root", root, "--json", *extra)
    found = json.loads(out)["errors"]
    assert code == (1 if found else 0), (code, found)
    return found


@contextlib.contextmanager
def fixture_copy() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        shutil.copytree(FIXTURE, root)
        yield root


@contextlib.contextmanager
def project(files: Dict[str, str]) -> Iterator[Path]:
    """A temporary project built from {relative path: text}; dict values become JSON."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        for rel, content in files.items():
            write(rel, content)(root)
        yield root


Mutation = Callable[[Path], None]


def edit(rel: str, old: str, new: str) -> Mutation:
    def apply(root: Path) -> None:
        path = root / rel
        text = path.read_text(encoding="utf-8")
        assert text.count(old) == 1, f"{rel} holds {text.count(old)} copies of {old!r}"
        path.write_text(text.replace(old, new), encoding="utf-8")
    return apply


def append(rel: str, extra: str) -> Mutation:
    def apply(root: Path) -> None:
        path = root / rel
        path.write_text(path.read_text(encoding="utf-8") + extra, encoding="utf-8")
    return apply


def write(rel: str, content: object) -> Mutation:
    def apply(root: Path) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        text = content if isinstance(content, str) else json.dumps(content, indent=2) + "\n"
        path.write_text(text, encoding="utf-8")
    return apply


def delete(rel: str) -> Mutation:
    def apply(root: Path) -> None:
        (root / rel).unlink()
    return apply


def edit_json(rel: str, change: Callable[[dict], None]) -> Mutation:
    def apply(root: Path) -> None:
        path = root / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return apply


def catalog_doc(doc_id: str, path: str, when: object, check_type: str = "exists", sections: Tuple[str, ...] = (),
                areas: Tuple[str, ...] = (), inputs: Tuple[Tuple[str, str], ...] = ()) -> dict:
    return {
        "id": doc_id,
        "title": doc_id.capitalize(),
        "path": path,
        "when": when,
        "check": check_type,
        "sections": [{"key": key, "title": key.capitalize()} for key in sections],
        "areas": [{"key": key, "ask": f"What about {key}?"} for key in areas],
        "inputs": [{"key": key, "title": key.capitalize(), "kind": kind} for key, kind in inputs],
    }


def synthetic_catalog(*docs: dict) -> dict:
    return {
        "version": 1,
        "component_kinds": ["website", "mobile-app", "desktop-app", "cli"],
        "flags": ["cms", "ai"],
        "lists": ["integrations", "regulated", "domain_topics"],
        "docs": list(docs),
    }


def facets(**overrides: object) -> dict:
    data = {
        "mirage_version": "0.1.0",
        "name": "Tiny Kiosk",
        "components": [{"id": "tool", "kind": "cli"}],
        "releases": ["v1"],
        "areas": ["core"],
    }
    data.update(overrides)
    return data
