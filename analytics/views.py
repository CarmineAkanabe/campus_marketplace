from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.shortcuts import render

from products.models import Product
from requestsystem.models import PurchaseRequest
from .models import SearchQuery, ProductAnalytics


def track_search(user, query, category_filter=''):
    """Record a search query for analytics."""
    if query.strip():
        SearchQuery.objects.create(
            user=user if user.is_authenticated else None,
            query=query,
            category_filter=category_filter
        )


def get_popular_searches(limit=10):
    """Get the most common search queries."""
    return SearchQuery.objects.values('query').annotate(
        count=Count('query')
    ).order_by('-count')[:limit]


def get_trending_categories(limit=10):
    """Get the most searched categories."""
    return SearchQuery.objects.filter(
        category_filter__isnull=False
    ).exclude(
        category_filter=''
    ).values('category_filter').annotate(
        count=Count('category_filter')
    ).order_by('-count')[:limit]


def get_popular_products(limit=10):
    """Get products by various popularity metrics."""
    return Product.objects.filter(
        availability_status=Product.AVAILABILITY_AVAILABLE
    ).annotate(
        view_count=Count('views'),
        request_count=Count('requests')
    ).order_by('-view_count', '-request_count')[:limit]


def get_seller_product_stats(seller):
    """Get detailed product statistics for a seller."""
    products = Product.objects.filter(seller=seller)
    
    stats = {
        'total_products': products.count(),
        'available_products': products.filter(availability_status=Product.AVAILABILITY_AVAILABLE).count(),
        'sold_products': products.filter(availability_status=Product.AVAILABILITY_SOLD).count(),
        'total_requests': PurchaseRequest.objects.filter(product__in=products).count(),
        'completed_requests': PurchaseRequest.objects.filter(
            product__in=products,
            status=PurchaseRequest.STATUS_COMPLETED
        ).count(),
    }
    
    # Top performing products
    stats['top_products'] = products.annotate(
        request_count=Count('requests')
    ).order_by('-request_count')[:5]
    
    return stats


@staff_member_required
def analytics_dashboard(request):
    """Admin analytics dashboard."""
    popular_searches = get_popular_searches(limit=15)
    trending_categories = get_trending_categories(limit=10)
    popular_products = get_popular_products(limit=10)
    
    # Request statistics
    total_requests = PurchaseRequest.objects.count()
    completed_requests = PurchaseRequest.objects.filter(status=PurchaseRequest.STATUS_COMPLETED).count()
    pending_requests = PurchaseRequest.objects.filter(status=PurchaseRequest.STATUS_PENDING).count()
    
    # Product statistics
    total_products = Product.objects.count()
    available_products = Product.objects.filter(availability_status=Product.AVAILABILITY_AVAILABLE).count()
    sold_products = Product.objects.filter(availability_status=Product.AVAILABILITY_SOLD).count()
    
    context = {
        'popular_searches': popular_searches,
        'trending_categories': trending_categories,
        'popular_products': popular_products,
        'total_requests': total_requests,
        'completed_requests': completed_requests,
        'pending_requests': pending_requests,
        'total_products': total_products,
        'available_products': available_products,
        'sold_products': sold_products,
    }
    
    return render(request, 'analytics/analytics_dashboard.html', context)


def seller_analytics(request):
    """Analytics for individual sellers."""
    if getattr(request.user, 'role', None) != 'seller':
        return render(request, 'analytics/access_denied.html')
    
    seller_stats = get_seller_product_stats(request.user)
    
    return render(request, 'analytics/seller_analytics.html', {
        'stats': seller_stats,
    })
