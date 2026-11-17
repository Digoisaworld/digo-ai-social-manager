# DIGO AI Social Manager

Python service that generates English social content and artwork for DIGO AI WORLD, then publishes to the official Telegram channel, its community group, and X on a configurable schedule.

## Destinations
- Telegram channel: @Digoisaworld
- Telegram community group: @Digocryptocoin
- X account: @DigoAicoin

The Telegram bot must be an administrator in both Telegram destinations with permission to post messages/photos.

## Critical credential security
- Never commit API keys, Telegram bot tokens, X credentials, or .env.
- X API credentials were pasted into a chat and must be revoked/rotated before use. Regenerate Consumer/API Key and Secret, plus user Access Token and Access Token Secret. The Bearer Token is not used by this posting implementation.
- The Pollinations secret previously pasted into chat must also be revoked and replaced.
- Keep replacement secrets only in the VPS .env file.
- Pollinations models, credits and rate limits depend on the account and are not guaranteed to be free or unlimited.

## Setup
1. Copy .env.example to .env on the VPS and fill in credentials.
2. Create a Telegram bot with BotFather; add it as administrator to both destinations.
3. Configure an X Developer App with user-context write permission and generate user Access Token/Secret.
4. Set POST_INTERVAL_DAYS=3 for one post every three days, or 1 for daily.
5. Run docker compose up -d --build.

## MVP behavior
- Generates one English content package and one image per run.
- Publishes to the Telegram channel and group, and to X independently.
- Stores publication records in PostgreSQL.
- Supports optional RSS feeds; without feeds it creates evergreen educational content, not fabricated breaking news.
- Manual trigger is protected by an admin token.

This is an initial MVP. Test privately before enabling production scheduling. It does not promise listing, profit, airdrops, partnerships, or token price movements.
