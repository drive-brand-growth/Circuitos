# Fix Content-Type Issue (2 Minutes)

## Problem
HTML files are showing as plain text instead of rendering.

## Quick Fix

### Option 1: Re-upload via Supabase Dashboard (Easiest - 2 min)

1. Go to: https://supabase.com/dashboard/project/kymixjuynffjvnrwmcpk/storage/buckets/circuit-os-dashboards

2. Delete these files:
   - `main-dashboard.html`
   - All files in `Dashboards/` folder

3. Re-upload them:
   - Click "Upload file"
   - Select `main-dashboard.html` from `/Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE/`
   - Click into `Dashboards` folder
   - Upload all HTML files from `Dashboards/` folder

Supabase will auto-detect `.html` files and set correct content-type.

### Option 2: Use This Script

```bash
cd /Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE
chmod +x fix-content-type.sh
./fix-content-type.sh
```

I'll create the script now...

## Why This Happened

When uploading via curl with `--data-binary`, the content-type defaults to `application/octet-stream` or `text/plain`.

Using `-F file=@filename` (form upload) lets Supabase auto-detect the correct MIME type from the `.html` extension.

## Test After Fix

Open this URL - it should render the dashboard, not show code:
```
https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/main-dashboard.html
```
