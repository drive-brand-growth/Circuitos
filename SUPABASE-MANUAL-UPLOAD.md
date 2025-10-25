# Supabase Manual Upload (5 Minutes)

## Your Project
**Project ID:** kymixjuynffjvnrwmcpk
**Dashboard:** https://supabase.com/dashboard/project/kymixjuynffjvnrwmcpk

## Quick Upload (No CLI Required)

### Step 1: Create Storage Bucket (1 min)
1. Go to: https://supabase.com/dashboard/project/kymixjuynffjvnrwmcpk/storage/buckets
2. Click "New bucket"
3. Bucket name: `circuit-os-dashboards`
4. Toggle "Public bucket" to **ON** ✅
5. Click "Create bucket"

### Step 2: Upload Files (3 min)

#### Upload Root Files
1. Click on `circuit-os-dashboards` bucket
2. Click "Upload file"
3. Select these files from `/Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE/`:
   - `main-dashboard.html`
   - `index.html`
   - `circuit-animations.js`

#### Upload Dashboards Folder
1. In bucket, click "New folder"
2. Name it: `Dashboards`
3. Click into `Dashboards` folder
4. Click "Upload file"
5. Select ALL files from `/Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE/Dashboards/`:
   - `caio-university.html`
   - `interactive-demo.html`
   - `sales-team-dashboard.html`
   - `unified-demo-dashboard.html`
   - `lead-processing-demo.html`

#### Upload Brand-Assets Folder
1. Go back to bucket root (click `circuit-os-dashboards` breadcrumb)
2. Click "New folder"
3. Name it: `Brand-Assets`
4. Click into `Brand-Assets` folder
5. Click "Upload file"
6. Select ALL .svg files from `/Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE/Brand-Assets/`:
   - `circuit-os-executive-logo.svg`
   - `circuit-os-logo.svg`
   - `circuit-os-icon.svg`
   - `circuit-os-horizontal.svg`
   - All other SVG files

### Step 3: Get Your Live URLs (1 min)

After uploading, your dashboards are live at:

**Main Dashboard:**
```
https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/main-dashboard.html
```

**Individual Dashboards:**
```
https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/Dashboards/caio-university.html

https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/Dashboards/interactive-demo.html

https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/Dashboards/sales-team-dashboard.html

https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/Dashboards/unified-demo-dashboard.html
```

## Verification

Test each URL in your browser:
- [ ] Main dashboard loads
- [ ] All 4 tabs work
- [ ] Logos display correctly
- [ ] Animations work smoothly

## Files to Upload Checklist

### Essential (Must Upload):
- [ ] main-dashboard.html
- [ ] index.html
- [ ] circuit-animations.js
- [ ] Dashboards/caio-university.html
- [ ] Dashboards/interactive-demo.html
- [ ] Dashboards/sales-team-dashboard.html
- [ ] Dashboards/unified-demo-dashboard.html
- [ ] Brand-Assets/circuit-os-executive-logo.svg
- [ ] Brand-Assets/circuit-os-logo.svg

### Optional:
- [ ] All other SVG files in Brand-Assets/
- [ ] Dashboards/lead-processing-demo.html
- [ ] Documentation files (.md)

## Troubleshooting

### Files won't upload
- Check file size (should be under 50MB each)
- Make sure bucket is PUBLIC
- Try refreshing the page

### URLs don't work
- Verify bucket name is exactly: `circuit-os-dashboards`
- Check bucket is set to PUBLIC
- Wait 30 seconds after upload for CDN to sync

### Images/logos not loading
- Make sure Brand-Assets folder structure matches exactly
- Upload all SVG files
- Check file names match (case-sensitive)

## Quick Access

**Supabase Storage Dashboard:**
https://supabase.com/dashboard/project/kymixjuynffjvnrwmcpk/storage/buckets

**Your Files Location:**
`/Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE/`

---

**Total Time:** 5 minutes
**Total Cost:** $0 (free tier: 1GB storage)

🎉 Your Circuit OS will be live worldwide with CDN!
