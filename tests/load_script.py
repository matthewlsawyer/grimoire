"""Load Grimoire skill scripts as modules for unittest."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

GRIMOIRE_ROOT = Path(__file__).resolve().parents[1]


def load_script(rel_path: str, module_name: str) -> ModuleType:
    path = GRIMOIRE_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod
