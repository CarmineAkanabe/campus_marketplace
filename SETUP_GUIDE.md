# CampusMart Setup Guide

This guide explains how to clone, install, seed, test, and run CampusMart on a new PC.

## 1. Requirements

- Python 3.12 or newer recommended
- Git
- Windows PowerShell or a terminal
- Internet connection for dependency installation and optional online features

## 2. Clone the Repository

```powershell
git clone <repository-url>
cd campus_marketplace
```

Replace `<repository-url>` with the real GitHub repository URL.

## 3. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again.

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 5. Environment File

The project can run without a `.env` file because it has a local demo fallback key.

For a cleaner setup, create `.env` in the project root:

```env
SECRET_KEY=replace-this-with-any-long-random-string-for-local-testing
```

## 6. Database Setup

Run migrations:

```powershell
python manage.py migrate
```

## 7. Seed Demo Data

CampusMart includes a Django seeder-like command:

```powershell
python manage.py seed_demo_data
```

It creates demo users and sample products. It is safe to run more than once.

Demo accounts:

```txt
Seller: demo_seller / demo12345
Buyer:  demo_buyer  / demo12345
```

## 8. Run Tests

```powershell
python manage.py test
```

All tests should pass before demoing the app.

## 9. Start the Server

```powershell
python manage.py runserver
```

Open:

```txt
http://127.0.0.1:8000/
```

## 10. Common Issues

If `python` does not work, try:

```powershell
py manage.py runserver
```

If dependencies are missing, make sure the virtual environment is activated and run:

```powershell
pip install -r requirements.txt
```

If the database looks empty, run:

```powershell
python manage.py migrate
python manage.py seed_demo_data
```

If online images or converted prices do not appear, check the internet connection. The app still works without them.
