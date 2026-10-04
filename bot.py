"""SSR Telegram info bot — multilingual + Phase 2–7 features."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from content.i18n import (
    GBV_PAGE_KEYS,
    PEACE_PAGE_KEYS,
    QUIZ_OPTIONS,
    RIGHTS_PAGE_KEYS,
    get_lang,
    has_lang,
    home_only_keyboard,
    language_keyboard,
    main_menu_keyboard,
    page_keyboard,
    quiz_options_keyboard,
    quiz_result_keyboard,
    referral_need_keyboard,
    resources_keyboard,
    set_lang,
    t,
    topic_menu_keyboard,
    updates_keyboard,
)
from cms_admin import set_en_text
from db import (
    add_feedback,
    add_referral,
    add_volunteer,
    get_user_lang,
    init_db,
    list_subscribers,
    log_event,
    set_subscribed,
    stats_summary,
    upsert_user_lang,
)

load_dotenv()
TOKEN = os.environ["BOT_TOKEN"]
ADMIN_IDS = {
    int(x.strip())
    for x in os.environ.get("ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
}
MEDIA_ROOT = Path(__file__).resolve().parent / "media"
STAFF_CHAT_ID = os.environ.get("STAFF_CHAT_ID", "").strip()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def _is_admin(user_id: int | None) -> bool:
    return bool(user_id and user_id in ADMIN_IDS)


async def _notify_staff(context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    targets: list[int] = []
    if STAFF_CHAT_ID.lstrip("-").isdigit():
        targets.append(int(STAFF_CHAT_ID))
    targets.extend(ADMIN_IDS)
    for chat_id in dict.fromkeys(targets):
        try:
            await context.bot.send_message(chat_id, text, parse_mode=ParseMode.HTML)
        except Exception:
            logging.exception("Failed staff notify to %s", chat_id)


# ---------- Screens ----------


async def show_language_picker(update: Update, *, edit: bool) -> None:
    text = (
        "<b>Choose your language</b>\n"
        "<b>ቋንቋዎን ይምረጡ</b>\n"
        "<b>ቋንቋኹም ምረጹ</b>\n\n"
        "English is the default until you choose."
    )
    markup = language_keyboard()
    if edit and update.callback_query:
        await update.callback_query.edit_message_text(
            text, reply_markup=markup, parse_mode=ParseMode.HTML
        )
    elif update.message:
        await update.message.reply_text(
            text, reply_markup=markup, parse_mode=ParseMode.HTML
        )


async def show_home(
    update: Update, context: ContextTypes.DEFAULT_TYPE, *, edit: bool
) -> None:
    lang = get_lang(context)
    markup = main_menu_keyboard(lang)
    text = t(lang, "home")
    if edit and update.callback_query:
        await update.callback_query.edit_message_text(
            text, reply_markup=markup, parse_mode=ParseMode.HTML
        )
    elif update.message:
        await update.message.reply_text(
            text, reply_markup=markup, parse_mode=ParseMode.HTML
        )


async def show_static(query, text: str, markup) -> None:
    await query.edit_message_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)


async def show_topic(
    query,
    context: ContextTypes.DEFAULT_TYPE,
    prefix: str,
    key: str,
    page_keys: tuple[str, ...],
) -> None:
    lang = get_lang(context)
    body_key = f"{prefix}.{key}"
    text = t(lang, body_key)
    if text == body_key:
        await show_static(query, t(lang, "not_found"), home_only_keyboard(lang))
        return

    user = query.from_user
    log_event(
        user.id if user else None,
        "page_open",
        topic=prefix,
        page=key,
        lang=lang,
    )

    if key == "menu":
        await show_static(
            query, text, topic_menu_keyboard(lang, prefix, page_keys)
        )
    else:
        feedback_note = f"\n\n<i>{t(lang, 'feedback.ask')}</i>"
        await show_static(
            query,
            text + feedback_note,
            page_keyboard(lang, f"{prefix}:menu", topic=prefix, page=key),
        )


def _load_lang_from_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or has_lang(context):
        return
    saved = get_user_lang(user.id)
    if saved:
        set_lang(context, saved)


def _first_media_file(topic: str) -> Path | None:
    folder = MEDIA_ROOT / topic
    if not folder.is_dir():
        return None
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.name != ".gitkeep":
            return path
    return None


# ---------- Handlers ----------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("await", None)
    _load_lang_from_db(update, context)
    if not has_lang(context):
        await show_language_picker(update, edit=False)
        return
    await show_home(update, context, edit=False)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not _is_admin(user.id if user else None):
        return
    await update.message.reply_text(stats_summary(), parse_mode=ParseMode.HTML)


async def settext_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin CMS starter: /settext home|New home text..."""
    user = update.effective_user
    if not _is_admin(user.id if user else None):
        return
    raw = " ".join(context.args) if context.args else ""
    if "|" not in raw:
        await update.message.reply_text(
            "Usage: /settext key|value\nExample: /settext home|<b>SSR</b>\\nWelcome..."
        )
        return
    key, value = raw.split("|", 1)
    key, value = key.strip(), value.strip()
    if not key or not value:
        await update.message.reply_text("Both key and value are required.")
        return
    msg = set_en_text(key, value)
    await update.message.reply_text(msg)


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not _is_admin(user.id if user else None):
        return
    text = " ".join(context.args).strip() if context.args else ""
    if not text:
        context.user_data["await"] = "broadcast"
        await update.message.reply_text(
            "Send the broadcast message as your next text.\n"
            "Or use: /broadcast Your message here"
        )
        return
    await _do_broadcast(update, context, text)


