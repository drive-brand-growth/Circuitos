#!/bin/bash

# Circuit OS - Supabase Storage Deployment Script
# Project ID: kymixjuynffjvnrwmcpk

echo "🚀 Circuit OS - Supabase Deployment Script"
echo "=========================================="
echo ""

# Configuration
PROJECT_REF="kymixjuynffjvnrwmcpk"
BUCKET_NAME="circuit-os-dashboards"
PROJECT_DIR="/Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE"

echo "Project: $PROJECT_REF"
echo "Bucket: $BUCKET_NAME"
echo ""

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI not installed"
    echo ""
    echo "Installing Supabase CLI..."
    brew install supabase/tap/supabase

    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Supabase CLI"
        echo ""
        echo "Manual installation:"
        echo "  brew install supabase/tap/supabase"
        exit 1
    fi
fi

echo "✅ Supabase CLI found"
echo ""

# Login to Supabase
echo "🔐 Logging in to Supabase..."
echo "   (A browser window will open for authentication)"
supabase login

if [ $? -ne 0 ]; then
    echo "❌ Supabase login failed"
    exit 1
fi

echo "✅ Logged in successfully"
echo ""

# Link to project
echo "🔗 Linking to project..."
cd "$PROJECT_DIR"
supabase link --project-ref $PROJECT_REF

if [ $? -ne 0 ]; then
    echo "❌ Failed to link project"
    exit 1
fi

echo "✅ Project linked"
echo ""

# Create bucket (if it doesn't exist)
echo "📦 Creating storage bucket..."
supabase storage create $BUCKET_NAME --public 2>/dev/null || echo "   Bucket may already exist, continuing..."
echo ""

# Upload files
echo "📤 Uploading files to Supabase Storage..."
echo ""

# Upload main files
echo "   Uploading main files..."
supabase storage upload $BUCKET_NAME/main-dashboard.html main-dashboard.html --upsert
supabase storage upload $BUCKET_NAME/index.html index.html --upsert
supabase storage upload $BUCKET_NAME/circuit-animations.js circuit-animations.js --upsert

# Upload Dashboards
echo "   Uploading dashboards..."
for file in Dashboards/*.html; do
    filename=$(basename "$file")
    echo "      - $filename"
    supabase storage upload $BUCKET_NAME/Dashboards/$filename "$file" --upsert
done

# Upload Brand Assets
echo "   Uploading brand assets..."
for file in Brand-Assets/*.svg; do
    filename=$(basename "$file")
    echo "      - $filename"
    supabase storage upload $BUCKET_NAME/Brand-Assets/$filename "$file" --upsert
done

echo ""
echo "✅ Upload complete!"
echo ""

# Get public URLs
echo "🔗 Your Circuit OS is now live at:"
echo ""
echo "Main Dashboard:"
echo "https://$PROJECT_REF.supabase.co/storage/v1/object/public/$BUCKET_NAME/main-dashboard.html"
echo ""
echo "Individual Dashboards:"
echo "https://$PROJECT_REF.supabase.co/storage/v1/object/public/$BUCKET_NAME/Dashboards/caio-university.html"
echo "https://$PROJECT_REF.supabase.co/storage/v1/object/public/$BUCKET_NAME/Dashboards/interactive-demo.html"
echo "https://$PROJECT_REF.supabase.co/storage/v1/object/public/$BUCKET_NAME/Dashboards/sales-team-dashboard.html"
echo "https://$PROJECT_REF.supabase.co/storage/v1/object/public/$BUCKET_NAME/Dashboards/unified-demo-dashboard.html"
echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Test the URLs above in your browser"
echo "2. Share with stakeholders"
echo "3. Monitor usage in Supabase dashboard"
echo ""
