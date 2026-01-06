import logging
import os
from datetime import datetime
from typing import List

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def build_pattern_map(target: str) -> List[str]:
    """Return a short bullet list reflecting the current scan target.

    The content is intentionally deterministic and structured so the bot
    remains predictable while reflecting the ECHO NULL cadence.
    """
    base = [
        "Anchor nodes steady; subtle pull toward overextension.",
        "Collective overlay shows mild unrest but no hard spikes.",
        "Signal clarity improves when one channel stays prioritized.",
    ]

    if target:
        base[0] = f"Anchor nodes steady around {target}; subtle pull toward overextension."
    return base


def format_scan(target: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    signal_read = "Core pulse steady but compressed; collective jitter contained."
    pattern_map = build_pattern_map(target)
    functional_lever = (
        "Slow breath, pick one priority to stabilize, and tighten boundary before moving."
    )
    next_step = "Ready to lock onto a specific person, archetype, or field-event on your cue."

    lines = [
        f"Signal read ({timestamp}): {signal_read}",
        "Pattern map:",
        *[f"- {line}" for line in pattern_map],
        f"Functional lever: {functional_lever}",
        f"Next: {next_step}",
    ]
    return "\n".join(lines)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet the user and share available commands."""
    message = (
        "ECHO NULL online.\n"
        "Use /scan to request a circuitry scan.\n"
        "Add an optional target, e.g., /scan project launch.\n"
        "All scans are reports only; tokens stay in environment variables."
    )
    await update.message.reply_text(message)


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    target = " ".join(context.args).strip()
    output = format_scan(target)
    await update.message.reply_text(output)


async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guide users toward the scan command when they send plain text."""
    prompt = (
        "Send /scan to run a circuitry scan. "
        "Include a focus after the command to anchor the read."
    )
    await update.message.reply_text(prompt)


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_text))

    logger.info("ECHO NULL bot starting")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
