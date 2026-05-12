from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
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


def get_popular_recommendations(limit=8):
    """Get products with the most views."""
    popular = Product.objects.filter(
        availability_status=Product.AVAILABILITY_AVAILABLE
    ).annotate(
        view_count=Count('views')
    ).order_by('-view_count', '-created_at')[:limit]

    return popular


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

    # Try category-based first
    category_recs = get_category_recommendations(user, limit)
    if category_recs.count() >= limit:
        return category_recs

    # Combine category and seller recommendations
    seller_recs = get_seller_recommendations(user, limit - category_recs.count())
    all_recs = list(category_recs) + list(seller_recs)

    # Fill remaining with popular products
    if len(all_recs) < limit:
        popular_recs = get_popular_recommendations(limit - len(all_recs))
        all_recs.extend(popular_recs)

    return all_recs[:limit]


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

