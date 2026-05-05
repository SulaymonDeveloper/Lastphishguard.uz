# Admin Login Test

## Default Admin Credentials
- **Username:** `admin`
- **Password:** `admin123`

## Test Steps

### 1. Fresh Database Test
```bash
# Remove old database
rm -f phishguard.db data/phishguard.db

# Run app
python app.py

# Check output for:
# "✅ Admin user created (username: admin, password: admin123)"
```

### 2. Login Test
1. Go to http://localhost:5000
2. Click "Login"
3. Enter:
   - Username: `admin`
   - Password: `admin123`
4. Should redirect to `/admin/exam-questions`

### 3. Session Persistence Test
1. Login as admin
2. Stop server
3. Start server again
4. Refresh page
5. Should still be logged in (if SECRET_KEY unchanged)

### 4. Admin Panel Test
1. After login, you should see admin panel
2. Try adding a test question
3. Try editing a question
4. Try deleting a question

## Troubleshooting

### Login fails with "Invalid username or password"
**Check:**
1. Database was created (phishguard.db exists)
2. Admin user exists: `sqlite3 phishguard.db "SELECT username, is_admin FROM users WHERE username='admin'"`
3. Password hash exists: Should see a long hash string

### Redirects to /home instead of /admin
**Check:**
1. is_admin column value: Should be 1
2. Session is_admin: Add print statement in login route

### Can't access /admin/exam-questions
**Check:**
1. User is_admin = 1 in database
2. Session contains is_admin = 1
3. @admin_required decorator is working
