## CampusMart

CampusMart is a Django web application for students and small campus vendors. Buyers can browse products, search listings, send purchase requests, review sellers, and receive notifications. Sellers can create products, manage inventory, respond to requests, and view dashboard/analytics summaries.

The project is intentionally simple enough to explain in an academic defense while still showing a clean modular Django structure.

## Core Features

- Buyer and seller registration/login with role-based dashboards
- Product CRUD for sellers
- Product browsing, search, filtering, and detail pages
- Purchase request workflow with statuses: pending, accepted, rejected, completed
- Seller review and rating system
- Notifications for requests, status updates, and reviews
- Product recommendations based on recent product views
- Basic analytics for searches, products, and seller performance
- Optional online currency conversion for FCFA prices
- Optional online media search for products without uploaded images

## Optional Online Feature

Product prices are stored and shown in FCFA. Where exchange rates are available, product cards and product details also show approximate USD/EUR values. FCFA to EUR uses the fixed peg, and EUR to USD is fetched online.

The app uses the public Frankfurter exchange-rate API:

- Website: https://frankfurter.dev/
- API base: `https://api.frankfurter.dev`
- No API key required

If the API is unavailable, the app simply shows FCFA prices only.

## Online Media Enhancement

When a seller does not upload a product image, CampusMart searches Openverse using the product name and category, then shows a relevant online image. Results are cached so repeated page loads stay fast.

If image search is unavailable, the app falls back to a simple category image.

## Tech Stack

- Python
- Django
- SQLite for local development
- Optional MySQL for production-style deployment
- Bootstrap 5
- Requests
- Pillow
- python-dotenv

## Project Structure

```txt
campus_marketplace/
├── analytics/
├── config/
├── core/
├── dashboard/
├── notifications/
├── products/
├── recommendations/
├── requestsystem/
├── reviews/
├── static/
├── templates/
├── users/
├── manage.py
├── requirements.txt
├── README.md
├── DOCUMENTATION.md
└── TODO.md
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```bash
   python manage.py migrate
   ```

4. Optional: seed demo users and products:

   ```bash
   python manage.py seed_demo_data
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Demo Accounts

After running `seed_demo_data`, these local accounts are available:

- Seller: `demo_seller` / `demo12345`
- Buyer: `demo_buyer` / `demo12345`

## Contributors

| Name | Role | GitHub |
| --- | --- | --- |
| Abanda Ambrouise | Product Owner | https://github.com/AmbroiseAB |
| Serge | Backend & Platform | https://github.com/CarmineAkanabe |

## Environment

The app reads `SECRET_KEY` from `.env` or the environment. A harmless local fallback key is included so the project can run easily during demos.

Example `.env`:

```env
SECRET_KEY=replace-this-with-a-real-secret-for-production
```

## Testing

Run:

```bash
python manage.py test
```

On Windows with the included virtual environment:

```powershell
.venv\Scripts\python.exe manage.py test
```
