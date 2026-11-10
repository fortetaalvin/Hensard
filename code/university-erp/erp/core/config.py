"""Load the institution's structure from institution.yaml (path overridable with ERP_INSTITUTION)."""

import functools
import os
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]


@functools.lru_cache(maxsize=1)
def institution() -> dict:
    path = pathlib.Path(os.environ.get("ERP_INSTITUTION", ROOT / "institution.yaml"))
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    for key in ("name", "short_name", "faculties", "sessions", "grading", "credit_load"):
        if key not in cfg:
            raise ValueError(f"institution.yaml is missing '{key}'")
    return cfg


def grade_for(score: float) -> tuple[str, int]:
    """Map a score to (grade, grade point) using the institution's scale."""
    for band in sorted(institution()["grading"], key=lambda b: -b["min"]):
        if score >= band["min"]:
            return band["grade"], band["point"]
    raise ValueError(f"no grade band for score {score}")
