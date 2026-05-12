# CampusMart Project Plan

## Completed

- Core Django project and modular app structure
- Custom buyer/seller user roles
- Product CRUD, listing, detail, search, and filtering
- Purchase requests and seller status updates
- Review and rating workflow
- Notifications
- Buyer and seller dashboards
- Recommendations based on product views
- Search/product analytics
- Simple currency conversion online feature
- Keyword-based online image search for products without uploaded photos
- Demo seed command
- Cleaner Bootstrap-based styling
- Admin panel access for superusers

## Not Included

- Favorites/wishlist
- Web scraping
- Payments
- Real-time chat
- Production deployment automation

## Useful Commands

```bash
python manage.py migrate
python manage.py seed_demo_data
python manage.py test
python manage.py runserver
```

## Notes for Presentation

- The online features are intentionally small and explainable.
- Converted prices and online images fail safely when internet access is unavailable.
- The seed command provides quick demo data similar to Laravel seeders.
- Superusers manage users/products through Django admin rather than acting as buyers.
