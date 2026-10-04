# -*- coding: utf-8 -*-
"""Build am.json / ti.json from en.json + UI patches + long-body locale files."""

from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOC = ROOT / "content" / "locales"

LONG_KEYS = [
    "home",
    "about",
    "contact",
    "help",
    "fallback",
    "gbv.menu",
    "gbv.what",
    "gbv.rights",
    "gbv.safety",
    "gbv.support",
    "gbv.help",
    "peace.menu",
    "peace.why",
    "peace.dialogue",
    "peace.youth",
    "rights.menu",
    "rights.basics",
    "rights.women_youth",
    "rights.engage",
    "quiz.intro",
    "quiz.gbv_result",
    "quiz.peace_result",
    "quiz.rights_result",
    "quiz.about_result",
]


def get_path(d: dict, dotted: str):
    cur = d
    for p in dotted.split("."):
        cur = cur[p]
    return cur


def set_path(d: dict, dotted: str, value) -> None:
    parts = dotted.split(".")
    cur = d
    for p in parts[:-1]:
        cur = cur[p]
    cur[parts[-1]] = value


def apply_patches(base: dict, patches: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in patches.items():
        set_path(out, key, value)
    return out


def apply_bodies(data: dict, bodies: dict, en: dict) -> None:
    for key in LONG_KEYS:
        if key in bodies:
            set_path(data, key, bodies[key])
        else:
            # keep English body if translation missing
            set_path(data, key, get_path(en, key))


def main() -> None:
    en = json.loads((LOC / "en.json").read_text(encoding="utf-8"))
    am_patches = json.loads((LOC / "patches_am.json").read_text(encoding="utf-8"))
    ti_patches = json.loads((LOC / "patches_ti.json").read_text(encoding="utf-8"))

    am_bodies_path = LOC / "bodies_am.json"
    ti_bodies_path = LOC / "bodies_ti.json"
    am_bodies = (
        json.loads(am_bodies_path.read_text(encoding="utf-8"))
        if am_bodies_path.exists()
        else {}
    )
    ti_bodies = (
        json.loads(ti_bodies_path.read_text(encoding="utf-8"))
        if ti_bodies_path.exists()
        else {}
    )

    am = apply_patches(en, am_patches)
    ti = apply_patches(en, ti_patches)
    apply_bodies(am, am_bodies, en)
    apply_bodies(ti, ti_bodies, en)

    (LOC / "am.json").write_text(
        json.dumps(am, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (LOC / "ti.json").write_text(
        json.dumps(ti, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote am.json and ti.json")


if __name__ == "__main__":
    main()
