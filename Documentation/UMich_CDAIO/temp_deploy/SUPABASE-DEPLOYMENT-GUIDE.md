# Supabase Storage Deployment Guide

## Overview
Deploy Circuit OS dashboards to Supabase Storage for reliable, scalable cloud hosting.

## Prerequisites
- Supabase account (free tier available)
- Project created at https://app.supabase.com

## Deployment Methods

### Method 1: Web Interface (Easiest)

#### Step 1: Create Storage Bucket
1. Go to https://app.supabase.com
2. Select your project (or create new one)
3. Click "Storage" in left sidebar
4. Click "New bucket"
5. Bucket name: `circuit-os-dashboards`
6. Public bucket: ✅ YES (for web hosting)
7. Click "Create bucket"

#### Step 2: Upload Files

**Upload these folders/files:**

1. **Root Files:**
   - `index.html`
   - `main-dashboard.html`
   - `circuit-animations.js`
   - `COLOR-PALETTE-GUIDE.html`

2. **Dashboards Folder** (entire folder):
   - `Dashboards/caio-university.html`
   - `Dashboards/interactive-demo.html`
   - `Dashboards/sales-team-dashboard.html`
   - `Dashboards/unified-demo-dashboard.html`
   - `Dashboards/lead-processing-demo.html`

3. **Brand-Assets Folder** (entire folder):
   - All SVG logos
   - `circuit-os-executive-logo.svg`
   - `circuit-os-logo.svg`
   - etc.

**How to upload:**
1. In Supabase Storage, click your bucket
2. Click "Upload file" or "Upload folder"
3. Select files/folders from `/Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE/`
4. Wait for upload to complete

#### Step 3: Get Public URLs
After uploading, each file gets a public URL:

**Format:**
```
https://[PROJECT_ID].supabase.co/storage/v1/object/public/circuit-os-dashboards/[FILE_PATH]
```

**Examples:**
- Main Dashboard: `https://xxx.supabase.co/storage/v1/object/public/circuit-os-dashboards/main-dashboard.html`
- CAIO University: `https://xxx.supabase.co/storage/v1/object/public/circuit-os-dashboards/Dashboards/caio-university.html`

### Method 2: Supabase CLI (Advanced)

#### Setup
```bash
# Install Supabase CLI
brew install supabase/tap/supabase

# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref YOUR_PROJECT_ID
```

#### Deploy All Files
```bash
cd /Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE

# Upload all HTML files
supabase storage upload circuit-os-dashboards *.html

# Upload Dashboards folder
supabase storage upload circuit-os-dashboards/Dashboards Dashboards/*.html

# Upload Brand Assets
supabase storage upload circuit-os-dashboards/Brand-Assets Brand-Assets/*
```

## Files to Upload (Priority Order)

### Essential Files (Must Upload)
```
1. main-dashboard.html (4KB) - Main entry point
2. index.html (15KB) - Landing page
3. Dashboards/caio-university.html (172KB)
4. Dashboards/interactive-demo.html (31KB)
5. Dashboards/sales-team-dashboard.html (39KB)
6. Dashboards/unified-demo-dashboard.html (35KB)
7. Brand-Assets/circuit-os-executive-logo.svg (5.3KB)
8. circuit-animations.js (17KB)
```

### Optional Files (Nice to Have)
```
- All documentation .md files
- DEPLOY-WITH-SSL.sh
- COLOR-PALETTE-GUIDE.html
- Other brand assets
```

## Storage Size Estimate
- **Essential files:** ~350KB
- **All files:** ~2.5MB
- **Supabase free tier:** 1GB (plenty of space!)

## Access Your Deployed Site

### Find Your Public URL
1. In Supabase dashboard → Storage
2. Click on `circuit-os-dashboards` bucket
3. Click any file → "Get public URL"
4. Copy the base URL (everything before the filename)

### Your Live URLs
Replace `[YOUR_PROJECT_URL]` with your actual Supabase project URL:

**Main Dashboard:**
```
[YOUR_PROJECT_URL]/storage/v1/object/public/circuit-os-dashboards/main-dashboard.html
```

**Individual Dashboards:**
```
[YOUR_PROJECT_URL]/storage/v1/object/public/circuit-os-dashboards/Dashboards/caio-university.html
[YOUR_PROJECT_URL]/storage/v1/object/public/circuit-os-dashboards/Dashboards/interactive-demo.html
[YOUR_PROJECT_URL]/storage/v1/object/public/circuit-os-dashboards/Dashboards/sales-team-dashboard.html
```

## Update HTML Files for Production (Optional)

If you want to use a custom domain or CDN, update the paths in your HTML files:

### Update main-dashboard.html
Change iframe sources from:
```html
<iframe src="Dashboards/caio-university.html">
```

To:
```html
<iframe src="https://YOUR_PROJECT_URL/storage/v1/object/public/circuit-os-dashboards/Dashboards/caio-university.html">
```

## Bucket Configuration

### Recommended Settings
```
Bucket name: circuit-os-dashboards
Public: ✅ Yes
File size limit: 50MB
Allowed MIME types: */* (all types)
```

### Security Policies (RLS)
For public dashboards, use this policy:

```sql
-- Allow public read access
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'circuit-os-dashboards' );

-- Allow authenticated uploads (optional)
CREATE POLICY "Authenticated uploads"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'circuit-os-dashboards' AND auth.role() = 'authenticated' );
```

## Advantages of Supabase Storage

✅ **Free tier:** 1GB storage
✅ **Global CDN:** Fast worldwide delivery
✅ **99.9% uptime:** Reliable hosting
✅ **Easy updates:** Drag & drop file replacement
✅ **No build process:** Upload static files directly
✅ **HTTPS by default:** Secure connections
✅ **Version control:** Via git + manual uploads

## Quick Deploy Checklist

- [ ] Create Supabase account
- [ ] Create new project
- [ ] Create storage bucket `circuit-os-dashboards`
- [ ] Set bucket to PUBLIC
- [ ] Upload `main-dashboard.html`
- [ ] Upload `Dashboards/` folder
- [ ] Upload `Brand-Assets/` folder
- [ ] Upload `circuit-animations.js`
- [ ] Get public URL
- [ ] Test main dashboard in browser
- [ ] Test all 4 dashboard tabs
- [ ] Share URL with team!

## Support & Resources

- **Supabase Docs:** https://supabase.com/docs/guides/storage
- **Storage Dashboard:** https://app.supabase.com/project/_/storage
- **Community Support:** https://github.com/supabase/supabase/discussions

---

**Deployment Time:** ~10 minutes for manual upload
**Total Cost:** $0 (free tier)

🤖 Generated with Claude Code
