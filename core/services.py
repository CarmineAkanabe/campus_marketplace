from decimal import Decimal, InvalidOperation
from hashlib import sha256

import requests
from django.core.cache import cache


FRANKFURTER_RATE_URL = 'https://api.frankfurter.dev/v2/rate/EUR/USD'
XAF_RATE_CACHE_KEY = 'xaf_exchange_rates_usd_eur'
RATE_CACHE_SECONDS = 60 * 60 * 24
RATE_FAILURE_CACHE_SECONDS = 60 * 10
XAF_PER_EUR = Decimal('655.957')
OPENVERSE_IMAGE_SEARCH_URL = 'https://api.openverse.org/v1/images/'
PRODUCT_IMAGE_CACHE_SECONDS = 60 * 60 * 24 * 7
PRODUCT_IMAGE_FAILURE_CACHE_SECONDS = 60 * 60


CATEGORY_IMAGE_FALLBACKS = {
    'book': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=900&q=80',
    'books': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=900&q=80',
    'electronics': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80',
    'audio': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=900&q=80',
    'school supplies': 'https://images.unsplash.com/photo-1456735190827-d1262f71b8a3?auto=format&fit=crop&w=900&q=80',
    'room essentials': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80',
}

DEFAULT_PRODUCT_IMAGE = 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=900&q=80'


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


def category_fallback_image(category):
    category_key = (category or '').strip().lower()
    return CATEGORY_IMAGE_FALLBACKS.get(category_key, DEFAULT_PRODUCT_IMAGE)


def search_product_image(product_name, category=''):
    """Find a relevant online image for a product, cached by search phrase."""
    search_terms = ' '.join(part for part in [product_name, category] if part).strip()
    if not search_terms:
        return category_fallback_image(category)

    cache_key = f'product_media_image:{sha256(search_terms.lower().encode()).hexdigest()}'
    cached_url = cache.get(cache_key)
    if cached_url is not None:
        return cached_url or category_fallback_image(category)

    try:
        response = requests.get(
            OPENVERSE_IMAGE_SEARCH_URL,
            params={
                'format': 'json',
                'q': search_terms,
                'page_size': 5,
                'mature': 'false',
            },
            timeout=3,
        )
        response.raise_for_status()
        results = response.json().get('results', [])
        image_url = ''
        for result in results:
            image_url = result.get('thumbnail') or result.get('url') or ''
            if image_url.startswith('http'):
                break
    except (requests.RequestException, ValueError, TypeError, AttributeError):
        cache.set(cache_key, '', PRODUCT_IMAGE_FAILURE_CACHE_SECONDS)
        return category_fallback_image(category)

    if image_url:
        cache.set(cache_key, image_url, PRODUCT_IMAGE_CACHE_SECONDS)
        return image_url

    cache.set(cache_key, '', PRODUCT_IMAGE_FAILURE_CACHE_SECONDS)
    return category_fallback_image(category)
