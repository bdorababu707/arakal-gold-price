import aiohttp
import asyncio
from datetime import datetime, timezone
from app.utils.price_fetcher import PriceFetcher
from app.websocket_manager import WebSocketManager
from app.utils.log_setup import get_logger

logger = get_logger(__name__)

last_known = {"gold": None, "gold_last_updated": None, "silver": None, "silver_last_updated": None}
health_error = None  # To track the last error

async def fetch_live_price():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                gold_task = PriceFetcher.fetch_price(session, "GOLD")
                silver_task = PriceFetcher.fetch_price(session, "SILVER")
                gold_price, silver_price = await asyncio.gather(gold_task, silver_task)

                now_ts = datetime.now(timezone.utc).isoformat()

                if gold_price:
                    last_known["gold"] = gold_price
                    last_known["gold_last_updated"] = now_ts
                if silver_price:
                    last_known["silver"] = silver_price
                    last_known["silver_last_updated"] = now_ts

                data = {
                    "gold": {"price": last_known["gold"] or {"error": "No data"}, "updated_at": last_known["gold_last_updated"]},
                    "silver": {"price": last_known["silver"] or {"error": "No data"}, "updated_at": last_known["silver_last_updated"]},
                }

                await WebSocketManager.broadcast(data)
                health_error = None  # success

            except Exception as e:
                # logger.error("Error in price fetcher: %s", e)
                health_error = str(e)  # track last error

            await asyncio.sleep(0.5)
