# Campus Market Intelligence Platform

## Project Overview

The Campus Market Intelligence Platform is a Django + MySQL web application designed for students and small campus vendors.

The platform allows sellers to post products and buyers to browse, search, compare, and request products.

The system combines:
- Local marketplace functionalities
- CRUD operations
- Dashboard systems
- Notifications
- Recommendation logic
- Optional online features such as scraping and analytics

The goal of this project is not full implementation, but rather:
- System design
- Software architecture
- Database architecture
- Folder structure
- Feature planning
- Application flow

---

# Main Objectives

## Academic Objectives

This project demonstrates:
- Django MVT architecture
- MySQL database design
- Modular application structure
- User authentication and authorization
- CRUD operations
- Dashboard systems
- Data relationships
- Service-based architecture
- Online data integration concepts

---

# Users of the System

## 1. Buyer

The Buyer can:
- Register and login
- Browse products
- Search products
- Filter products
- Save favorite products
- Send purchase requests
- View recommendations
- Review sellers
- Receive notifications

---

## 2. Seller

The Seller can:
- Register and login
- Create products
- Edit products
- Delete products
- Upload product images
- Manage inventory status
- View buyer requests
- Respond to requests
- View analytics dashboard
- Receive notifications

---

## Superuser (Django Admin)

The Django superuser manages:
- Users
- Products
- Reports
- Scraped data
- Platform moderation
- Notifications

The superuser is NOT considered one of the two system users.

---

# Main Features

# Local Functionalities (Core Features)

## Authentication System

Features:
- User registration
- User login/logout
- Password hashing
- Role selection (Buyer or Seller)
- Session management

---

## Product Management (CRUD)

Seller functionalities:
- Create product
- Read/View product
- Update product
- Delete product

Product fields:
- Product name
- Description
- Category
- Price
- Product image
- Product condition
- Availability status

---

## Product Search and Filtering

Buyers can search products using:
- Keywords
- Category
- Price range
- Seller
- Product condition
- Availability

---

## Favorites/Wishlist

Buyers can:
- Save products
- Remove saved products
- View favorite products

---

## Purchase Request System

Buyers can send requests to sellers.

Request features:
- Request message
- Request status
- Request history
- Seller response

Request statuses:
- Pending
- Accepted
- Rejected
- Completed

---

## Review and Rating System

Buyers can:
- Rate sellers
- Leave comments
- View seller ratings

---

## Notification System

Notifications include:
- New requests
- Request updates
- Product updates
- New reviews

---

## User Dashboard

### Buyer Dashboard

Displays:
- Favorite products
- Recent requests
- Notifications
- Recommended products

### Seller Dashboard

Displays:
- Product statistics
- Request statistics
- Product performance
- Notifications

---

# Optional Online Features

These features are conceptual and may not be fully implemented.

---

## Price Scraping System

The system can scrape prices from:
- Jumia Cameroon
- Local marketplace websites
- Classified listing websites

Purpose:
- Compare market prices
- Suggest fair product prices
- Detect overpriced items

Possible tools:
- BeautifulSoup
- Requests

---

## Recommendation Engine

Simple recommendation logic:

Examples:
- Users interested in phones may also view accessories
- Related products suggestions
- Popular products recommendations

---

## Trending Products Analytics

Displays:
- Most viewed products
- Most searched categories
- Trending products

---

## Currency Conversion API

Optional API integration:
- Convert FCFA to USD/EUR

---

# System Architecture

## Architecture Pattern

The system follows Django's MVT architecture:

- Model
- View
- Template

---

## Modular Design

The project is separated into multiple Django apps.

Advantages:
- Maintainability
- Scalability
- Reusability
- Separation of concerns

---

# Suggested Django Apps

```txt
campus_market/
│
├── users/
├── products/
├── requestsystem/
├── reviews/
├── notifications/
├── analytics/
├── scraper/
├── recommendations/
├── dashboard/
└── core/
```

---

# Full Project Folder Structure

```txt
campus_marketplace/
│
├── manage.py
├── requirements.txt
├── README.md
├── .env
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── users/
│   ├── migrations/
│   ├── templates/users/
│   ├── static/users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   └── services.py
│
├── products/
│   ├── migrations/
│   ├── templates/products/
│   ├── static/products/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   └── services.py
│
├── requestsystem/
│   ├── migrations/
│   ├── templates/requestsystem/
│   ├── static/requestsystem/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── reviews/
├── notifications/
├── analytics/
├── scraper/
├── recommendations/
├── dashboard/
├── media/
├── static/
└── templates/
```

---

# Database Design

# Main Tables

## users

```txt
id
full_name
email
phone
password
role
location
profile_image
created_at
```

---

## products

```txt
id
seller_id
name
description
category
price
condition
image
availability_status
created_at
updated_at
```

---

## purchase_requests

```txt
id
buyer_id
product_id
message
status
created_at
updated_at
```

---

## reviews

```txt
id
buyer_id
seller_id
rating
comment
created_at
```

---

## notifications

```txt
id
user_id
title
message
is_read
created_at
```

---

## favorites

```txt
id
buyer_id
product_id
created_at
```

---

## scraped_prices

```txt
id
product_name
source
price
scraped_at
```

---

# Suggested URLs

## Authentication

```txt
/register/
/login/
/logout/
```

---

## Products

```txt
/products/
/products/create/
/products/<id>/
/products/<id>/edit/
/products/<id>/delete/
```

---

## Requests

```txt
/requests/
/requests/create/
/requests/<id>/
```

---

## Reviews

```txt
/reviews/
/reviews/create/
```

---

## Dashboard

```txt
/dashboard/buyer/
/dashboard/seller/
```

---

# Suggested Pages

## Public Pages

- Home Page
- Product Listings
- Product Details
- Login Page
- Register Page
- About Page

---

## Buyer Pages

- Buyer Dashboard
- Favorite Products
- Notifications
- Requests History
- Recommendations

---

## Seller Pages

- Seller Dashboard
- Product Management
- Request Management
- Analytics Page
- Notifications

---

# Security Considerations

The system should include:
- Password hashing
- Authentication checks
- Role-based access control
- CSRF protection
- Form validation
- Secure file uploads

---

# Technologies Used

## Backend
- Django
- Python

## Database
- MySQL

## Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

## Optional Libraries
- BeautifulSoup
- Requests

---

# Future Improvements

Possible future upgrades:
- Real-time chat
- AI recommendations
- Mobile application
- Payment integration
- SMS notifications
- Email verification
- Product image recognition
- Geo-location support

---

# Development Roadmap

## Phase 1 — Planning

- Define requirements
- Design database
- Define architecture
- Create UI wireframes

---

## Phase 2 — Backend Structure

- Create Django project
- Configure MySQL
- Create apps
- Configure authentication

---

## Phase 3 — CRUD Features

- Product CRUD
- Request CRUD
- Review CRUD
- Notifications

---

## Phase 4 — Advanced Features

- Recommendations
- Analytics
- Scraping system
- Dashboard statistics

---

## Phase 5 — Testing and Documentation

- Test application structure
- Review architecture
- Create project documentation

---

# Conclusion

The Campus Market Intelligence Platform is a modern Django web application concept that combines:
- Marketplace management
- CRUD operations
- Dashboard systems
- Recommendation concepts
- Scraping architecture
- Analytics systems

The project is intentionally designed to remain simple enough for students while still appearing innovative and technically advanced during project defense and evaluation.

