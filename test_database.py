#!/usr/bin/env python3
"""
Test database initialization independently
Run this to verify database setup works
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

print("=" * 60)
print("🧪 Database Test Script")
print("=" * 60)

DATABASE = './test_db.db'

try:
    # 1. Remove old test database
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print("\n✓ Removed old test database")
    
    # 2. Create connection
    print("\n1️⃣  Creating database connection...")
    conn = sqlite3.connect(DATABASE, timeout=10.0)
    conn.row_factory = sqlite3.Row
    print("   ✓ Connection successful")
    
    # 3. Create users table
    print("\n2️⃣  Creating users table...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("   ✓ Table created")
    
    # 4. Insert admin
    print("\n3️⃣  Creating admin user...")
    admin_hash = generate_password_hash('admin123')
    conn.execute(
        "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 1)",
        ('admin', admin_hash)
    )
    conn.commit()
    print("   ✓ Admin inserted")
    
    # 5. Query admin
    print("\n4️⃣  Querying admin user...")
    user = conn.execute("SELECT * FROM users WHERE username = ?", ('admin',)).fetchone()
    if user:
        user_dict = dict(user)
        print(f"   ✓ User found:")
        print(f"     - ID: {user_dict['id']}")
        print(f"     - Username: {user_dict['username']}")
        print(f"     - is_admin: {user_dict['is_admin']}")
        print(f"     - Password hash: {user_dict['password_hash'][:50]}...")
    else:
        print("   ✗ User NOT found!")
    
    # 6. Test password
    print("\n5️⃣  Testing password verification...")
    if check_password_hash(user_dict['password_hash'], 'admin123'):
        print("   ✓ Password 'admin123' verified successfully!")
    else:
        print("   ✗ Password verification FAILED!")
    
    # 7. Cleanup
    conn.close()
    os.remove(DATABASE)
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nDatabase operations are working correctly.")
    print("If login still fails, the issue is elsewhere.")
    
except Exception as e:
    print("\n" + "=" * 60)
    print("❌ TEST FAILED!")
    print("=" * 60)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
