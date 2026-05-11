from django.shortcuts import render

from products.models import Product


def home(request):
    products = Product.objects.filter(availability_status=Product.AVAILABILITY_AVAILABLE).order_by('-created_at')[:8]
    return render(request, 'core/home.html', {'products': products})
