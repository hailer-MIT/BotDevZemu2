"""Load locale JSON and resolve translated strings / keyboards."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

LOCALES_DIR = Path(__file__).resolve().parent / "locales"
SUPPORTED = ("en", "am", "ti")
DEFAULT_LANG = "en"

GBV_PAGE_KEYS = ("what", "rights", "safety", "support", "help")
PEACE_PAGE_KEYS = ("why", "dialogue", "youth", "rumors", "skills")
RIGHTS_PAGE_KEYS = ("basics", "women_youth", "engage", "advocacy_steps", "duty_bearers")
RESOURCE_TOPICS = ("gbv", "peace", "rights")
QUIZ_OPTIONS = (
    ("gbv", "gbv:menu"),
    ("peace", "peace:menu"),
    ("rights", "rights:menu"),
    ("about", "menu:about"),
)

_CACHE: dict[str, dict[str, Any]] | None = None


def _load_locales() -> dict[str, dict[str, Any]]:
    global _CACHE
    if _CACHE is None:
        _CACHE = {}
        for code in SUPPORTED:
            path = LOCALES_DIR / f"{code}.json"
            with path.open(encoding="utf-8") as f:
                _CACHE[code] = json.load(f)
    return _CACHE


def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    lang = context.user_data.get("lang")
    if lang in SUPPORTED:
        return lang
    return DEFAULT_LANG


def has_lang(context: ContextTypes.DEFAULT_TYPE) -> bool:
    return context.user_data.get("lang") in SUPPORTED


def set_lang(context: ContextTypes.DEFAULT_TYPE, code: str) -> None:
    if code in SUPPORTED:
        context.user_data["lang"] = code


def t(lang: str, key: str) -> str:
    """Resolve dotted key; fall back to English, then to the key itself."""
    locales = _load_locales()
    for code in (lang if lang in SUPPORTED else DEFAULT_LANG, DEFAULT_LANG):
        node: Any = locales.get(code, {})
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                node = None
                break
            node = node[part]
        if isinstance(node, str):
            return node
    return key


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("English", callback_data="lang:en")],
            [InlineKeyboardButton("አማርኛ", callback_data="lang:am")],
            [InlineKeyboardButton("ትግርኛ", callback_data="lang:ti")],
        ]
    )


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t(lang, "menu.about"), callback_data="menu:about")],
            [
                InlineKeyboardButton(t(lang, "menu.gbv"), callback_data="gbv:menu"),
                InlineKeyboardButton(t(lang, "menu.peace"), callback_data="peace:menu"),
            ],
            [InlineKeyboardButton(t(lang, "menu.rights"), callback_data="rights:menu")],
            [InlineKeyboardButton(t(lang, "menu.quiz"), callback_data="quiz:start")],
            [
                InlineKeyboardButton(t(lang, "menu.resources"), callback_data="res:menu"),
                InlineKeyboardButton(t(lang, "menu.request"), callback_data="ref:start"),
            ],
            [
                InlineKeyboardButton(t(lang, "menu.involve"), callback_data="vol:start"),
                InlineKeyboardButton(t(lang, "menu.updates"), callback_data="upd:menu"),
            ],
            [
                InlineKeyboardButton(t(lang, "menu.contact"), callback_data="menu:contact"),
                InlineKeyboardButton(t(lang, "menu.help"), callback_data="menu:help"),
            ],
            [InlineKeyboardButton(t(lang, "menu.language"), callback_data="menu:language")],
        ]
    )


def home_only_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(t(lang, "nav.main"), callback_data="menu:home")]]
    )


def topic_menu_keyboard(lang: str, prefix: str, page_keys: tuple[str, ...]) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                t(lang, f"{prefix}.btn.{key}"),
                callback_data=f"{prefix}:{key}",
            )
        ]
        for key in page_keys
    ]
    rows.append(
        [InlineKeyboardButton(t(lang, "nav.main"), callback_data="menu:home")]
    )
    return InlineKeyboardMarkup(rows)


def page_keyboard(
    lang: str,
    back_to: str,
    *,
    topic: str | None = None,
    page: str | None = None,
) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    if topic and page and page != "menu":
        rows.append(
            [
                InlineKeyboardButton(
                    t(lang, "feedback.yes"),
                    callback_data=f"fb:1:{topic}:{page}",
                ),
                InlineKeyboardButton(
                    t(lang, "feedback.no"),
                    callback_data=f"fb:0:{topic}:{page}",
                ),
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    t(lang, "feedback.skip"),
                    callback_data=f"fb:skip:{topic}:{page}",
                )
            ]
        )
    rows.append(
        [
            InlineKeyboardButton(t(lang, "nav.back"), callback_data=back_to),
            InlineKeyboardButton(t(lang, "nav.main"), callback_data="menu:home"),
        ]
    )
    return InlineKeyboardMarkup(rows)


def resources_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("GBV", callback_data="res:gbv")],
            [InlineKeyboardButton("Peace", callback_data="res:peace")],
            [InlineKeyboardButton("Rights", callback_data="res:rights")],
            [InlineKeyboardButton(t(lang, "nav.main"), callback_data="menu:home")],
        ]
    )


def referral_need_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t(lang, "referral.need_info"), callback_data="ref:need:info"
                )
            ],
            [
                InlineKeyboardButton(
                    t(lang, "referral.need_program"), callback_data="ref:need:program"
                )
            ],
            [
                InlineKeyboardButton(
                    t(lang, "referral.need_referral"), callback_data="ref:need:referral"
                )
            ],
            [InlineKeyboardButton(t(lang, "nav.main"), callback_data="menu:home")],
        ]
    )


def updates_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t(lang, "updates.sub"), callback_data="upd:sub")],
            [InlineKeyboardButton(t(lang, "updates.unsub"), callback_data="upd:unsub")],
            [InlineKeyboardButton(t(lang, "nav.main"), callback_data="menu:home")],
        ]
    )


def quiz_options_keyboard(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                t(lang, f"quiz.{key}_label"),
                callback_data=f"quiz:{key}",
            )
        ]
        for key, _ in QUIZ_OPTIONS
    ]
    rows.append(
        [InlineKeyboardButton(t(lang, "nav.main"), callback_data="menu:home")]
    )
    return InlineKeyboardMarkup(rows)


def quiz_result_keyboard(lang: str, option_key: str, goto: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t(lang, f"quiz.{option_key}_goto"),
                    callback_data=goto,
                )
            ],
            [
                InlineKeyboardButton(t(lang, "nav.try_again"), callback_data="quiz:start"),
                InlineKeyboardButton(t(lang, "nav.main"), callback_data="menu:home"),
            ],
        ]
    )
