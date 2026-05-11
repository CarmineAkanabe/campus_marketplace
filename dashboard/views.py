from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from products.models import Product
from requestsystem.models import PurchaseRequest


@login_required
def buyer_dashboard(request):
    if getattr(request.user, 'role', None) == 'seller':
        return redirect('dashboard:seller_dashboard')

    from recommendations.views import get_recommendations_for_user
    
    recent_requests = PurchaseRequest.objects.filter(buyer=request.user).order_by('-created_at')[:5]
    notifications = request.user.notifications.order_by('-created_at')[:5]
    recommendations = get_recommendations_for_user(request.user, limit=4)
    
    return render(request, 'dashboard/buyer_dashboard.html', {
        'recent_requests': recent_requests,
        'notifications': notifications,
        'recommendations': recommendations,
    })


@login_required
def seller_dashboard(request):
    if getattr(request.user, 'role', None) != 'seller':
        return redirect('dashboard:buyer_dashboard')

    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    incoming_requests = PurchaseRequest.objects.filter(product__seller=request.user).order_by('-created_at')[:5]
    notifications = request.user.notifications.order_by('-created_at')[:5]
    return render(request, 'dashboard/seller_dashboard.html', {
        'products': products,
        'incoming_requests': incoming_requests,
        'notifications': notifications,
        'request_count': incoming_requests.count(),
        'product_count': products.count(),
    })
