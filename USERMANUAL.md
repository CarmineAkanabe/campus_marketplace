# CampusMart User Manual

CampusMart is a simple campus marketplace for buyers and sellers.

## 1. Starting the App

From the project folder, run:

```powershell
.venv\Scripts\python.exe manage.py runserver
```

Open:

```txt
http://127.0.0.1:8000/
```

## 2. Demo Accounts

If demo data has been seeded, use:

| Role | Username | Password |
| --- | --- | --- |
| Seller | `demo_seller` | `demo12345` |
| Buyer | `demo_buyer` | `demo12345` |

## 3. Public Visitor

Public visitors can:

- View the homepage
- Browse available products
- Search and filter products
- View product details
- Register or login
- Read the About page

## 4. Buyer Workflow

1. Login as a buyer.
2. Browse products from the Products page.
3. Open a product detail page.
4. Click **Send request**.
5. Enter a message for the seller.
6. Track sent requests from **Menu > My Requests**.
7. When a request is accepted or completed, leave a seller review.
8. Check recommendations from **Menu > Recommendations**.
9. Check notifications from the navbar.

## 5. Seller Workflow

1. Login as a seller.
2. Use **Menu > Create Product** or the product list button to add a product.
3. Fill in name, category, price, condition, status, description, and optional image.
4. View incoming requests from **Menu > Incoming Requests**.
5. Open a request and update its status.
6. Use the dashboard to view products, request counts, and recent activity.

## 6. Product Images

Sellers can upload product images. If no image is uploaded, CampusMart searches online using the product name and category, then displays a relevant fallback image to keep listings visually clear during demos.

## 7. Online Features

CampusMart includes two simple online enhancements:

- Product prices can show approximate USD/EUR values.
- Products without uploaded photos can show keyword-matched online images.

Both features fail safely. If the internet is unavailable, the app still works.

## 8. Admin

Create an admin user with:

```powershell
.venv\Scripts\python.exe manage.py createsuperuser
```

Open:

```txt
http://127.0.0.1:8000/admin/
```

Admins can manage users, products, requests, reviews, notifications, and analytics data.
