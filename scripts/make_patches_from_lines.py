# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

LOC = Path(__file__).resolve().parents[1] / "content" / "locales"

AM_KEYS = [
    "lang_picker_title",
    "lang_picker_body",
    "not_found",
    "menu.about",
    "menu.gbv",
    "menu.peace",
    "menu.rights",
    "menu.quiz",
    "menu.contact",
    "menu.help",
    "menu.language",
    "nav.back",
    "nav.main",
    "nav.try_again",
    "gbv.btn.what",
    "gbv.btn.rights",
    "gbv.btn.safety",
    "gbv.btn.support",
    "gbv.btn.help",
    "peace.btn.why",
    "peace.btn.dialogue",
    "peace.btn.youth",
    "rights.btn.basics",
    "rights.btn.women_youth",
    "rights.btn.engage",
    "quiz.question",
    "quiz.gbv_label",
    "quiz.peace_label",
    "quiz.rights_label",
    "quiz.about_label",
    "quiz.gbv_goto",
    "quiz.peace_goto",
    "quiz.rights_goto",
    "quiz.about_goto",
]

TI_KEYS = AM_KEYS  # same structure


def load_nonempty_lines(path: Path) -> list[str]:
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            lines.append(line.strip())
    return lines


def build_patch(keys: list[str], values: list[str]) -> dict:
    if len(values) < len(keys):
        raise SystemExit(f"Need {len(keys)} values, got {len(values)} from lines file")
    values = values[: len(keys)]
    data = dict(zip(keys, values))
    title = data.pop("lang_picker_title")
    body = data.pop("lang_picker_body")
    data["lang_picker"] = f"<b>{title}</b>\n\n{body}"
    return data


def main() -> None:
    am_lines = load_nonempty_lines(LOC / "_am_lines.txt")
    # Deduplicate consecutive duplicates caused by heredoc corruption
    cleaned: list[str] = []
    for line in am_lines:
        if cleaned and cleaned[-1] == line:
            continue
        cleaned.append(line)

    am = build_patch(AM_KEYS, cleaned)
    (LOC / "patches_am.json").write_text(
        json.dumps(am, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote patches_am.json with", len(am), "keys")

    ti_path = LOC / "_ti_lines.txt"
    if ti_path.exists():
        ti_lines = load_nonempty_lines(ti_path)
        cleaned_ti: list[str] = []
        for line in ti_lines:
            if cleaned_ti and cleaned_ti[-1] == line:
                continue
            cleaned_ti.append(line)
        ti = build_patch(TI_KEYS, cleaned_ti)
        (LOC / "patches_ti.json").write_text(
            json.dumps(ti, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("wrote patches_ti.json with", len(ti), "keys")


if __name__ == "__main__":
    main()
