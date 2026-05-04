#!/usr/bin/env python3
"""
Test script to verify admin user creation and login
"""
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

DATABASE_DIR = os.environ.get('DATABASE_DIR', '.')
DATABASE = os.path.join(DATABASE_DIR, 'phishguard.db')

print("🧪 Admin User Test Script")
print("=" * 50)
print(f"Database: {DATABASE}")
print()

# Connect to database
conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check if admin exists
print("1️⃣  Checking if admin user exists...")
admin = cursor.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()

if admin:
    print(f"   ✅ Admin found!")
    print(f"      ID: {admin['id']}")
    print(f"      Username: {admin['username']}")
    print(f"      is_admin: {admin['is_admin']}")
    print(f"      Password hash: {admin['password_hash'][:50]}...")
    print()
    
    # Test password
    print("2️⃣  Testing password 'admin123'...")
    if check_password_hash(admin['password_hash'], 'admin123'):
        print("   ✅ Password 'admin123' works!")
    else:
        print("   ❌ Password 'admin123' does NOT work!")
        print("   🔧 Fixing password...")
        new_hash = generate_password_hash('admin123')
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (new_hash,))
        conn.commit()
        print("   ✅ Password reset to 'admin123'")
else:
    print("   ❌ Admin NOT found!")
    print("   🔧 Creating admin user...")
    admin_hash = generate_password_hash('admin123')
    cursor.execute(
        "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 1)",
        ('admin', admin_hash)
    )
    conn.commit()
    print("   ✅ Admin created with password 'admin123'")

print()
print("3️⃣  Final verification...")
admin = cursor.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
if admin and check_password_hash(admin['password_hash'], 'admin123'):
    print("   ✅ Admin login will work with: admin / admin123")
else:
    print("   ❌ Admin login still broken!")

conn.close()
print()
print("=" * 50)
print("Test complete!")
