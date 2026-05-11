from django.shortcuts import render, get_object_or_404

from .models import Product


def product_list(request):
    products = Product.objects.filter(availability_status=Product.AVAILABILITY_AVAILABLE).order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    can_request = request.user.is_authenticated and getattr(request.user, 'role', None) == 'buyer'
    return render(request, 'products/product_detail.html', {'product': product, 'can_request': can_request})
