import os
import aiohttp
import asyncio
from dotenv import load_dotenv
from typing import Dict, Optional
from app.utils.price_parser import html_dump_to_dict
from app.utils.log_setup import get_logger

load_dotenv()

logger = get_logger(__name__)

class PriceFetcher:
    BASE_URL = os.getenv("BASE_URL")

    @staticmethod
    async def fetch_price(session: aiohttp.ClientSession, metal: str, retries: int = 3, timeout: int = 5) -> Optional[Dict[str, object]]:
        # logger.info("Loaded BASE_URL=%s", os.getenv("BASE_URL"))

        url = f"{PriceFetcher.BASE_URL}/{metal}"

        for attempt in range(1, retries + 1):
            try:
                async with session.get(url, timeout=timeout) as response:
                    response.raise_for_status()
                    html = await response.text()
                    return html_dump_to_dict(html)
            except Exception as e:
                logger.error("Attempt %d/%d failed for %s: %s", attempt, retries, metal, e)
                await asyncio.sleep(2 ** attempt)
        return None
