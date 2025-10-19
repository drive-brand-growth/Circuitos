#!/bin/bash

# Fix Content-Type for HTML files in Supabase

API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt5bWl4anV5bmZmanZucndtY3BrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTM2Njk3MiwiZXhwIjoyMDcwOTQyOTcyfQ.awZjVP0rDDIEEbj-7EkjgRyM1sJmDAIw5EaOwVGvdco"
PROJECT="kymixjuynffjvnrwmcpk"
BUCKET="circuit-os-dashboards"

echo "🔧 Fixing content-type for HTML files..."
echo ""

# Function to upload with form data (auto-detects content-type)
upload_file() {
    local file=$1
    local path=$2

    # Delete existing file
    curl -s -X DELETE "https://$PROJECT.supabase.co/storage/v1/object/$BUCKET/$path" \
        -H "Authorization: Bearer $API_KEY" \
        -H "apikey: $API_KEY" > /dev/null 2>&1

    # Upload with form data (Supabase auto-detects .html -> text/html)
    result=$(curl -s -X POST "https://$PROJECT.supabase.co/storage/v1/object/$BUCKET/$path" \
        -H "Authorization: Bearer $API_KEY" \
        -H "apikey: $API_KEY" \
        -F "file=@$file")

    if [[ $result == *"Key"* ]]; then
        echo "  ✓ $path"
    else
        echo "  ✗ $path (failed)"
    fi
}

# Upload main files
echo "Main files:"
upload_file "main-dashboard.html" "main-dashboard.html"
upload_file "index.html" "index.html"

echo ""
echo "Dashboard files:"
for file in Dashboards/*.html; do
    filename=$(basename "$file")
    upload_file "$file" "Dashboards/$filename"
done

echo ""
echo "✅ Done! Test your dashboard:"
echo "https://$PROJECT.supabase.co/storage/v1/object/public/$BUCKET/main-dashboard.html"
echo ""
echo "It should now render properly, not show code!"
