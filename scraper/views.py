import requests
from bs4 import BeautifulSoup
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render

from products.models import Product
from .models import PriceScrapeLog, ScrapedPrice


def scrape_product_prices(product):
    """Simulate scraping product prices from external sources."""
    sources = [
        {
            'name': 'Amazon',
            'url': f'https://example.com/amazon/search?q={product.name.replace(" ", "+")}',
            'price': float(product.price) * 0.95,
        },
        {
            'name': 'eBay',
            'url': f'https://example.com/ebay/search?q={product.name.replace(" ", "+")}',
            'price': float(product.price) * 1.05,
        },
    ]

    scraped_entries = []
    errors = []

    for source in sources:
        try:
            # Placeholder HTTP request, not used in this simplified example.
            response = requests.get(source['url'], timeout=5)
            if response.status_code != 200:
                raise ValueError('Unexpected response status')

            # Simulate parsing data with BeautifulSoup.
            soup = BeautifulSoup(response.text, 'html.parser')
            scraped_price = ScrapedPrice.objects.create(
                product=product,
                source_name=source['name'],
                source_url=source['url'],
                price=source['price'],
                currency='USD',
            )
            scraped_entries.append(scraped_price)
        except Exception as exc:
            errors.append(str(exc))

    status = 'success' if scraped_entries and not errors else 'partial' if scraped_entries else 'failed'
    PriceScrapeLog.objects.create(
        source='other',
        status=status,
        products_scraped=1,
        prices_found=len(scraped_entries),
        errors='; '.join(errors),
    )

    return scraped_entries, errors


@staff_member_required
def scrape_dashboard(request):
    """Admin view to trigger scraping for products."""
    products = Product.objects.order_by('-created_at')[:20]
    scraped_data = []

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.filter(id=product_id).first()
        if product:
            scraped_data, errors = scrape_product_prices(product)
            return render(request, 'scraper/scrape_dashboard.html', {
                'products': products,
                'scraped_data': scraped_data,
                'errors': errors,
            })

    return render(request, 'scraper/scrape_dashboard.html', {
        'products': products,
        'scraped_data': scraped_data,
        'errors': [],
    })