async def _do_broadcast(
    update: Update, context: ContextTypes.DEFAULT_TYPE, text: str
) -> None:
    recipients = list_subscribers()
    ok = 0
    for chat_id in recipients:
        try:
            await context.bot.send_message(chat_id, text)
            ok += 1
        except Exception:
            logging.exception("Broadcast failed for %s", chat_id)
    await update.effective_message.reply_text(
        f"Broadcast sent to {ok}/{len(recipients)} subscribers."
    )


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle conversational replies OR fallback guide."""
    if not update.message or not update.message.text:
        return

    _load_lang_from_db(update, context)
    awaiting = context.user_data.get("await")
    lang = get_lang(context) if has_lang(context) else "en"
    user = update.effective_user
    text = update.message.text.strip()

    if awaiting == "broadcast" and _is_admin(user.id if user else None):
        context.user_data.pop("await", None)
        await _do_broadcast(update, context, text)
        return

    if awaiting == "ref_contact" and user:
        need = context.user_data.pop("ref_need", "info")
        context.user_data.pop("await", None)
        rid = add_referral(user.id, need, text, lang)
        await _notify_staff(
            context,
            f"<b>New support request #{rid}</b>\n"
            f"User: <code>{user.id}</code>\nNeed: {need}\nContact: {text}\nLang: {lang}",
        )
        await update.message.reply_text(
            t(lang, "referral.done"),
            reply_markup=main_menu_keyboard(lang),
            parse_mode=ParseMode.HTML,
        )
        return

    if awaiting == "vol_city" and user:
        context.user_data["vol_city"] = text[:200]
        context.user_data["await"] = "vol_skills"
        await update.message.reply_text(t(lang, "involve.ask_skills"))
        return

    if awaiting == "vol_skills" and user:
        city = context.user_data.pop("vol_city", "")
        context.user_data.pop("await", None)
        vid = add_volunteer(user.id, city, text[:500], lang)
        await _notify_staff(
            context,
            f"<b>Volunteer interest #{vid}</b>\n"
            f"User: <code>{user.id}</code>\nCity: {city}\nSkills: {text}\nLang: {lang}",
        )
        await update.message.reply_text(
            t(lang, "involve.done"),
            reply_markup=main_menu_keyboard(lang),
            parse_mode=ParseMode.HTML,
        )
        return

    # Unexpected text / uploads handled separately for non-text; text fallback:
    if not has_lang(context):
        await show_language_picker(update, edit=False)
        return
    await update.message.reply_text(
        t(lang, "fallback"),
        reply_markup=main_menu_keyboard(lang),
        parse_mode=ParseMode.HTML,
    )


async def on_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    _load_lang_from_db(update, context)
    if not has_lang(context):
        await show_language_picker(update, edit=False)
        return
    lang = get_lang(context)
    await update.message.reply_text(
        t(lang, "fallback"),
        reply_markup=main_menu_keyboard(lang),
        parse_mode=ParseMode.HTML,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data or ""
    _load_lang_from_db(update, context)
    user = update.effective_user

    if data.startswith("lang:"):
        code = data.split(":", 1)[1]
        set_lang(context, code)
        if user:
            upsert_user_lang(user.id, code)
        await show_home(update, context, edit=True)
        return

    if data == "menu:language":
        await show_language_picker(update, edit=True)
        return

    if not has_lang(context):
        await show_language_picker(update, edit=True)
        return

    lang = get_lang(context)

    if data == "menu:home":
        context.user_data.pop("await", None)
        await show_home(update, context, edit=True)
        return

    if data == "menu:about":
        await show_static(query, t(lang, "about"), home_only_keyboard(lang))
        return

    if data == "menu:contact":
        await show_static(query, t(lang, "contact"), home_only_keyboard(lang))
        return

    if data == "menu:help":
        await show_static(query, t(lang, "help"), home_only_keyboard(lang))
        return

    if data == "quiz:start":
        text = f"{t(lang, 'quiz.intro')}\n\n<b>{t(lang, 'quiz.question')}</b>"
        await show_static(query, text, quiz_options_keyboard(lang))
        return

    for key, goto in QUIZ_OPTIONS:
        if data == f"quiz:{key}":
            await show_static(
                query,
                t(lang, f"quiz.{key}_result"),
                quiz_result_keyboard(lang, key, goto),
            )
            return

    if data.startswith("gbv:"):
        await show_topic(
            query, context, "gbv", data.split(":", 1)[1], GBV_PAGE_KEYS
        )
        return

    if data.startswith("peace:"):
        await show_topic(
            query, context, "peace", data.split(":", 1)[1], PEACE_PAGE_KEYS
        )
        return

    if data.startswith("rights:"):
        await show_topic(
            query, context, "rights", data.split(":", 1)[1], RIGHTS_PAGE_KEYS
        )
        return

    # Feedback
    if data.startswith("fb:"):
        parts = data.split(":")
        # fb:1:topic:page | fb:0:topic:page | fb:skip:topic:page
        if len(parts) >= 4:
            flag, topic, page = parts[1], parts[2], parts[3]
            if flag in ("1", "0") and user:
                add_feedback(user.id, topic, page, flag == "1", lang)
            await show_static(
                query,
                t(lang, "feedback.thanks"),
                home_only_keyboard(lang),
            )
        return

    # Resources
    if data == "res:menu":
        await show_static(query, t(lang, "resources.menu"), resources_keyboard(lang))
        return
    if data.startswith("res:"):
        topic = data.split(":", 1)[1]
        path = _first_media_file(topic)
        if not path:
            await show_static(
                query, t(lang, "resources.empty"), home_only_keyboard(lang)
            )
            return
        await query.edit_message_text(
            t(lang, "resources.menu"),
            reply_markup=home_only_keyboard(lang),
            parse_mode=ParseMode.HTML,
        )
        with path.open("rb") as doc:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=doc,
                filename=path.name,
                caption=f"SSR resource — {topic}",
            )
        return

    # Referral
    if data == "ref:start":
        context.user_data.pop("await", None)
        await show_static(
            query,
            f"{t(lang, 'referral.intro')}\n\n{t(lang, 'referral.choose_need')}",
            referral_need_keyboard(lang),
        )
        return
    if data.startswith("ref:need:") and user:
        need = data.split(":")[-1]
        context.user_data["ref_need"] = need
        context.user_data["await"] = "ref_contact"
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        t(lang, "referral.skip_contact"),
                        callback_data="ref:skip",
                    )
                ],
                [InlineKeyboardButton(t(lang, "nav.main"), callback_data="menu:home")],
            ]
        )
        await show_static(query, t(lang, "referral.ask_contact"), markup)
        return
    if data == "ref:skip" and user:
        need = context.user_data.pop("ref_need", "info")
        context.user_data.pop("await", None)
        rid = add_referral(user.id, need, None, lang)
        await _notify_staff(
            context,
            f"<b>New support request #{rid}</b>\n"
            f"User: <code>{user.id}</code>\nNeed: {need}\nContact: (skipped)\nLang: {lang}",
        )
        await show_static(query, t(lang, "referral.done"), home_only_keyboard(lang))
        return

    # Updates / subscribe
    if data == "upd:menu":
        await show_static(query, t(lang, "updates.menu"), updates_keyboard(lang))
        return
    if data == "upd:sub" and user:
        set_subscribed(user.id, True, lang)
        await show_static(query, t(lang, "updates.sub_ok"), home_only_keyboard(lang))
        return
    if data == "upd:unsub" and user:
        set_subscribed(user.id, False, lang)
        await show_static(query, t(lang, "updates.unsub_ok"), home_only_keyboard(lang))
        return

    # Volunteer
    if data == "vol:start":
        context.user_data["await"] = "vol_city"
        await show_static(
            query,
            f"{t(lang, 'involve.menu')}\n\n{t(lang, 'involve.ask_city')}",
            home_only_keyboard(lang),
        )
        return


def main() -> None:
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("settext", settext_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(MessageHandler(~filters.COMMAND & ~filters.TEXT, on_non_text))
    print("SSR bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
