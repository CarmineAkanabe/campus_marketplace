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
- About page and footer
- Simple currency conversion online feature
- Demo seed command
- Cleaner Bootstrap-based styling

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

- The online feature is intentionally small: FCFA prices can show approximate USD/EUR values from a public exchange-rate API.
- The app still works if the API is unavailable.
- The seed command provides quick demo data similar to Laravel seeders.
- The project emphasizes clear Django architecture and explainable workflows over advanced production complexity.
