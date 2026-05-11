from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from .models import PurchaseRequest


@login_required
def request_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id, availability_status=Product.AVAILABILITY_AVAILABLE)
    if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'buyer':
        messages.error(request, 'Only buyers can send requests.')
        return redirect('products:product_detail', pk=product.pk)

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            PurchaseRequest.objects.create(buyer=request.user, product=product, message=message_text)
            messages.success(request, 'Your request was sent to the seller.')
            return redirect('products:product_detail', pk=product.pk)
        messages.error(request, 'Please enter a message for the request.')
    return render(request, 'requestsystem/request_form.html', {'product': product})


@login_required
def request_list(request):
    requests = PurchaseRequest.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'requestsystem/request_list.html', {'requests': requests})
