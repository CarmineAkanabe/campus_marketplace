# Campus Marketplace - Complete Documentation

## Overview

The Campus Marketplace is a comprehensive Django web application designed for university students and small campus vendors. It provides a platform where students can buy and sell products within their campus community, featuring role-based access, product management, purchase requests, reviews, notifications, and personalized recommendations.

## Architecture

### Technology Stack
- **Backend**: Django 6.0.5
- **Database**: SQLite (development) / MySQL (production)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.0, JavaScript
- **Image Processing**: Pillow
- **Web Scraping**: BeautifulSoup4, Requests
- **Authentication**: Django's built-in authentication system

### Project Structure
```
campus_marketplace/
├── config/                 # Django project settings
├── core/                   # Homepage and core functionality
├── users/                  # Authentication and user management
├── products/               # Product CRUD operations
├── requestsystem/          # Purchase request management
├── reviews/                # Rating and review system
├── notifications/          # User notification system
├── dashboard/              # Buyer/Seller dashboards
├── recommendations/        # Product recommendation engine
├── analytics/              # Search and usage analytics
├── scraper/                # Price scraping (removed)
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User-uploaded files
└── templates/              # HTML templates
```

## User Roles

### 1. Buyer
Buyers can:
- Register and login to the platform
- Browse products with search and filtering
- View detailed product information
- Send purchase requests to sellers
- View and manage their requests
- Leave reviews and ratings for sellers
- Receive personalized product recommendations
- Access buyer dashboard with activity overview
- Receive notifications about request updates

### 2. Seller
Sellers can:
- Register and login to the platform
- Create, edit, and delete products
- Upload product images
- Manage product inventory and availability
- View and respond to buyer purchase requests
- Access seller dashboard with sales statistics
- View analytics about their products
- Receive notifications about new requests and reviews

### 3. Administrator (Django Admin)
Administrators can:
- Manage all users, products, and requests
- Access Django admin interface
- Moderate platform content
- View system-wide analytics

## Core Features

### Authentication System
- User registration with role selection (buyer/seller)
- Secure login/logout functionality
- Password hashing and validation
- Role-based access control
- Profile management and editing

### Product Management
- CRUD operations for products
- Image upload and management
- Category-based organization
- Price and condition tracking
- Availability status management
- Search and filtering capabilities

### Purchase Request System
- Buyers can send purchase requests to sellers
- Sellers can view and respond to requests
- Request status tracking (pending, accepted, rejected, completed)
- Message exchange between buyers and sellers

### Review and Rating System
- Buyers can rate and review sellers (1-5 stars)
- Review comments and timestamps
- Average rating calculation for sellers
- Review display on seller profiles

### Notification System
- Real-time notifications for user activities
- Unread notification count in navigation
- Mark notifications as read
- Notifications for requests, reviews, and updates

### Dashboard System
- **Buyer Dashboard**: Recent requests, notifications, recommendations
- **Seller Dashboard**: Product statistics, incoming requests, sales overview
- Role-based dashboard redirection

### Recommendation Engine
- Personalized product recommendations
- Category-based suggestions
- Seller-based recommendations
- Popular product tracking
- Product view tracking

### Analytics System
- Search query tracking
- Product view analytics
- Category popularity metrics
- User behavior insights

## Database Models

### User Model (Custom)
- Extends Django's AbstractUser
- Additional fields: role (buyer/seller), profile picture
- Role-based permissions and access control

### Product Model
- Fields: name, description, category, price, condition, image, availability
- Foreign key to User (seller)
- Image upload handling

### PurchaseRequest Model
- Links buyer, product, and seller
- Status tracking and messaging
- Timestamp fields

### Review Model
- Buyer-seller rating system
- Star ratings (1-5) and comments
- Average rating calculations

### Notification Model
- User-specific notifications
- Read/unread status
- Title and message content

### Analytics Models
- SearchQuery: Tracks user searches
- ProductAnalytics: Product view statistics

### Recommendation Models
- ProductView: Tracks product viewing history

## URL Structure

```
/                     # Homepage
/accounts/login/       # User login
/accounts/register/    # User registration
/accounts/logout/      # User logout
/accounts/profile/     # User profile
/products/             # Product listing
/products/create/      # Create product (sellers)
/products/<id>/        # Product detail
/products/<id>/edit/   # Edit product (sellers)
/products/<id>/delete/ # Delete product (sellers)
/requests/             # Buyer requests
/requests/<id>/        # Request detail
/requests/seller/      # Seller request management
/reviews/              # User reviews
/recommendations/      # Product recommendations
/notifications/        # User notifications
/dashboard/            # User dashboard (role-based)
/analytics/            # Analytics dashboard (staff)
/admin/                # Django admin
```

## Security Features

- CSRF protection on all forms
- User authentication required for sensitive operations
- Role-based access control
- Form validation and sanitization
- Secure file upload handling
- SQL injection prevention through Django ORM

## Testing

The application includes comprehensive unit tests covering:
- Model creation and relationships
- View functionality and access control
- Form validation
- User authentication flows
- Role-based permissions

**Test Coverage**: 18 test cases covering all major functionality

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd campus_marketplace
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Production Deployment

For production deployment:
- Use MySQL database instead of SQLite
- Configure environment variables
- Set DEBUG=False
- Use a production WSGI server (Gunicorn)
- Configure static file serving
- Set up proper logging

## Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (False for production)
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Static Files
- CSS and JS files are served locally (no CDN dependencies)
- Custom Bootstrap theme with campus colors
- Responsive design for mobile and desktop

## API Endpoints

The application uses Django's URL routing system. Key endpoints include:

- Authentication: `/accounts/`
- Products: `/products/`
- Requests: `/requests/`
- Reviews: `/reviews/`
- Notifications: `/notifications/`
- Dashboard: `/dashboard/`

## Future Enhancements

Potential future features:
- Real-time chat between buyers and sellers
- Payment integration
- Mobile app development
- Advanced analytics and reporting
- Email notifications
- Product categories management
- Wishlist/favorites functionality
- Advanced search with filters

## Development Notes

### Code Quality
- Follows Django best practices
- Clean, readable code with comments
- Modular app structure
- Proper error handling
- Form validation and security

### Performance Considerations
- Database query optimization
- Image compression and caching
- Static file optimization
- Efficient template rendering

### Maintenance
- Regular security updates
- Database backup procedures
- User data privacy compliance
- Performance monitoring

## Conclusion

The Campus Marketplace provides a complete solution for campus-based buying and selling, featuring modern web technologies, comprehensive user management, and a scalable architecture suitable for educational institutions.</content>
<parameter name="filePath">d:\Projects\Personal\campus_marketplace\DOCUMENTATION.md