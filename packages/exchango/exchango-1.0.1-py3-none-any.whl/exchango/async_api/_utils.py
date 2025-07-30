from datetime import datetime, timedelta
import aiohttp
import asyncio
import json

_cache = {}
_lock = asyncio.Lock()

def _update_cache(key, data):
    _cache[key] = {
        "data": data,
        "expires_at": datetime.now() + timedelta(minutes=30)
    }


def _get_cache(key):
    cached = _cache.get(key)
    if cached and cached["expires_at"] > datetime.now():
        return cached.get("data")
    return None


async def aget_exchange_rate():
    if cached := _get_cache("exchange_rate"):
        return cached

    async with _lock:
        if cached := _get_cache("exchange_rate"):
            return cached

        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.cbr-xml-daily.ru/latest.js") as response:
                text = await response.text()
                data = json.loads(text)

        _update_cache("exchange_rate", data)
        return data