#!/usr/bin/env python
"""
Database reset and migration script
Handles clearing migration history and applying migrations fresh
"""
import os
import django
import MySQLdb

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Connect to MySQL directly and drop/create database
connection = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='2370',
    port=3306
)
cursor = connection.cursor()

try:
    # Drop and recreate database
    cursor.execute("DROP DATABASE IF EXISTS campus_marketplace")
    cursor.execute("CREATE DATABASE campus_marketplace")
    connection.commit()
    print("✓ Database dropped and recreated")
except Exception as e:
    print(f"✗ Error resetting database: {e}")
finally:
    cursor.close()
    connection.close()

# Now run migrations
from django.core.management import execute_from_command_line
print("✓ Running migrations...")
execute_from_command_line(['manage.py', 'migrate'])
print("✓ Migrations completed successfully")
