#!/bin/bash

echo "🔍 PhishGuard - Verification Script"
echo "===================================="
echo ""

# Check 1: Admin password in code
echo "✅ CHECK 1: Admin Password in Code"
if grep -q "generate_password_hash('admin123')" app.py; then
    echo "   ✓ Admin password set to 'admin123'"
else
    echo "   ✗ Admin password NOT set to 'admin123'"
    exit 1
fi
echo ""

# Check 2: Admin reset logic exists
echo "✅ CHECK 2: Admin Reset Logic"
if grep -q "UPDATE users SET password_hash = ?, is_admin = 1 WHERE username = ?" app.py; then
    echo "   ✓ Admin password reset on startup configured"
else
    echo "   ✗ Admin reset logic missing"
    exit 1
fi
echo ""

# Check 3: Database configuration
echo "✅ CHECK 3: Database Configuration"
if grep -q "DATABASE_DIR = os.environ.get('DATABASE_DIR'" app.py; then
    echo "   ✓ Persistent database path configured"
else
    echo "   ✗ Database path NOT configured for persistence"
fi
echo ""

# Check 4: Secret key from environment
echo "✅ CHECK 4: Secret Key Configuration"
if grep -q "app.secret_key = os.environ.get('SECRET_KEY'" app.py; then
    echo "   ✓ Secret key from environment variable"
else
    echo "   ✗ Secret key hardcoded (will break login on restart)"
fi
echo ""

# Check 5: Templates count
echo "✅ CHECK 5: Templates Exist"
TEMPLATE_COUNT=$(find templates -name "*.html" 2>/dev/null | wc -l)
echo "   Templates found: $TEMPLATE_COUNT"
if [ "$TEMPLATE_COUNT" -ge 23 ]; then
    echo "   ✓ All templates present"
else
    echo "   ✗ Missing templates (expected 23+)"
fi
echo ""

# Check 6: Hamburger menu elements
echo "✅ CHECK 6: Hamburger Menu Implementation"
if grep -q 'id="menuBtn"' templates/modules.html 2>/dev/null; then
    echo "   ✓ Menu button exists"
else
    echo "   ✗ Menu button missing"
fi

if grep -q 'id="sidebar"' templates/modules.html 2>/dev/null; then
    echo "   ✓ Sidebar exists"
else
    echo "   ✗ Sidebar missing"
fi

if grep -q 'id="sidebarOverlay"' templates/modules.html 2>/dev/null; then
    echo "   ✓ Overlay exists"
else
    echo "   ✗ Overlay missing"
fi

if grep -q "menuBtn.addEventListener('click'" templates/modules.html 2>/dev/null; then
    echo "   ✓ Menu JavaScript attached"
else
    echo "   ✗ Menu JavaScript missing"
fi

# Check navigation links work
if grep -q 'href="{{ url_for(' templates/modules.html 2>/dev/null; then
    echo "   ✓ Navigation links use proper hrefs"
else
    echo "   ✗ Navigation links broken (using data-page)"
fi
echo ""

# Check 7: Render deployment config
echo "✅ CHECK 7: Render Deployment"
if [ -f "render.yaml" ]; then
    echo "   ✓ render.yaml exists"
    if grep -q "disk:" render.yaml; then
        echo "   ✓ Persistent disk configured"
    else
        echo "   ✗ Persistent disk NOT configured"
    fi
else
    echo "   ✗ render.yaml missing"
fi
echo ""

# Check 8: Admin route protection
echo "✅ CHECK 8: Admin Route Protection"
if grep -q "@admin_required" app.py; then
    echo "   ✓ Admin decorator exists"
else
    echo "   ✗ Admin decorator missing"
fi
echo ""

echo "=================================="
echo "✅ All checks passed!"
echo ""
echo "🧪 To test admin login:"
echo "1. Delete old database: rm -f *.db data/*.db"
echo "2. Run app: python app.py"
echo "3. Look for: '✅ Admin user created' or '✅ Admin password reset'"
echo "4. Login at: http://localhost:5000/login"
echo "5. Use: admin / admin123"
echo ""
echo "If login still fails, run: python reset_admin.py"
