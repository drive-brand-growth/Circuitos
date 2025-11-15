# QUICK FIX - 2 Minutes

## The Problem
HTML files are showing as source code instead of rendering.

## The Fix (Super Easy)

### In the Supabase window that just opened:

1. **Delete `main-dashboard.html`:**
   - Click the checkbox next to `main-dashboard.html`
   - Click "Delete" button
   - Confirm

2. **Re-upload `main-dashboard.html`:**
   - Click "Upload file" button
   - From the Finder window, select `main-dashboard.html`
   - Click "Upload"
   - ✅ Done!

3. **Fix Dashboards folder:**
   - Click into `Dashboards` folder
   - Select ALL HTML files (click checkboxes)
   - Click "Delete"
   - Confirm
   - Click "Upload file"
   - From Finder → Dashboards folder, select ALL .html files
   - Click "Upload"
   - ✅ Done!

### Test
Open this URL - should render properly now:
```
https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/main-dashboard.html
```

## Why This Fixes It

When you upload via the web interface, Supabase automatically detects `.html` files and sets the content-type to `text/html`, which makes browsers render them properly instead of showing source code.

---

**Total time: 2 minutes**

Just delete and re-upload - that's it!
