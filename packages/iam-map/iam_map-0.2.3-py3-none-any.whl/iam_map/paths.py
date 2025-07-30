# iam_anal/paths.py
from pathlib import Path
import os


def _ensure(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


# Resolve once, when the package is imported
DATA_DIR = _ensure(Path(os.getenv("DATA_DIR", Path.cwd() / "data")).expanduser())
OUTPUT_DIR = _ensure(Path(os.getenv("OUTPUT_DIR", Path.cwd() / "output")).expanduser())
