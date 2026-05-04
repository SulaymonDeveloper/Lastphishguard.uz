#!/usr/bin/env python3
"""
Emergency admin reset script
Run this if admin login doesn't work
"""
import sqlite3
from werkzeug.security import generate_password_hash
import os
import sys

DATABASE_DIR = os.environ.get('DATABASE_DIR', '.')
DATABASE = os.path.join(DATABASE_DIR, 'phishguard.db')

print("🔧 PhishGuard Admin Reset")
print("=" * 50)

if not os.path.exists(DATABASE):
    print(f"❌ Database not found: {DATABASE}")
    print("   Run 'python app.py' first to create database")
    sys.exit(1)

print(f"📊 Database: {DATABASE}")

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Delete existing admin if exists
cursor.execute("DELETE FROM users WHERE username = 'admin'")

# Create fresh admin with admin123
admin_hash = generate_password_hash('admin123')
cursor.execute(
    "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 1)",
    ('admin', admin_hash)
)

conn.commit()
conn.close()

print("✅ Admin user reset successfully!")
print()
print("   Username: admin")
print("   Password: admin123")
print()
print("=" * 50)
print("You can now login at http://localhost:5000/login")
