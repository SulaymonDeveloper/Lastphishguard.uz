# Hamburger Menu - Implementation Details

## How It Works

### HTML Structure
```html
<!-- Menu Button (in header) -->
<button class="menu-btn" id="menuBtn">
    <div class="menu-icon">
        <span></span>
        <span></span>
        <span></span>
    </div>
</button>

<!-- Sidebar (hidden by default) -->
<nav class="sidebar" id="sidebar">
    <!-- Menu content -->
</nav>

<!-- Overlay (appears when menu is open) -->
<div class="sidebar-overlay" id="sidebarOverlay"></div>
```

### CSS
- **Sidebar:** Positioned fixed, starts at `left: -320px` (off-screen)
- **Active State:** When `.active` class added, moves to `left: 0`
- **Overlay:** Hidden by default, shows with `.active` class
- **Z-index:** Overlay=999, Sidebar=1000

### JavaScript
```javascript
// Open menu
menuBtn.addEventListener('click', () => {
    sidebar.classList.add('active');
    sidebarOverlay.classList.add('active');
});

// Close menu (X button)
closeSidebar.addEventListener('click', () => {
    sidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
});

// Close menu (click outside)
sidebarOverlay.addEventListener('click', () => {
    sidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
});
```

## Mobile Responsive
- **Desktop:** Sidebar hidden, menu button visible
- **Mobile (<768px):** 
  - Sidebar width: 280px
  - Starting position: left: -280px
  - Full-screen overlay when open

## Common Issues & Fixes

### Issue: Menu button not clickable
**Fix:** Check z-index of header elements. Menu button should be clickable.

### Issue: Menu doesn't open
**Check:**
1. JavaScript loaded (check browser console for errors)
2. Element IDs match: `menuBtn`, `sidebar`, `sidebarOverlay`, `closeSidebar`
3. CSS transitions not disabled

### Issue: Menu opens but can't close
**Check:**
1. Close button exists with id="closeSidebar"
2. Overlay click listener working
3. CSS `.active` class removes properly

### Issue: Menu content not scrollable
**Fix:** Sidebar has `overflow-y: auto` in CSS

### Issue: Page scrolls with menu open
**Fix:** Add to body when menu opens:
```javascript
document.body.style.overflow = 'hidden';
```

## Testing Checklist

- [ ] Menu button visible on mobile
- [ ] Click menu button → sidebar slides in
- [ ] Overlay appears (dimmed background)
- [ ] Click X button → menu closes
- [ ] Click outside (overlay) → menu closes
- [ ] Click menu link → menu closes and navigates
- [ ] Sidebar content scrollable if needed
- [ ] No horizontal overflow on any screen size

## Verified Working
✅ All event listeners attached  
✅ CSS transitions smooth  
✅ Z-index layering correct  
✅ Mobile responsive  
✅ Touch-friendly button sizes  
