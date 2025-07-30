from ._utils import aget_exchange_rate as _aget_exchange_rate

async def convert(currency, amount, to):
    if not isinstance(currency, str):
        actual_type = type(currency).__name__
        return f"Argument 'currency' must be a string, got {actual_type} instead (exchango.convert)."

    if not isinstance(to, str):
        actual_type = type(to).__name__
        return f"Argument 'to' must be a string, got {actual_type} instead (exchango.convert)."

    data = await _aget_exchange_rate()

    base_currency = data["base"]
    rates = data["rates"]

    if currency == base_currency:
        rate_from = 1.0
    else:
        rate_from = rates.get(currency)
        if rate_from is None:
            return f"Exchange rate for \"{currency}\" (exchango.convert) not found"

    if to == base_currency:
        rate_to = 1.0
    else:
        rate_to = rates.get(to)
        if rate_to is None:
            return f"Exchange rate for \"{to}\" (exchango.convert) not found"

    result = amount * (rate_to / rate_from)
    return result