# 🔐 Admin Login - Complete Solution

## ✅ What Was Fixed

### Issue
- Admin login fails with "wrong password"
- Password: admin123 doesn't work

### Root Cause
- Old database had admin with different password (sulaymon123)
- Password hash wasn't being updated on restart

### Solution Applied
**Code in app.py (lines 122-141):**
```python
# CRITICAL FIX: Always reset admin password on startup
cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
admin_user = cursor.fetchone()

admin_password_hash = generate_password_hash('admin123')

if not admin_user:
    # Create new admin
    cursor.execute("INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 1)",
                  ('admin', admin_password_hash))
    print("✅ Admin user created")
else:
    # Update existing admin (FIXES LOGIN ISSUE)
    cursor.execute("UPDATE users SET password_hash = ?, is_admin = 1 WHERE username = ?",
                  (admin_password_hash, 'admin'))
    print("✅ Admin password reset to: admin123")
```

**Result:** Admin password is ALWAYS correct on every startup!

---

## 🚀 Quick Start (Fresh Database)

```bash
# 1. Remove old database
rm -f phishguard.db data/phishguard.db

# 2. Run app
python app.py

# You should see:
# ✅ Admin user created (username: admin, password: admin123)
# OR
# ✅ Admin password reset to: admin123

# 3. Login at http://localhost:5000
# Username: admin
# Password: admin123
```

---

## 🔧 Fix Existing Database

If you have an existing database with wrong password:

### Method 1: Let the app fix it (Automatic)
```bash
# Just restart the app - it will reset admin password automatically
python app.py

# Look for this message:
# ✅ Admin password reset to: admin123
```

### Method 2: Manual database fix
```bash
# Run the test script
python test_admin.py

# It will automatically:
# - Check if admin exists
# - Test password
# - Fix password if broken
```

### Method 3: SQLite direct
```bash
sqlite3 phishguard.db

# Check admin
SELECT username, is_admin FROM users WHERE username='admin';

# If wrong password, delete and let app recreate:
DELETE FROM users WHERE username='admin';
.quit

# Then restart app
python app.py
```

---

## 🧪 Verify Admin Login Works

```bash
# 1. Check startup logs
python app.py

# Look for ONE of these messages:
# ✅ Admin user created (username: admin, password: admin123)
# ✅ Admin password reset to: admin123

# 2. Test login
# Go to http://localhost:5000/login
# Enter: admin / admin123
# Should redirect to: /admin/exam-questions

# 3. Check console output (debug mode)
# You should see:
# 🔍 Login attempt for: admin
#    User found: admin, is_admin: 1
#    ✅ Password verified!
#    ➡️  Redirecting to: admin panel
```

---

## 🔍 Troubleshooting

### Still says "wrong password"?

**Check 1: Database was recreated**
```bash
ls -la *.db data/*.db
# Should see modification time = recent
```

**Check 2: App actually started**
```bash
# Run app and check output
python app.py

# MUST see one of:
# ✅ Admin user created
# ✅ Admin password reset
```

**Check 3: Test password hash directly**
```bash
python test_admin.py

# Should show:
# ✅ Password 'admin123' works!
```

**Check 4: Clear browser cookies**
```
Sometimes old session cookies interfere.
- Clear cookies for localhost:5000
- Try in incognito/private mode
```

---

## 📊 Database Schema

Users table structure:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0,  -- 1 for admin, 0 for regular user
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Admin user should have:
- username = 'admin'
- is_admin = 1
- password_hash = (hash of 'admin123')

---

## ✅ Verification Checklist

- [ ] Old database deleted (or admin password reset)
- [ ] App started successfully
- [ ] Saw "Admin user created" or "Admin password reset" message
- [ ] Opened http://localhost:5000/login
- [ ] Entered admin / admin123
- [ ] Redirected to /admin/exam-questions (not /home)
- [ ] Can see admin panel with question management

If ALL checked ✓ = Admin login working!

---

## 🎯 Credentials Reference

**Default Admin:**
- Username: `admin`
- Password: `admin123`

**This is set in:** `app.py` line 128
**Password reset:** Every time app starts

**⚠️ Security Note:**
For production deployment, change the admin password after first login using the "Change Password" feature.

---

## 🚀 For Render Deployment

On Render, the admin password will be reset on every deployment:
1. Deploy to Render
2. Wait for deployment to complete
3. Check logs for "Admin password reset" message
4. Login with admin / admin123
5. Change password immediately

The password will persist until next deployment (which resets it again).

To avoid this, manually change the admin password in the database after deployment and remove the password reset code from app.py.

---

**Bottom line:** Delete old database → Run app → Login with admin/admin123 → Works! ✅
