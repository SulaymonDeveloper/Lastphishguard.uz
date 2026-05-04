# 🚀 PhishGuard - Quick Start Guide

**Get admin login working in 60 seconds!**

---

## ⚡ Fast Track (Local Testing)

```bash
# 1. Extract ZIP
unzip phishguard_final_complete.zip
cd phishguard_final

# 2. Delete any old databases (CRITICAL!)
rm -f *.db data/*.db

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run app
python app.py

# ✅ You MUST see one of these messages:
# "✅ Admin user created (username: admin, password: admin123)"
# "✅ Admin password reset to: admin123"
```

**If you don't see the message above, the app didn't start correctly!**

```bash
# 5. Open browser
# Go to: http://localhost:5000

# 6. Click "Login"
# Enter:
#   Username: admin
#   Password: admin123

# 7. Success!
# You should be redirected to: /admin/exam-questions
```

---

## 🔧 If Admin Login STILL Fails

### Emergency Fix #1: Force Admin Reset
```bash
# Stop the app (Ctrl+C)

# Run emergency reset script
python reset_admin.py

# Restart app
python app.py

# Try login again
```

### Emergency Fix #2: Complete Fresh Start
```bash
# Stop the app (Ctrl+C)

# Delete EVERYTHING database-related
rm -rf *.db data/ __pycache__/

# Recreate data directory
mkdir -p data

# Run app
python app.py

# Login: admin / admin123
```

### Emergency Fix #3: Check What's Actually Happening
```bash
# Run the app and watch console output carefully

python app.py

# You MUST see:
# 📊 Database: /path/to/phishguard.db
# ✅ Admin user created (username: admin, password: admin123)
#    OR
# ✅ Admin password reset to: admin123

# If you don't see these messages, something is wrong!
```

---

## 🧪 Test Admin Login Works

After app starts, look for these console messages when you try to login:

```
🔍 Login attempt for: admin
   User found: admin, is_admin: 1
   ✅ Password verified!
   ➡️  Redirecting to: admin panel
```

If you see `❌ Password verification failed!`, run `python reset_admin.py`

---

## 🌐 Deploy to Render

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Deploy PhishGuard"
git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main

# 2. Create Web Service on Render
# - Connect GitHub repo
# - render.yaml will auto-configure everything

# 3. Check Render Logs
# Look for:
# ✅ Admin password reset to: admin123

# 4. Login
# Go to your Render URL
# Login: admin / admin123
```

---

## 📋 Verification Checklist

Before you say "it doesn't work", verify:

- [ ] Deleted old database files (`rm -f *.db data/*.db`)
- [ ] Saw "Admin user created" or "Admin password reset" message in console
- [ ] Console shows database path (e.g., `📊 Database: /path/to/phishguard.db`)
- [ ] Cleared browser cookies / tried incognito mode
- [ ] Using correct credentials: `admin` / `admin123` (not sulaymon123!)
- [ ] Tried emergency reset script: `python reset_admin.py`

If ALL checked and still fails → There's a different issue (check console for errors)

---

## ⚙️ Admin Panel Features

Once logged in as admin, you can:

✅ **View all exam questions**
✅ **Add new questions** (bilingual EN + UZ)
✅ **Edit existing questions**
✅ **Delete questions**
✅ **Changes persist** across restarts

Access: `/admin/exam-questions`

---

## 🎯 Default Credentials

**Username:** `admin`  
**Password:** `admin123`

**This password is reset EVERY TIME the app starts!**

To set a permanent password:
1. Login as admin
2. Navigate to "Change Password"
3. Set your new password
4. (Optional) Remove the password reset code from `app.py` line 135-138

---

## 📱 Test Hamburger Menu

1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select mobile device (e.g., iPhone 12)
4. Click the ☰ button (top left)
5. Menu should slide in smoothly
6. Click outside or X to close

---

## 🔍 Common Issues

### "Invalid username or password"
- Delete database: `rm -f *.db data/*.db`
- Restart app
- Watch for "Admin created" message

### Page just refreshes (doesn't login)
- Check console for error messages
- Try incognito/private browsing
- Clear cookies for localhost:5000

### Redirects to /home instead of /admin
- Admin's `is_admin` value is 0 (should be 1)
- Run: `python reset_admin.py`

### "Database is locked"
- Stop all running instances
- Delete database
- Restart

---

## 📚 Full Documentation

- `README.md` - Project overview
- `DEPLOYMENT_GUIDE.md` - Complete deployment guide
- `ADMIN_LOGIN_SOLUTION.md` - Detailed admin login troubleshooting
- `HAMBURGER_MENU_FIX.md` - Menu implementation details
- `FIXES_APPLIED.md` - All fixes documented

---

**Bottom Line:**

```bash
rm -f *.db data/*.db  # Delete old database
python app.py          # Must see "Admin created" message
# Login at localhost:5000 with admin/admin123
```

That's it! 🎉
