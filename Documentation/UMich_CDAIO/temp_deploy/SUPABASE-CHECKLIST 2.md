# Supabase Upload Checklist

## What Your Bucket Should Look Like

After uploading correctly, your `circuit-os-dashboards` bucket should have this structure:

```
circuit-os-dashboards/
├── main-dashboard.html           ← uploaded directly to root
├── index.html                    ← uploaded directly to root
├── circuit-animations.js         ← uploaded directly to root
├── Dashboards/                   ← folder you created
│   ├── caio-university.html
│   ├── interactive-demo.html
│   ├── sales-team-dashboard.html
│   ├── unified-demo-dashboard.html
│   └── lead-processing-demo.html
└── Brand-Assets/                 ← folder you created
    ├── circuit-os-executive-logo.svg
    ├── circuit-os-logo.svg
    ├── circuit-os-icon.svg
    └── (other SVG files)
```

## Check Your Upload

### In Supabase Dashboard:
1. Go to: https://supabase.com/dashboard/project/kymixjuynffjvnrwmcpk/storage/buckets/circuit-os-dashboards
2. You should see:
   - [ ] 3 files in the root (main-dashboard.html, index.html, circuit-animations.js)
   - [ ] 1 folder called "Dashboards"
   - [ ] 1 folder called "Brand-Assets"

### Click into Dashboards folder:
- [ ] Should have 5 HTML files

### Click into Brand-Assets folder:
- [ ] Should have 8+ SVG files

## Test URLs

After correct upload, these URLs should work:

**Main Dashboard (test this first!):**
```
https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/main-dashboard.html
```

**CAIO University:**
```
https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/Dashboards/caio-university.html
```

**Logo (test if images work):**
```
https://kymixjuynffjvnrwmcpk.supabase.co/storage/v1/object/public/circuit-os-dashboards/Brand-Assets/circuit-os-executive-logo.svg
```

## Common Mistakes

### ❌ Wrong: Uploaded everything in root
```
circuit-os-dashboards/
├── main-dashboard.html
├── index.html
├── caio-university.html          ← Should be in Dashboards folder!
├── interactive-demo.html         ← Should be in Dashboards folder!
├── circuit-os-logo.svg           ← Should be in Brand-Assets folder!
└── ...
```

### ❌ Wrong: Uploaded entire folders from your computer
```
circuit-os-dashboards/
└── CircuitOS-DEPLOY-PACKAGE/     ← Don't upload the parent folder!
    ├── main-dashboard.html
    └── ...
```

### ✅ Correct Structure:
```
circuit-os-dashboards/
├── main-dashboard.html           ← Root level
├── index.html                    ← Root level
├── circuit-animations.js         ← Root level
├── Dashboards/                   ← Created folder in Supabase
│   └── (5 HTML files)
└── Brand-Assets/                 ← Created folder in Supabase
    └── (SVG files)
```

## How to Fix If Wrong

### If you uploaded to wrong location:
1. In Supabase, select the wrongly placed files
2. Click "Delete"
3. Follow the upload steps again correctly

### If you uploaded parent folder:
1. Delete the entire `CircuitOS-DEPLOY-PACKAGE` folder from bucket
2. Start fresh with correct structure

## Need Help?

Tell me what you see in your bucket and I can help fix it!

Or share a screenshot of your Supabase storage bucket view.
