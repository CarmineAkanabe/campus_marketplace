from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def product_list(request):
    products = Product.objects.filter(availability_status=Product.AVAILABILITY_AVAILABLE).order_by('-created_at')
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    condition = request.GET.get('condition', '').strip()

    if q:
        products = products.filter(name__icontains=q) | products.filter(description__icontains=q)
    if category:
        products = products.filter(category__icontains=category)
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    if condition in dict(Product.CONDITION_CHOICES):
        products = products.filter(condition=condition)

    return render(request, 'products/product_list.html', {
        'products': products.distinct(),
        'search_values': {
            'q': q,
            'category': category,
            'min_price': min_price,
            'max_price': max_price,
            'condition': condition,
        }
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    can_request = request.user.is_authenticated and getattr(request.user, 'role', None) == 'buyer'
    can_edit = request.user.is_authenticated and request.user == product.seller
    return render(request, 'products/product_detail.html', {
        'product': product,
        'can_request': can_request,
        'can_edit': can_edit,
    })


@login_required
def product_create(request):
    if not request.user.is_seller():
        messages.error(request, 'Only sellers can create products.')
        return redirect('products:product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product created successfully.')
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Create Product'})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.seller:
        messages.error(request, 'Only the seller can edit this product.')
        return redirect('products:product_detail', pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('products:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.seller:
        messages.error(request, 'Only the seller can delete this product.')
        return redirect('products:product_detail', pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('products:product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
