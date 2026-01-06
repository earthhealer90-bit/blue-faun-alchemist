# Echo Null Telegram Bot

A minimal Telegram bot that delivers ECHO NULL style circuitry scan outputs. It is designed for easy deployment with a Render worker and keeps the bot token in an environment variable.

## Running locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your bot token (keep it private):
   ```bash
   export BOT_TOKEN="<your-telegram-bot-token>"
   ```
3. Start the bot:
   ```bash
   python bot.py
   ```

Use `/start` to see instructions and `/scan <target>` to receive a structured scan.

## Using the bot in Telegram

1. In Telegram, search for the bot username you registered with BotFather (right now it is `@ulga333bot`; if you rename it later, use the new handle).
2. Tap **Start** to open the chat and confirm the bot is online.
3. Send `/start` for a quick primer, then `/scan` with or without a focus:
   - `/scan`
   - `/scan project launch`
4. The bot runs wherever `bot.py` is active (locally or on Render); if the chat does not respond, confirm the process is running and the `BOT_TOKEN` matches the BotFather token.

## Deploying to Render

Create a **Worker** service that uses this repository.

- **Start command:** `python bot.py`
- **Environment variable:** add `BOT_TOKEN` with your Telegram bot token.
- No inbound port is required because the bot uses long polling.

When you rename the bot (e.g., from `ulga333bot` to `echo_null`), update the bot name in BotFather; the deployment does not need code changes—just ensure the `BOT_TOKEN` matches the active bot.
