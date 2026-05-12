from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from products.models import Product
from requestsystem.models import PurchaseRequest


def percent(part, whole):
    if not whole:
        return 0
    return round((part / whole) * 100)


@login_required
def buyer_dashboard(request):
    if request.user.is_superuser:
        return redirect('dashboard:admin_dashboard')
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
    if request.user.is_superuser:
        return redirect('dashboard:admin_dashboard')
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


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard:buyer_dashboard')

    User = get_user_model()
    buyers = User.objects.filter(role=User.BUYER, is_superuser=False).count()
    sellers = User.objects.filter(role=User.SELLER, is_superuser=False).count()
    admins = User.objects.filter(is_superuser=True).count()
    total_people = buyers + sellers + admins

    total_products = Product.objects.count()
    available_products = Product.objects.filter(availability_status=Product.AVAILABILITY_AVAILABLE).count()
    sold_products = Product.objects.filter(availability_status=Product.AVAILABILITY_SOLD).count()

    total_requests = PurchaseRequest.objects.count()
    pending_requests = PurchaseRequest.objects.filter(status=PurchaseRequest.STATUS_PENDING).count()
    completed_requests = PurchaseRequest.objects.filter(status=PurchaseRequest.STATUS_COMPLETED).count()

    return render(request, 'dashboard/admin_dashboard.html', {
        'user_chart_stats': [
            {'label': 'Buyers', 'count': buyers, 'percent': percent(buyers, total_people)},
            {'label': 'Sellers', 'count': sellers, 'percent': percent(sellers, total_people)},
            {'label': 'Admins', 'count': admins, 'percent': percent(admins, total_people)},
        ],
        'product_chart_stats': [
            {'label': 'Available products', 'count': available_products, 'percent': percent(available_products, total_products)},
            {'label': 'Sold products', 'count': sold_products, 'percent': percent(sold_products, total_products)},
        ],
        'request_chart_stats': [
            {'label': 'Pending requests', 'count': pending_requests, 'percent': percent(pending_requests, total_requests)},
            {'label': 'Completed requests', 'count': completed_requests, 'percent': percent(completed_requests, total_requests)},
        ],
        'total_people': total_people,
        'total_products': total_products,
        'total_requests': total_requests,
    })
