from decimal import Decimal, InvalidOperation

import requests
from django.core.cache import cache


FRANKFURTER_RATE_URL = 'https://api.frankfurter.dev/v2/rate/EUR/USD'
XAF_RATE_CACHE_KEY = 'xaf_exchange_rates_usd_eur'
RATE_CACHE_SECONDS = 60 * 60 * 24
RATE_FAILURE_CACHE_SECONDS = 60 * 10
XAF_PER_EUR = Decimal('655.957')


def get_xaf_exchange_rates():
    """Fetch XAF to USD/EUR rates and cache them for one day."""
    cached_rates = cache.get(XAF_RATE_CACHE_KEY)
    if cached_rates is not None:
        return cached_rates

    try:
        response = requests.get(FRANKFURTER_RATE_URL, timeout=3)
        response.raise_for_status()
        eur_to_usd = Decimal(str(response.json()['rate']))
        rates = {
            'EUR': Decimal('1') / XAF_PER_EUR,
            'USD': eur_to_usd / XAF_PER_EUR,
        }
    except (requests.RequestException, ValueError, TypeError, InvalidOperation, KeyError, AttributeError):
        cache.set(XAF_RATE_CACHE_KEY, {}, RATE_FAILURE_CACHE_SECONDS)
        return {}

    if {'USD', 'EUR'} <= set(rates):
        cache.set(XAF_RATE_CACHE_KEY, rates, RATE_CACHE_SECONDS)
        return rates

    cache.set(XAF_RATE_CACHE_KEY, {}, RATE_FAILURE_CACHE_SECONDS)
    return {}


def convert_xaf_price(amount):
    """Return approximate USD/EUR values for an FCFA amount."""
    try:
        price = Decimal(str(amount))
    except (InvalidOperation, TypeError):
        return {}

    rates = get_xaf_exchange_rates()
    if not rates:
        return {}

    return {
        code: (price * rate).quantize(Decimal('0.01'))
        for code, rate in rates.items()
    }
