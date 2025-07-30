from datetime import datetime, timedelta
import requests


_cache = {}

def _update_cache(key, data):
    _cache[key] = {
        "data": data,
        "expires_at": datetime.now() + timedelta(minutes=30)
    }

def _get_cache(key):
    cached = _cache.get(key)

    if cached is not None and cached["expires_at"] > datetime.now():
        return cached.get("data")
    return None

def get_exchange_rate():
    if cached := _get_cache("exchange_rate"):
        return cached

    response = requests.get("https://www.cbr-xml-daily.ru/latest.js")
    data = response.json()

    _update_cache("exchange_rate", data)

    return data