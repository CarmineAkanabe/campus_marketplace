from django.shortcuts import render

from products.models import Product


def home(request):
    products = Product.objects.filter(availability_status=Product.AVAILABILITY_AVAILABLE).order_by('-created_at')[:8]
    return render(request, 'core/home.html', {'products': products})


def about(request):
    team_members = [
        {
            'name': 'Abanda Ambrouise',
            'role': 'Product Owner',
            'github': 'https://github.com/AmbroiseAB',
        },
        {
            'name': 'Serge',
            'role': 'Backend & Platform',
            'github': 'https://github.com/CarmineAkanabe',
        },
    ]
    return render(request, 'core/about.html', {'team_members': team_members})
