# 🚀 Render Deployment Guide (Free Tier)

## ⚠️ IMPORTANT: Why PostgreSQL?

Render's free tier has an **ephemeral filesystem** — the SQLite database
is **deleted every time your service sleeps** (after 15 min of inactivity).

This project now uses **Render's free PostgreSQL** database instead,
which persists your data even when the web service sleeps.

**Note:** Free PostgreSQL databases expire after 30 days on Render.
You'll need to recreate it or upgrade to paid.

---

## 🚀 Deploy (Step by Step)

### Option A: Using render.yaml (Recommended)

1. **Push to GitHub:**
   ```bash
   cd phishguard_final
   git init
   git add .
   git commit -m "Deploy PhishGuard"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO
   git push -u origin main
   ```

2. **On Render Dashboard:**
   - Click "New +" → "Blueprint"
   - Connect your GitHub repo
   - Render reads `render.yaml` and creates:
     - ✅ Web Service (free)
     - ✅ PostgreSQL Database (free)
     - ✅ DATABASE_URL auto-linked
   - Click "Apply"
   - Wait 3-5 minutes

3. **Done!** Login with admin/admin123

### Option B: Manual Setup

1. **Create PostgreSQL Database:**
   - Render Dashboard → "New +" → "PostgreSQL"
   - Name: phishguard-db
   - Plan: Free
   - Click "Create Database"
   - Copy the **Internal Database URL**

2. **Create Web Service:**
   - Render Dashboard → "New +" → "Web Service"
   - Connect your GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Add Environment Variables:**
   - `SECRET_KEY` → Click "Generate"
   - `DATABASE_URL` → Paste the Internal Database URL from step 1

4. **Deploy!**

---

## 🔐 Default Admin

- Username: `admin`
- Password: `admin123`

---

## 🧪 Local Development (SQLite)

When no `DATABASE_URL` is set, the app automatically uses SQLite:

```bash
pip install -r requirements.txt
python app.py
# Uses ./phishguard.db (local only)
```

---

## 📊 How It Works

```
┌────────────────────────────────────────┐
│              Your App                  │
│                                        │
│  DATABASE_URL set?                     │
│    ├── YES → PostgreSQL (persistent!)  │
│    └── NO  → SQLite (local dev only)   │
└────────────────────────────────────────┘
```

The app auto-detects which database to use based on the
`DATABASE_URL` environment variable. No code changes needed.

---

## ✅ What This Solves

| Problem | Before | After |
|---------|--------|-------|
| Service sleeps | DB wiped | DB persists |
| Login after wake | "user not found" | Works! |
| Registered users | Lost on sleep | Saved! |
| Admin questions | Reset on sleep | Saved! |

---

## 🔍 Troubleshooting

### "Database error" on login
**Check:** Is DATABASE_URL set in Render environment variables?

### "relation users does not exist"
**Check:** App startup logs — look for "Database initialization complete"

### Users lost after sleep
**Check:** You're using PostgreSQL, not SQLite. Verify DATABASE_URL is set.

---

## 📋 render.yaml Explained

```yaml
databases:
  - name: phishguard-db     # Creates free PostgreSQL
    plan: free

services:
  - type: web
    envVars:
      - key: DATABASE_URL    # Auto-links to PostgreSQL
        fromDatabase:
          name: phishguard-db
          property: connectionString
```

**This creates both the database AND the web service automatically!**
