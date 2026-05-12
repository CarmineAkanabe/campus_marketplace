# CampusMart Documentation

## Overview

CampusMart is a modular Django application for campus buying and selling. It supports two main user roles:

- Buyers browse products, send purchase requests, review sellers, view recommendations, and receive notifications.
- Sellers create products, manage listings, respond to requests, receive notifications, and view dashboard/analytics summaries.

## Architecture

The project follows Django's MVT pattern:

- Models define users, products, requests, reviews, notifications, analytics, and recommendation tracking.
- Views handle role checks, form workflows, dashboards, search, analytics, and page rendering.
- Templates provide Bootstrap-based pages with custom styling in `static/css/style.css`.

## Apps

```txt
core              Home, About, shared services, seed command
users             Authentication, roles, profiles
products          Product CRUD, product search, product detail
requestsystem     Buyer/seller purchase request workflow
reviews           Seller reviews and ratings
notifications     User notifications and read state
dashboard         Buyer and seller dashboards
recommendations   Product view tracking and recommendations
analytics         Search and product performance analytics
```

## Data Model Summary

- `users.User`: custom user with buyer/seller role, phone, location, profile image
- `products.Product`: seller-owned listing with category, price, condition, image, availability
- `requestsystem.PurchaseRequest`: buyer request for a product with status tracking
- `reviews.Review`: buyer rating/comment for a seller
- `notifications.Notification`: user alert with read/unread state
- `recommendations.ProductView`: product view history for recommendations
- `analytics.SearchQuery`: search tracking
- `analytics.ProductAnalytics`: product analytics placeholder/aggregate model

## Main URLs

```txt
/                         Home
/about/                   About page
/accounts/register/       Register
/accounts/login/          Login
/accounts/logout/         Logout
/accounts/profile/        Profile
/products/                Product list
/products/create/         Create product
/products/<id>/           Product detail
/requests/                Buyer requests
/requests/seller/         Seller incoming requests
/reviews/                 Buyer reviews
/recommendations/         Buyer recommendations
/notifications/           Notifications
/dashboard/buyer/         Buyer dashboard
/dashboard/seller/        Seller dashboard
/analytics/dashboard/     Staff analytics dashboard
/analytics/seller/        Seller analytics
/admin/                   Django admin
```

## Online Currency Feature

Product prices remain stored in FCFA. A small service in `core.services` converts FCFA to EUR using the fixed peg, calls Frankfurter's public exchange-rate API for EUR to USD, and caches the derived rates for one day. Templates use a custom tag to show approximate converted prices.

If the external API fails or does not return the expected rates, pages continue to render normally and only show FCFA prices.

## Demo Data

The command below seeds one buyer, one seller, and several campus products:

```bash
python manage.py seed_demo_data
```

The command is safe to rerun. It updates/reuses known demo users and products instead of duplicating them.

## Security Notes

- Django handles password hashing and CSRF protection.
- Sensitive actions require login.
- Seller-only actions are checked in views.
- `SECRET_KEY` is read from environment variables with a local fallback for demos.
- Uploaded media and local database files are ignored by git.

## Testing

The test suite covers core pages, products, requests, reviews, notifications, recommendations, analytics, currency conversion fallback, scraper removal, and seed command reruns.

Run:

```bash
python manage.py test
```
