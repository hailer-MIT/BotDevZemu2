"""SSR Telegram info bot — pitch preview for Sirius for Sustainable Resilience."""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from content.guides import (
    GBV_MENU_KEYS,
    GBV_PAGES,
    PEACE_MENU_KEYS,
    PEACE_PAGES,
    QUIZ,
    RIGHTS_MENU_KEYS,
    RIGHTS_PAGES,
)
from content.org import ABOUT_TEXT, CONTACT_TEXT, FALLBACK_TEXT, HELP_TEXT, HOME_TEXT

load_dotenv()
TOKEN = os.environ["BOT_TOKEN"]

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ---------- Keyboards ----------


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("About SSR", callback_data="menu:about")],
            [
                InlineKeyboardButton("GBV Info", callback_data="gbv:menu"),
                InlineKeyboardButton("Peacebuilding", callback_data="peace:menu"),
            ],
            [InlineKeyboardButton("Human Rights", callback_data="rights:menu")],
            [InlineKeyboardButton("Find your path", callback_data="quiz:start")],
            [
                InlineKeyboardButton("Contact SSR", callback_data="menu:contact"),
                InlineKeyboardButton("Help", callback_data="menu:help"),
            ],
        ]
    )


def home_only_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Main menu", callback_data="menu:home")]]
    )


def topic_menu_keyboard(prefix: str, items: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(label, callback_data=f"{prefix}:{key}")]
        for key, label in items
    ]
    rows.append([InlineKeyboardButton("Main menu", callback_data="menu:home")])
    return InlineKeyboardMarkup(rows)


def page_keyboard(back_to: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Back", callback_data=back_to),
                InlineKeyboardButton("Main menu", callback_data="menu:home"),
            ]
        ]
    )


def quiz_options_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(opt["label"], callback_data=opt["id"])]
        for opt in QUIZ["options"]
    ]
    rows.append([InlineKeyboardButton("Main menu", callback_data="menu:home")])
    return InlineKeyboardMarkup(rows)


def quiz_result_keyboard(goto: str, goto_label: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(goto_label, callback_data=goto)],
            [
                InlineKeyboardButton("Try again", callback_data="quiz:start"),
                InlineKeyboardButton("Main menu", callback_data="menu:home"),
            ],
        ]
    )


# ---------- Screen helpers ----------


async def show_home(update: Update, *, edit: bool) -> None:
    markup = main_menu_keyboard()
    if edit and update.callback_query:
        await update.callback_query.edit_message_text(
            HOME_TEXT, reply_markup=markup, parse_mode=ParseMode.HTML
        )
    elif update.message:
        await update.message.reply_text(
            HOME_TEXT, reply_markup=markup, parse_mode=ParseMode.HTML
        )


async def show_static(query, text: str, markup: InlineKeyboardMarkup) -> None:
    await query.edit_message_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)


def page_text(pages: dict, key: str) -> str:
    return pages[key]["body"]


async def show_topic(query, prefix: str, key: str, pages: dict, menu_keys: list) -> None:
    if key not in pages:
        await query.edit_message_text(
            "Sorry, that page was not found.\n\nTap Main menu to continue.",
            reply_markup=home_only_keyboard(),
        )
        return
    if key == "menu":
        await show_static(
            query,
            page_text(pages, "menu"),
            topic_menu_keyboard(prefix, menu_keys),
        )
    else:
        await show_static(
            query,
            page_text(pages, key),
            page_keyboard(f"{prefix}:menu"),
        )


# ---------- Handlers ----------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Brand-first home menu."""
    await show_home(update, edit=False)


async def on_unexpected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guide users who type free text or send files/photos back to the menu."""
    if not update.message:
        return
    await update.message.reply_text(
        FALLBACK_TEXT,
        reply_markup=main_menu_keyboard(),
        parse_mode=ParseMode.HTML,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data or ""

    if data == "menu:home":
        await show_home(update, edit=True)
        return

    if data == "menu:about":
        await show_static(query, ABOUT_TEXT, home_only_keyboard())
        return

    if data == "menu:contact":
        await show_static(query, CONTACT_TEXT, home_only_keyboard())
        return

    if data == "menu:help":
        await show_static(query, HELP_TEXT, home_only_keyboard())
        return

    if data == "quiz:start":
        text = f"{QUIZ['intro']}\n\n<b>{QUIZ['question']}</b>"
        await show_static(query, text, quiz_options_keyboard())
        return

    for opt in QUIZ["options"]:
        if data == opt["id"]:
            await show_static(
                query,
                opt["result"],
                quiz_result_keyboard(opt["goto"], opt["goto_label"]),
            )
            return

    if data.startswith("gbv:"):
        await show_topic(query, "gbv", data.split(":", 1)[1], GBV_PAGES, GBV_MENU_KEYS)
        return

    if data.startswith("peace:"):
        await show_topic(
            query, "peace", data.split(":", 1)[1], PEACE_PAGES, PEACE_MENU_KEYS
        )
        return

    if data.startswith("rights:"):
        await show_topic(
            query, "rights", data.split(":", 1)[1], RIGHTS_PAGES, RIGHTS_MENU_KEYS
        )
        return


# ---------- Main ----------


def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    # Any free text, photo, file, sticker, etc. → short how-to + main menu
    app.add_handler(MessageHandler(~filters.COMMAND, on_unexpected))
    print("SSR bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
