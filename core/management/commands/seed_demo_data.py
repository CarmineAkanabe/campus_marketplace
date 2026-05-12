from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = 'Seed demo users and products for local presentations.'

    def handle(self, *args, **options):
        User = get_user_model()

        seller, _ = User.objects.update_or_create(
            username='demo_seller',
            defaults={
                'email': 'seller@example.com',
                'first_name': 'Demo',
                'last_name': 'Seller',
                'role': User.SELLER,
                'phone': '+237 600 000 001',
                'location': 'Campus Main Gate',
            },
        )
        seller.set_password('demo12345')
        seller.save()

        buyer, _ = User.objects.update_or_create(
            username='demo_buyer',
            defaults={
                'email': 'buyer@example.com',
                'first_name': 'Demo',
                'last_name': 'Buyer',
                'role': User.BUYER,
                'phone': '+237 600 000 002',
                'location': 'Student Hostel',
            },
        )
        buyer.set_password('demo12345')
        buyer.save()

        products = [
            {
                'name': 'Scientific Calculator',
                'description': 'Reliable calculator for engineering and business courses.',
                'category': 'School Supplies',
                'price': Decimal('8500.00'),
                'condition': Product.CONDITION_USED,
            },
            {
                'name': 'Accounting Textbook',
                'description': 'Clean textbook with a few highlighted pages.',
                'category': 'Books',
                'price': Decimal('12000.00'),
                'condition': Product.CONDITION_USED,
            },
            {
                'name': 'Wireless Mouse',
                'description': 'Compact mouse for laptops and computer lab work.',
                'category': 'Electronics',
                'price': Decimal('6500.00'),
                'condition': Product.CONDITION_NEW,
            },
            {
                'name': 'Study Desk Lamp',
                'description': 'Small desk lamp suitable for hostel rooms.',
                'category': 'Room Essentials',
                'price': Decimal('10000.00'),
                'condition': Product.CONDITION_USED,
            },
        ]

        for data in products:
            Product.objects.update_or_create(
                seller=seller,
                name=data['name'],
                defaults={
                    **data,
                    'seller': seller,
                    'availability_status': Product.AVAILABILITY_AVAILABLE,
                },
            )

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
