from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import Review
from notifications.models import Notification
from requestsystem.models import PurchaseRequest


@login_required
def review_list(request):
    reviews = Review.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'reviews/review_list.html', {'reviews': reviews})


@login_required
def review_create(request, request_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=request_id, buyer=request.user)
    if purchase_request.status not in [PurchaseRequest.STATUS_ACCEPTED, PurchaseRequest.STATUS_COMPLETED]:
        messages.error(request, 'You can only review sellers after your request is accepted or completed.')
        return redirect('requestsystem:request_detail', pk=request_id)

    if Review.objects.filter(buyer=request.user, seller=purchase_request.product.seller).exists():
        messages.error(request, 'You have already reviewed this seller.')
        return redirect('reviews:review_list')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.buyer = request.user
            review.seller = purchase_request.product.seller
            review.save()
            Notification.objects.create(
                user=purchase_request.product.seller,
                title='New seller review',
                message=f'{request.user.username} left a review for {purchase_request.product.name}.',
            )
            messages.success(request, 'Your review has been submitted.')
            return redirect('reviews:review_list')
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_form.html', {
        'form': form,
        'seller': purchase_request.product.seller,
        'product': purchase_request.product,
        'request_id': purchase_request.pk,
    })
