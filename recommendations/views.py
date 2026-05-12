from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

from products.models import Product
from .models import ProductView


def track_product_view(user, product):
    """Record that a user viewed a product. Called from product detail view."""
    if user.is_authenticated:
        ProductView.objects.create(user=user, product=product)


def get_category_recommendations(user, limit=8):
    """
    Get products in categories the user has recently viewed.
    Excludes products already viewed.
    """
    # Find categories user has recently viewed
    viewed_products = ProductView.objects.filter(user=user).values_list('product_id', flat=True)[:10]
    categories = Product.objects.filter(id__in=viewed_products).values_list('category', flat=True).distinct()

    # Get popular products from those categories
    recommended = Product.objects.filter(
        category__in=categories,
        availability_status=Product.AVAILABILITY_AVAILABLE,
    ).exclude(id__in=viewed_products).order_by('-created_at')[:limit]

    return recommended


def get_popular_recommendations(limit=8, excluded_ids=None):
    """Get products with the most views."""
    popular = Product.objects.filter(
        availability_status=Product.AVAILABILITY_AVAILABLE
    ).annotate(
        view_count=Count('views')
    )
    if excluded_ids:
        popular = popular.exclude(id__in=excluded_ids)
    popular = popular.order_by('-view_count', '-created_at')[:limit]

    return popular


def unique_products(products, limit):
    """Return products once, preserving recommendation order."""
    seen = set()
    unique = []
    for product in products:
        if product.pk in seen:
            continue
        seen.add(product.pk)
        unique.append(product)
        if len(unique) >= limit:
            break
    return unique


def get_seller_recommendations(user, limit=8):
    """Get products from sellers the user has interacted with."""
    # Find sellers the user has viewed products from
    viewed_products = ProductView.objects.filter(user=user).values_list('product_id', flat=True)[:20]
    sellers = Product.objects.filter(id__in=viewed_products).values_list('seller_id', flat=True).distinct()

    # Get more products from those sellers
    recommended = Product.objects.filter(
        seller_id__in=sellers,
        availability_status=Product.AVAILABILITY_AVAILABLE,
    ).exclude(id__in=viewed_products).order_by('-created_at')[:limit]

    return recommended


def get_recommendations_for_user(user, limit=8):
    """
    Get personalized recommendations for a user.
    Priority: category-based > seller-based > popular.
    """
    if not user.is_authenticated:
        return get_popular_recommendations(limit)

    category_recs = list(get_category_recommendations(user, limit))
    seller_recs = list(get_seller_recommendations(user, limit))
    selected = unique_products(category_recs + seller_recs, limit)

    if len(selected) < limit:
        excluded_ids = [product.pk for product in selected]
        popular_recs = get_popular_recommendations(limit * 2, excluded_ids=excluded_ids)
        selected = unique_products(selected + list(popular_recs), limit)

    return selected


@login_required
def recommendations_list(request):
    """Display personalized recommendations for the user."""
    if getattr(request.user, 'role', None) == 'seller':
        messages.error(request, 'Recommendations are for buyers only.')
        return redirect('dashboard:seller_dashboard')
    
    recommendations = get_recommendations_for_user(request.user, limit=16)
    return render(request, 'recommendations/recommendations_list.html', {
        'recommendations': recommendations,
    })

