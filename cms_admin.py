"""Lightweight admin CMS: edit English locale strings via /settext (Phase 5 starter)."""

from __future__ import annotations

import json
from pathlib import Path

from content import i18n

LOCALES_DIR = Path(__file__).resolve().parent / "content" / "locales"


def set_en_text(dotted_key: str, value: str) -> str:
    path = LOCALES_DIR / "en.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    parts = dotted_key.split(".")
    node = data
    for part in parts[:-1]:
        if part not in node or not isinstance(node[part], dict):
            node[part] = {}
        node = node[part]
    node[parts[-1]] = value
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # clear i18n cache
    i18n._CACHE = None
    return f"Updated en:{dotted_key}"
