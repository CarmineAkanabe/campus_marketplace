from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from products.models import Product
from requestsystem.models import PurchaseRequest


def percent(part, whole):
    if not whole:
        return 0
    return round((part / whole) * 100)


@login_required
def buyer_dashboard(request):
    if getattr(request.user, 'role', None) == 'seller':
        return redirect('dashboard:seller_dashboard')

    from recommendations.views import get_recommendations_for_user
    
    recent_requests = PurchaseRequest.objects.filter(buyer=request.user).order_by('-created_at')[:5]
    all_requests = PurchaseRequest.objects.filter(buyer=request.user)
    notifications = request.user.notifications.order_by('-created_at')[:5]
    recommendations = get_recommendations_for_user(request.user, limit=4)
    total_requests = all_requests.count()
    pending_requests = all_requests.filter(status=PurchaseRequest.STATUS_PENDING).count()
    accepted_requests = all_requests.filter(status=PurchaseRequest.STATUS_ACCEPTED).count()
    completed_requests = all_requests.filter(status=PurchaseRequest.STATUS_COMPLETED).count()
    
    return render(request, 'dashboard/buyer_dashboard.html', {
        'recent_requests': recent_requests,
        'notifications': notifications,
        'recommendations': recommendations,
        'request_stats': [
            {'label': 'Pending', 'count': pending_requests, 'percent': percent(pending_requests, total_requests)},
            {'label': 'Accepted', 'count': accepted_requests, 'percent': percent(accepted_requests, total_requests)},
            {'label': 'Completed', 'count': completed_requests, 'percent': percent(completed_requests, total_requests)},
        ],
        'total_requests': total_requests,
    })


@login_required
def seller_dashboard(request):
    if getattr(request.user, 'role', None) != 'seller':
        return redirect('dashboard:buyer_dashboard')

    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    product_total = products.count()
    available_products = products.filter(availability_status=Product.AVAILABILITY_AVAILABLE).count()
    sold_products = products.filter(availability_status=Product.AVAILABILITY_SOLD).count()
    all_requests = PurchaseRequest.objects.filter(product__seller=request.user)
    incoming_requests = PurchaseRequest.objects.filter(product__seller=request.user).order_by('-created_at')[:5]
    notifications = request.user.notifications.order_by('-created_at')[:5]
    request_total = all_requests.count()
    pending_requests = all_requests.filter(status=PurchaseRequest.STATUS_PENDING).count()
    completed_requests = all_requests.filter(status=PurchaseRequest.STATUS_COMPLETED).count()
    return render(request, 'dashboard/seller_dashboard.html', {
        'products': products,
        'incoming_requests': incoming_requests,
        'notifications': notifications,
        'request_count': request_total,
        'product_count': product_total,
        'seller_chart_stats': [
            {'label': 'Available products', 'count': available_products, 'percent': percent(available_products, product_total)},
            {'label': 'Sold products', 'count': sold_products, 'percent': percent(sold_products, product_total)},
            {'label': 'Pending requests', 'count': pending_requests, 'percent': percent(pending_requests, request_total)},
            {'label': 'Completed requests', 'count': completed_requests, 'percent': percent(completed_requests, request_total)},
        ],
    })
