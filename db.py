"""SQLite persistence for users, events, feedback, referrals, volunteers."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("SSR_DB_PATH", "data/ssr_bot.db"))


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                lang TEXT NOT NULL DEFAULT 'en',
                subscribed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS events_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                event_type TEXT NOT NULL,
                topic TEXT,
                page TEXT,
                lang TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                topic TEXT,
                page TEXT,
                helpful INTEGER,
                lang TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                need TEXT,
                contact TEXT,
                lang TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS volunteers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                city TEXT,
                skills TEXT,
                lang TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )
        conn.commit()


def get_user_lang(telegram_id: int) -> str | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT lang FROM users WHERE telegram_id = ?",
            (telegram_id,),
        ).fetchone()
    if row and row["lang"] in ("en", "am", "ti"):
        return row["lang"]
    return None


def upsert_user_lang(telegram_id: int, lang: str) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO users (telegram_id, lang)
            VALUES (?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                lang = excluded.lang,
                updated_at = datetime('now')
            """,
            (telegram_id, lang),
        )
        conn.commit()


def set_subscribed(telegram_id: int, subscribed: bool, lang: str = "en") -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO users (telegram_id, lang, subscribed)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                subscribed = excluded.subscribed,
                updated_at = datetime('now')
            """,
            (telegram_id, lang, 1 if subscribed else 0),
        )
        conn.commit()


def list_subscribers() -> list[int]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT telegram_id FROM users WHERE subscribed = 1"
        ).fetchall()
    return [int(r["telegram_id"]) for r in rows]


def log_event(
    telegram_id: int | None,
    event_type: str,
    topic: str | None = None,
    page: str | None = None,
    lang: str | None = None,
) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO events_log (telegram_id, event_type, topic, page, lang)
            VALUES (?, ?, ?, ?, ?)
            """,
            (telegram_id, event_type, topic, page, lang),
        )
        conn.commit()


def add_feedback(
    telegram_id: int | None,
    topic: str,
    page: str,
    helpful: bool,
    lang: str,
) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO feedback (telegram_id, topic, page, helpful, lang)
            VALUES (?, ?, ?, ?, ?)
            """,
            (telegram_id, topic, page, 1 if helpful else 0, lang),
        )
        conn.commit()


def add_referral(
    telegram_id: int,
    need: str,
    contact: str | None,
    lang: str,
) -> int:
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO referrals (telegram_id, need, contact, lang)
            VALUES (?, ?, ?, ?)
            """,
            (telegram_id, need, contact, lang),
        )
        conn.commit()
        return int(cur.lastrowid)


def add_volunteer(
    telegram_id: int,
    city: str,
    skills: str,
    lang: str,
) -> int:
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO volunteers (telegram_id, city, skills, lang)
            VALUES (?, ?, ?, ?)
            """,
            (telegram_id, city, skills, lang),
        )
        conn.commit()
        return int(cur.lastrowid)


def stats_summary() -> str:
    with _connect() as conn:
        opens = conn.execute(
            """
            SELECT topic, COUNT(*) AS c FROM events_log
            WHERE event_type = 'page_open'
              AND created_at >= datetime('now', '-7 days')
            GROUP BY topic ORDER BY c DESC
            """
        ).fetchall()
        fb = conn.execute(
            """
            SELECT
              SUM(CASE WHEN helpful = 1 THEN 1 ELSE 0 END) AS yes_c,
              SUM(CASE WHEN helpful = 0 THEN 1 ELSE 0 END) AS no_c,
              COUNT(*) AS total
            FROM feedback
            WHERE created_at >= datetime('now', '-7 days')
            """
        ).fetchone()
        subs = conn.execute(
            "SELECT COUNT(*) AS c FROM users WHERE subscribed = 1"
        ).fetchone()["c"]
        refs = conn.execute(
            "SELECT COUNT(*) AS c FROM referrals WHERE created_at >= datetime('now', '-7 days')"
        ).fetchone()["c"]
        vols = conn.execute(
            "SELECT COUNT(*) AS c FROM volunteers WHERE created_at >= datetime('now', '-7 days')"
        ).fetchone()["c"]

    lines = ["<b>SSR bot stats (7 days)</b>", "", "<b>Topic opens</b>"]
    if opens:
        for row in opens:
            lines.append(f"• {row['topic'] or 'unknown'}: {row['c']}")
    else:
        lines.append("• No page opens yet")
    lines.extend(
        [
            "",
            f"<b>Feedback</b>: yes={fb['yes_c'] or 0}, no={fb['no_c'] or 0}, total={fb['total'] or 0}",
            f"<b>Subscribers</b>: {subs}",
            f"<b>Referrals</b>: {refs}",
            f"<b>Volunteer interests</b>: {vols}",
        ]
    )
    return "\n".join(lines)
