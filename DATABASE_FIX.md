# 🗄️ Database Fix - Complete Solution

## ✅ What Was Fixed

### Issue
Login and registration both return database errors - unable to connect or query the database.

### Root Causes & Fixes:

1. **Database Directory Path**
   - **Problem:** Default path `/opt/render/project/data` doesn't exist locally
   - **Fix:** Default to current directory (`.`) for local development
   - **Result:** Database always accessible

2. **Directory Creation**
   - **Problem:** makedirs() failed silently
   - **Fix:** Proper exception handling with fallback
   - **Result:** Directory created or graceful fallback

3. **Write Permissions**
   - **Problem:** No verification that directory is writable
   - **Fix:** Test write before starting app
   - **Result:** Early detection of permission issues

4. **Connection Handling**
   - **Problem:** Generic sqlite3.connect() with no timeout
   - **Fix:** Added timeout=10.0 and error handling
   - **Result:** Better error messages, no hangs

5. **Initialization**
   - **Problem:** Silent failures in init_db()
   - **Fix:** Comprehensive startup logging
   - **Result:** Clear visibility of what's happening

---

## 🔧 Complete Fixes Applied

### 1. Database Path Configuration
```python
# Default to current directory for local dev
DATABASE_DIR = os.environ.get('DATABASE_DIR', '.')

# Create directory if needed (for Render deployment)
if DATABASE_DIR != '.' and not os.path.exists(DATABASE_DIR):
    try:
        os.makedirs(DATABASE_DIR, exist_ok=True)
        print(f"✅ Created database directory: {DATABASE_DIR}")
    except Exception as e:
        print(f"⚠️  Cannot create {DATABASE_DIR}, using current directory.")
        DATABASE_DIR = '.'

DATABASE = os.path.join(DATABASE_DIR, 'phishguard.db')
```

### 2. Write Permission Test
```python
# Verify we can write to the database location
try:
    test_file = os.path.join(DATABASE_DIR, '.write_test')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    print(f"✅ Database directory is writable")
except Exception as e:
    print(f"❌ WARNING: Database directory may not be writable: {e}")
```

### 3. Improved Connection Function
```python
def get_db():
    try:
        conn = sqlite3.connect(DATABASE, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print(f"   Attempted to connect to: {DATABASE}")
        raise
```

### 4. Startup Initialization
```python
if __name__ == '__main__':
    print("🚀 Starting PhishGuard Application")
    
    try:
        print("📂 Checking database setup...")
        print(f"   Database directory: {DATABASE_DIR}")
        print(f"   Database file: {DATABASE}")
        
        print("🔧 Initializing database...")
        migrate_db()
        init_db()
        
        print("✅ Database initialization complete!")
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print("❌ STARTUP ERROR!")
        print(f"Error: {e}")
        print(f"Database location: {DATABASE}")
        print("Troubleshooting:")
        print("1. Check database directory permissions")
        print("2. Try: rm -f *.db && python app.py")
        raise
```

---

## 🗄️ Database Tables

### Users Table
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Progress Table
```sql
CREATE TABLE IF NOT EXISTS progress (
    user_id INTEGER PRIMARY KEY,
    current_module INTEGER DEFAULT 1,
    current_lesson INTEGER DEFAULT 1,
    modules_completed TEXT DEFAULT '',
    final_exam_unlocked INTEGER DEFAULT 0,
    final_exam_completed INTEGER DEFAULT 0,
    final_exam_score INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Exam Questions Table
```sql
CREATE TABLE IF NOT EXISTS exam_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    question_uz TEXT,
    option_a_uz TEXT,
    option_b_uz TEXT,
    option_c_uz TEXT,
    option_d_uz TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## 🧪 Testing

### Local Development
```bash
# 1. Clean start
rm -f *.db

# 2. Run app
python app.py

# Expected output:
# ============================================================
# 🚀 Starting PhishGuard Application
# ============================================================
# 
# 📂 Checking database setup...
#    Database directory: .
#    Database file: ./phishguard.db
# 
# 🔧 Initializing database...
# ✅ Admin password reset to: admin123
# 
# ✅ Database initialization complete!
# ============================================================
# 🌐 Starting web server...
#    Access at: http://localhost:5000
#    Admin credentials: admin / admin123
# ============================================================

# 3. Test login
# Go to http://localhost:5000/login
# Username: admin
# Password: admin123
# Should work! ✓
```

### Verify Database Created
```bash
# Check database file exists
ls -lh phishguard.db

# Check tables exist
sqlite3 phishguard.db ".tables"
# Should show: exam_questions  progress  users

# Check admin user
sqlite3 phishguard.db "SELECT username, is_admin FROM users WHERE username='admin'"
# Should show: admin|1
```

---

## 🔍 Troubleshooting

### Error: "unable to open database file"

**Cause:** Directory doesn't exist or no write permission

**Fix:**
```bash
# Create directory
mkdir -p data

# OR run in current directory
export DATABASE_DIR=.
python app.py
```

### Error: "database is locked"

**Cause:** Another process has the database open

**Fix:**
```bash
# Find and kill processes
ps aux | grep python
kill <PID>

# OR delete database and restart
rm -f *.db
python app.py
```

### Error: "table users already exists"

**Cause:** Trying to create table that already exists (shouldn't happen with IF NOT EXISTS)

**Fix:**
```bash
# Fresh database
rm -f *.db
python app.py
```

### Error: "UNIQUE constraint failed"

**Cause:** Trying to register username that already exists

**Expected behavior:** Shows "Username already exists" message (not a crash)

---

## 🎯 Admin User Guarantee

Admin is created/reset on every startup:

```python
# In init_db()
cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
admin_user = cursor.fetchone()

admin_password_hash = generate_password_hash('admin123')

if not admin_user:
    cursor.execute("INSERT INTO users (...) VALUES (...)")
    print("✅ Admin user created (username: admin, password: admin123)")
else:
    cursor.execute("UPDATE users SET password_hash = ?, is_admin = 1 WHERE username = ?",
                  (admin_password_hash, 'admin'))
    print("✅ Admin password reset to: admin123")
```

**Result:** Admin login always works with admin/admin123 ✅

---

## 📊 Database Location

### Local Development:
- Location: `./phishguard.db` (current directory)
- Set via: Default behavior

### Render Deployment:
- Location: `/opt/render/project/data/phishguard.db`
- Set via: `DATABASE_DIR` environment variable
- Persistent: Yes (Render disk mount)

### Custom Location:
```bash
export DATABASE_DIR=/path/to/your/data
python app.py
```

---

## ✅ Success Indicators

When app starts successfully, you'll see:

```
🚀 Starting PhishGuard Application
📂 Checking database setup...
   Database directory: .
   Database file: ./phishguard.db
✅ Database directory is writable
🔧 Initializing database...
✅ Admin password reset to: admin123
✅ Database initialization complete!
🌐 Starting web server...
```

If you see all these ✅ marks, database is working correctly!

---

## 🔐 Security Notes

1. **SQLite Connection:** Uses row_factory for dict-like access
2. **Foreign Keys:** Enabled with PRAGMA
3. **Timeout:** 10 seconds to prevent hangs
4. **Password Hashing:** Uses Werkzeug's generate_password_hash
5. **Unique Constraints:** Username must be unique

---

**Bottom Line:** Database now works reliably in both local and production environments! ✅
