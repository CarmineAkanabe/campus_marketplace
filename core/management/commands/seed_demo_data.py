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
                'name': 'Casio FX-991EX Scientific Calculator',
                'description': 'Casio scientific calculator for engineering and business courses.',
                'category': 'School Supplies',
                'price': Decimal('8500.00'),
                'condition': Product.CONDITION_USED,
            },
            {
                'name': 'Introduction to Accounting Textbook',
                'description': 'Accounting textbook with clean pages and a few useful highlights.',
                'category': 'Books',
                'price': Decimal('12000.00'),
                'condition': Product.CONDITION_USED,
            },
            {
                'name': 'Logitech Wireless Mouse',
                'description': 'Compact Logitech mouse for laptops and computer lab work.',
                'category': 'Electronics',
                'price': Decimal('6500.00'),
                'condition': Product.CONDITION_NEW,
            },
            {
                'name': 'LED Study Desk Lamp',
                'description': 'Adjustable LED desk lamp suitable for hostel study tables.',
                'category': 'Room Essentials',
                'price': Decimal('10000.00'),
                'condition': Product.CONDITION_USED,
            },
            {
                'name': 'JBL Bluetooth Speaker',
                'description': 'Portable Bluetooth speaker for small rooms and study breaks.',
                'category': 'Audio',
                'price': Decimal('18000.00'),
                'condition': Product.CONDITION_USED,
            },
            {
                'name': 'HP Laptop Backpack',
                'description': 'Durable backpack with a padded laptop compartment.',
                'category': 'School Supplies',
                'price': Decimal('15000.00'),
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
