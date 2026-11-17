# DIGO AI Social Manager

Python service that generates English social content and artwork for DIGO AI WORLD, then publishes to a Telegram channel and X account on a configurable schedule.

## Important security
- Never commit API keys, Telegram bot tokens, X credentials, or .env.
- The Pollinations secret key previously pasted into chat must be revoked and replaced. Do not reuse it.
- A Pollinations sk_ key is a server-side secret. Keep it only in the VPS environment.
- Pollinations usage is not guaranteed to be free or unlimited. Check selected models and account budget before enabling scheduled publishing.

## Setup
1. Copy .env.example to .env on the VPS and fill in credentials.
2. Create a Telegram bot with BotFather; add it as an administrator to the public DIGO channel with permission to post.
3. Create an X Developer App with user-context write permission and configure the credentials.
4. Set POST_INTERVAL_DAYS=3 for one post every three days, or 1 for daily.
5. Run docker compose up -d --build.

## Scope of this MVP
- Generates one English content package and one image per run.
- Publishes to Telegram and X independently.
- Stores publication records in PostgreSQL.
- Supports optional RSS feeds; without feeds it creates evergreen educational content, not fabricated breaking news.
- Manual trigger is protected by an admin token.

This is an initial MVP. Test privately before enabling production scheduling. It does not promise listing, profit, airdrops, partnerships, or token price movements.
