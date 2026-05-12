from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from reviews.models import Review
from notifications.models import Notification
from .models import PurchaseRequest


@login_required
def request_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id, availability_status=Product.AVAILABILITY_AVAILABLE)
    if getattr(request.user, 'role', None) != 'buyer' or request.user.is_staff or request.user.is_superuser:
        messages.error(request, 'Only buyers can send requests.')
        return redirect('products:product_detail', pk=product.pk)

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            purchase_request = PurchaseRequest.objects.create(buyer=request.user, product=product, message=message_text)
            Notification.objects.create(
                user=product.seller,
                title='New purchase request',
                message=f'{request.user.username} sent a request for {product.name}.',
            )
            messages.success(request, 'Your request was sent to the seller.')
            return redirect('products:product_detail', pk=product.pk)
        messages.error(request, 'Please enter a message for the request.')

    return render(request, 'requestsystem/request_form.html', {'product': product})


@login_required
def request_list(request):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, 'Admins manage requests from the admin panel.')
        return redirect('products:product_list')
    requests = PurchaseRequest.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'requestsystem/request_list.html', {'requests': requests})


@login_required
def seller_request_list(request):
    if getattr(request.user, 'role', None) != 'seller':
        messages.error(request, 'Only sellers can view incoming requests.')
        return redirect('core:home')

    requests = PurchaseRequest.objects.filter(product__seller=request.user).order_by('-created_at')
    return render(request, 'requestsystem/seller_request_list.html', {'requests': requests})


@login_required
def request_detail(request, pk):
    purchase_request = get_object_or_404(PurchaseRequest, pk=pk)
    if request.user != purchase_request.buyer and request.user != purchase_request.product.seller:
        messages.error(request, 'You do not have permission to view this request.')
        return redirect('core:home')

    if request.method == 'POST' and request.user == purchase_request.product.seller:
        new_status = request.POST.get('status')
        valid_statuses = [choice[0] for choice in PurchaseRequest.STATUS_CHOICES]
        if new_status in valid_statuses:
            purchase_request.status = new_status
            purchase_request.save()
            Notification.objects.create(
                user=purchase_request.buyer,
                title='Request status updated',
                message=f'Your request for {purchase_request.product.name} is now {new_status}.',
            )
            messages.success(request, 'Request status has been updated.')
            if new_status == PurchaseRequest.STATUS_COMPLETED:
                product = purchase_request.product
                product.availability_status = Product.AVAILABILITY_SOLD
                product.save()
        else:
            messages.error(request, 'Invalid status selected.')
        return redirect('requestsystem:request_detail', pk=pk)

    can_review = False
    if request.user == purchase_request.buyer and purchase_request.status in [PurchaseRequest.STATUS_ACCEPTED, PurchaseRequest.STATUS_COMPLETED]:
        can_review = not Review.objects.filter(
            buyer=request.user,
            seller=purchase_request.product.seller
        ).exists()

    return render(request, 'requestsystem/request_detail.html', {
        'request_item': purchase_request,
        'can_review': can_review,
    })
