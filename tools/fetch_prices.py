"""Dump real Telegram gift star prices to prices.json.

Uses payments.getStarGifts, which needs a logged-in user account (not a bot).
Get TG_API_ID / TG_API_HASH at https://my.telegram.org -> API development tools.

    TG_API_ID=123 TG_API_HASH=abc python fetch_prices.py [out.json]

The first run asks for your phone number and login code, then keeps the
session in prices.session next to the script so later runs don't ask again.
"""
import asyncio
import json
import os
import sys

from telethon import TelegramClient
from telethon.tl.functions.payments import GetStarGiftsRequest

API_ID = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]
OUT = sys.argv[1] if len(sys.argv) > 1 else "prices.json"
SESSION = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prices")


async def main():
    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        res = await client(GetStarGiftsRequest(hash=0))
        prices = {}
        for g in res.gifts:
            if not hasattr(g, "stars"):
                continue
            prices[str(g.id)] = {
                "title": getattr(g, "title", None),
                "stars": g.stars,
                "upgrade_stars": getattr(g, "upgrade_stars", None),
                "sold_out": bool(getattr(g, "sold_out", False)),
                "limited": bool(getattr(g, "limited", False)),
            }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=1)
    print(f"Saved {len(prices)} gifts to {OUT}")


asyncio.run(main())
