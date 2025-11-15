# CircuitOS Local™ - Multi-Location Deployment Guide

**Copyright © 2025 CircuitOS™. All Rights Reserved.**
**Proprietary & Confidential**

**Document Version:** 1.0.0
**Last Updated:** October 24, 2025

---

## 🎯 Purpose

This guide walks you through deploying CircuitOS Local™ to **four critical locations**:

1. **Desktop** - Active development and working copy
2. **Backup Drive** - Disaster recovery and IP timestamp proof
3. **GitHub** - Version control and team collaboration
4. **Supabase Storage** - Cloud backup and API access

**Why Multiple Locations?**
- **Redundancy:** Multiple backups protect against data loss
- **IP Protection:** Timestamped versions prove creation dates for trademark/trade secret claims
- **Collaboration:** Git enables team development and version tracking
- **Accessibility:** Cloud storage enables remote access and integration

---

## ✅ Current Status

### Completed:
✅ Desktop folder structure created
✅ 35 framework documents generated (532KB)
✅ Git repository initialized
✅ Initial commit created (v1.0.0)
✅ .gitignore and README.md configured

### Next Steps:
1. Configure backup drive deployment
2. Set up GitHub private repository
3. Configure Supabase Storage
4. Establish automated backup schedule

---

## 📍 Location 1: Desktop (Active Development)

**Current Path:** `/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package/`

**Status:** ✅ COMPLETE

**Purpose:**
- Active development and documentation updates
- Primary working copy
- Git repository source

**Maintenance:**
- Update framework documents as needed
- Commit changes to Git regularly
- Run `git status` before major changes

**Git Commands Reference:**
```bash
# Check status
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package
git status

# Add and commit changes
git add .
git commit -m "Description of changes"

# View commit history
git log --oneline

# Create new version tag
git tag -a v1.0.1 -m "Minor update description"
```

---

## 📍 Location 2: Backup Drive

**Recommended Path:** `[YOUR_BACKUP_DRIVE]/CircuitOS_Backups/CircuitOS_Local_Complete_Package/`

**Status:** ⏳ PENDING YOUR CONFIGURATION

### Setup Instructions:

#### Step 1: Identify Backup Drive
First, identify your backup drive path:

```bash
# List all mounted volumes
ls -la /Volumes/

# Common backup drive names:
# /Volumes/Backup/
# /Volumes/TimeMachine/
# /Volumes/External/
# /Volumes/[YOUR_DRIVE_NAME]/
```

#### Step 2: Create Backup Directory Structure
```bash
# Replace [BACKUP_DRIVE] with your actual drive name
BACKUP_PATH="/Volumes/[BACKUP_DRIVE]/CircuitOS_Backups"

# Create backup root directory
mkdir -p "$BACKUP_PATH"

# Create timestamped backup subdirectory
mkdir -p "$BACKUP_PATH/CircuitOS_Local_Complete_Package"
```

#### Step 3: Initial Backup
```bash
# Copy entire package to backup drive
rsync -av --progress \
  /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package/ \
  "$BACKUP_PATH/CircuitOS_Local_Complete_Package/"

# Verify backup
du -sh "$BACKUP_PATH/CircuitOS_Local_Complete_Package"
# Should show: 532K or similar
```

#### Step 4: Create Timestamped Archive (For IP Protection)
```bash
# Create dated archive for legal proof of creation
DATE=$(date +"%Y-%m-%d_%H%M")
tar -czf "$BACKUP_PATH/CircuitOS_Local_v1.0.0_${DATE}.tar.gz" \
  -C /Users/noelpena/Desktop/ \
  CircuitOS_Local_Complete_Package

# Verify archive created
ls -lh "$BACKUP_PATH"/*.tar.gz
```

### Automated Backup Script

Create a script to run daily backups:

**File:** `/Users/noelpena/Scripts/backup_circuitos_local.sh`

```bash
#!/bin/bash
# CircuitOS Local™ - Automated Backup Script
# Copyright © 2025 CircuitOS™. All Rights Reserved.

# Configuration
SOURCE_PATH="/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package"
BACKUP_DRIVE="/Volumes/[BACKUP_DRIVE]"
BACKUP_PATH="${BACKUP_DRIVE}/CircuitOS_Backups"
LOG_FILE="${BACKUP_PATH}/backup_log.txt"

# Check if backup drive is mounted
if [ ! -d "$BACKUP_DRIVE" ]; then
    echo "$(date): ERROR - Backup drive not mounted" >> "$LOG_FILE"
    exit 1
fi

# Create timestamped backup
DATE=$(date +"%Y-%m-%d_%H%M")
BACKUP_DIR="${BACKUP_PATH}/CircuitOS_Local_${DATE}"

# Sync files
rsync -av --delete \
  "$SOURCE_PATH/" \
  "${BACKUP_PATH}/CircuitOS_Local_Complete_Package/" \
  >> "$LOG_FILE" 2>&1

# Create compressed archive
tar -czf "${BACKUP_PATH}/CircuitOS_Local_v1.0.0_${DATE}.tar.gz" \
  -C /Users/noelpena/Desktop/ \
  CircuitOS_Local_Complete_Package \
  >> "$LOG_FILE" 2>&1

# Clean up old archives (keep last 30 days)
find "$BACKUP_PATH" -name "CircuitOS_Local_v*.tar.gz" -mtime +30 -delete

# Log success
echo "$(date): Backup completed successfully" >> "$LOG_FILE"
```

**Make script executable:**
```bash
chmod +x /Users/noelpena/Scripts/backup_circuitos_local.sh
```

**Schedule daily backup (macOS):**
```bash
# Create launchd plist file
# File: ~/Library/LaunchAgents/com.circuitos.backup.plist

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.circuitos.backup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/noelpena/Scripts/backup_circuitos_local.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardErrorPath</key>
    <string>/tmp/circuitos_backup_error.log</string>
    <key>StandardOutPath</key>
    <string>/tmp/circuitos_backup_output.log</string>
</dict>
</plist>

# Load the job
launchctl load ~/Library/LaunchAgents/com.circuitos.backup.plist
```

---

## 📍 Location 3: GitHub (Version Control)

**Repository Name:** `CircuitOS-Complete-System` (Recommended)
**Branch:** `local-retail-version`
**Visibility:** 🔒 **PRIVATE** (Critical for IP protection)

**Status:** ⏳ PENDING YOUR CONFIGURATION

### Setup Instructions:

#### Option A: GitHub CLI (Recommended)

**Step 1: Install GitHub CLI (if not installed)**
```bash
# macOS
brew install gh

# Verify installation
gh --version
```

**Step 2: Authenticate with GitHub**
```bash
# Login to GitHub
gh auth login

# Follow prompts:
# - Choose: GitHub.com
# - Protocol: HTTPS
# - Authenticate: Browser or Token
```

**Step 3: Create Private Repository**
```bash
# Navigate to your package
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package

# Create private repository
gh repo create CircuitOS-Complete-System \
  --private \
  --source=. \
  --remote=origin \
  --description="CircuitOS Local™ - Complete IP-protected framework package for local/retail businesses" \
  --push

# Verify repository created
gh repo view
```

**Step 4: Set Up Branch Structure**
```bash
# Rename main branch to more descriptive name
git branch -m main local-retail-version

# Push to GitHub
git push -u origin local-retail-version

# Create online-version branch for future (placeholder)
git checkout -b online-version
echo "# CircuitOS Online - Coming Soon" > ONLINE_VERSION_PLACEHOLDER.md
git add ONLINE_VERSION_PLACEHOLDER.md
git commit -m "Placeholder for online version"
git push -u origin online-version

# Switch back to local version
git checkout local-retail-version
```

#### Option B: Manual GitHub Setup

**Step 1: Create Repository on GitHub.com**
1. Go to https://github.com/new
2. Repository name: `CircuitOS-Complete-System`
3. Description: "CircuitOS Local™ - Complete IP-protected framework package"
4. Visibility: **Private** (CRITICAL!)
5. DO NOT initialize with README (we already have one)
6. Click "Create repository"

**Step 2: Add Remote and Push**
```bash
cd /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package

# Add GitHub as remote
git remote add origin https://github.com/[YOUR_USERNAME]/CircuitOS-Complete-System.git

# Push to GitHub
git branch -M local-retail-version
git push -u origin local-retail-version

# Verify push successful
git remote -v
```

### GitHub Repository Configuration

**Step 3: Configure Repository Settings**

1. **Branch Protection** (Recommended)
   - Go to: Settings → Branches → Add rule
   - Branch name pattern: `local-retail-version`
   - Enable: "Require pull request reviews before merging"
   - Enable: "Require status checks to pass before merging"

2. **Access Control**
   - Go to: Settings → Manage access
   - Add only authorized team members
   - Document all access in LEGAL_IP/Version_History_Legal.md

3. **Security**
   - Go to: Settings → Security
   - Enable: "Private vulnerability reporting"
   - Enable: "Dependency graph"

### Git Workflow Best Practices

**Daily Development:**
```bash
# Start work session
git pull origin local-retail-version

# Make changes to framework files
# ... edit documents ...

# Check what changed
git status
git diff

# Commit changes
git add .
git commit -m "Update [specific framework]: [description of changes]"

# Push to GitHub
git push origin local-retail-version
```

**Creating New Versions:**
```bash
# After significant updates
git tag -a v1.0.1 -m "Version 1.0.1 - [summary of changes]"
git push origin v1.0.1

# Update LEGAL_IP/Version_History_Legal.md with new version
```

---

## 📍 Location 4: Supabase Storage

**Bucket Name:** `circuitos-local-docs` (Recommended)
**Access:** 🔒 **PRIVATE** (Authentication required)

**Status:** ⏳ PENDING YOUR CONFIGURATION

### Why Supabase?
- **Cloud backup:** Accessible from anywhere
- **Version control:** File versioning built-in
- **API access:** Potential for future dashboard integration
- **Cost-effective:** Free tier generous for documentation storage

### Setup Instructions:

#### Step 1: Create Supabase Project

1. Go to https://supabase.com
2. Sign up or log in
3. Click "New Project"
4. Project name: `circuitos-local`
5. Database password: [Generate strong password - SAVE IT!]
6. Region: Choose closest to your location
7. Click "Create new project"

#### Step 2: Create Storage Bucket

```bash
# In Supabase Dashboard:
# 1. Go to Storage section
# 2. Click "New bucket"
# 3. Name: circuitos-local-docs
# 4. Public bucket: OFF (keep private!)
# 5. File size limit: 50 MB (more than enough)
# 6. Allowed MIME types: Leave empty (allow all)
# 7. Click "Create bucket"
```

#### Step 3: Configure Bucket Policies

```sql
-- In Supabase SQL Editor:
-- Navigate to: SQL Editor → New Query

-- Create policy for authenticated uploads
CREATE POLICY "Allow authenticated uploads"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'circuitos-local-docs');

-- Create policy for authenticated reads
CREATE POLICY "Allow authenticated reads"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'circuitos-local-docs');

-- Create policy for authenticated updates
CREATE POLICY "Allow authenticated updates"
ON storage.objects FOR UPDATE
TO authenticated
USING (bucket_id = 'circuitos-local-docs');
```

#### Step 4: Get API Credentials

```bash
# In Supabase Dashboard:
# 1. Go to Settings → API
# 2. Copy these values:

PROJECT_URL="https://[YOUR_PROJECT_ID].supabase.co"
ANON_KEY="[YOUR_ANON_KEY]"
SERVICE_ROLE_KEY="[YOUR_SERVICE_ROLE_KEY]" # Keep this secret!
```

**Save credentials securely:**
```bash
# Create .env file (DO NOT COMMIT TO GIT)
cat > /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package/.env << EOF
SUPABASE_URL="${PROJECT_URL}"
SUPABASE_ANON_KEY="${ANON_KEY}"
SUPABASE_SERVICE_KEY="${SERVICE_ROLE_KEY}"
EOF

# Verify .env is in .gitignore
grep "\.env" .gitignore
```

#### Step 5: Upload Documentation to Supabase

**Install Supabase CLI:**
```bash
# macOS
brew install supabase/tap/supabase

# Verify installation
supabase --version
```

**Upload Files:**
```bash
# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref [YOUR_PROJECT_ID]

# Upload framework files
supabase storage cp \
  /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package/ \
  supabase://circuitos-local-docs/ \
  --recursive

# Verify upload
supabase storage ls supabase://circuitos-local-docs/
```

### Automated Supabase Backup Script

**File:** `/Users/noelpena/Scripts/backup_to_supabase.sh`

```bash
#!/bin/bash
# CircuitOS Local™ - Supabase Backup Script
# Copyright © 2025 CircuitOS™. All Rights Reserved.

# Load environment variables
source /Users/noelpena/Desktop/CircuitOS_Local_Complete_Package/.env

# Configuration
SOURCE_PATH="/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package"
BUCKET_NAME="circuitos-local-docs"
DATE=$(date +"%Y-%m-%d_%H%M")
LOG_FILE="/tmp/supabase_backup_log.txt"

# Check if supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "$(date): ERROR - Supabase CLI not installed" >> "$LOG_FILE"
    exit 1
fi

# Upload files to Supabase
echo "$(date): Starting Supabase backup..." >> "$LOG_FILE"

supabase storage cp \
  "$SOURCE_PATH/" \
  "supabase://${BUCKET_NAME}/backups/${DATE}/" \
  --recursive \
  >> "$LOG_FILE" 2>&1

# Create version marker file
echo "CircuitOS Local v1.0.0 - Backup ${DATE}" > /tmp/version_marker.txt
supabase storage cp \
  /tmp/version_marker.txt \
  "supabase://${BUCKET_NAME}/backups/${DATE}/VERSION.txt" \
  >> "$LOG_FILE" 2>&1

# Log success
echo "$(date): Supabase backup completed successfully" >> "$LOG_FILE"
```

**Make script executable:**
```bash
chmod +x /Users/noelpena/Scripts/backup_to_supabase.sh
```

---

## 📅 Backup Schedule Summary

### Recommended Backup Frequency:

| Location | Frequency | Automation | Purpose |
|----------|-----------|------------|---------|
| **Desktop** | Real-time | Git commits | Active development |
| **Backup Drive** | Daily (11 PM) | Launchd script | Disaster recovery |
| **GitHub** | On commits | Git push | Version control, collaboration |
| **Supabase** | Weekly (Sundays) | Cron/Launchd | Cloud backup, API access |

### Set Up Weekly Supabase Backup:

```bash
# Create launchd plist for weekly backup
# File: ~/Library/LaunchAgents/com.circuitos.supabase.plist

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.circuitos.supabase</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/noelpena/Scripts/backup_to_supabase.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer> <!-- Sunday -->
        <key>Hour</key>
        <integer>22</integer> <!-- 10 PM -->
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>

# Load the job
launchctl load ~/Library/LaunchAgents/com.circuitos.supabase.plist
```

---

## ✅ Deployment Checklist

**Use this checklist to verify complete multi-location deployment:**

### Desktop
- [ ] Package folder exists at `/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package/`
- [ ] All 35 framework files present (verify with `find . -name "*.md" | wc -l`)
- [ ] Git repository initialized (`git status` works)
- [ ] Initial commit created (`git log` shows commit)
- [ ] .gitignore configured properly

### Backup Drive
- [ ] Backup drive identified and path confirmed
- [ ] Backup directory created on external drive
- [ ] Initial manual backup completed successfully
- [ ] Timestamped archive created (.tar.gz file)
- [ ] Automated backup script created and tested
- [ ] Launchd job scheduled for daily backups
- [ ] Backup log file accessible and monitoring

### GitHub
- [ ] GitHub account accessible
- [ ] Private repository created: `CircuitOS-Complete-System`
- [ ] Local repository connected to GitHub remote
- [ ] Initial push completed successfully
- [ ] Branch structure set up (local-retail-version)
- [ ] Repository settings configured (private, branch protection)
- [ ] Access control configured (authorized users only)
- [ ] Repository URL documented for team access

### Supabase
- [ ] Supabase project created
- [ ] Storage bucket created: `circuitos-local-docs`
- [ ] Bucket policies configured (private access only)
- [ ] API credentials saved securely (.env file)
- [ ] Supabase CLI installed and authenticated
- [ ] Initial upload to Supabase completed
- [ ] Automated backup script created and tested
- [ ] Weekly backup scheduled via launchd

### Documentation
- [ ] DEPLOYMENT_GUIDE_MULTI_LOCATION.md reviewed
- [ ] Backup credentials documented securely
- [ ] Team members notified of repository access
- [ ] LEGAL_IP/Version_History_Legal.md updated with deployment dates

---

## 🔐 Security Best Practices

### Credentials Management

**NEVER commit these to Git:**
- Supabase API keys (.env file)
- GitHub personal access tokens
- Backup drive paths with sensitive info
- Client-specific data

**DO commit:**
- Documentation and framework files
- .gitignore configuration
- README and setup guides
- Non-sensitive scripts

### Access Control

**Desktop:**
- Use FileVault encryption (macOS)
- Require password on wake
- Lock screen when away

**Backup Drive:**
- Use encrypted external drive (recommended)
- Store securely when not in use
- Test restore procedure quarterly

**GitHub:**
- Enable 2FA on account
- Use SSH keys for authentication
- Review access logs monthly
- Limit collaborators to essential team only

**Supabase:**
- Never share SERVICE_ROLE_KEY publicly
- Use ANON_KEY for client applications only
- Rotate keys if suspected compromise
- Monitor storage usage and access logs

---

## 🆘 Troubleshooting

### Issue: Backup Drive Not Mounting

**Solution:**
```bash
# Check available volumes
ls -la /Volumes/

# If drive not showing, check Disk Utility
# macOS: Applications → Utilities → Disk Utility

# Remount manually
diskutil list
diskutil mount /dev/disk[X]
```

### Issue: GitHub Push Fails (Authentication)

**Solution:**
```bash
# Update remote URL to use SSH
git remote set-url origin git@github.com:[YOUR_USERNAME]/CircuitOS-Complete-System.git

# Or use GitHub CLI
gh auth refresh

# Or create personal access token
# GitHub → Settings → Developer settings → Personal access tokens
```

### Issue: Supabase Upload Fails

**Solution:**
```bash
# Verify authentication
supabase login

# Check project link
supabase projects list
supabase link --project-ref [YOUR_PROJECT_ID]

# Test connection
supabase storage ls

# Check file size (must be < bucket limit)
du -sh [FILE_PATH]
```

### Issue: Git Repository Too Large

**Solution:**
```bash
# Check repository size
du -sh .git

# If over 1GB, use Git LFS for large files
git lfs install
git lfs track "*.pdf"
git lfs track "*.mp4"
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

---

## 📞 Next Steps

After completing multi-location deployment:

1. **Test Restore Procedure**
   - Practice restoring from backup drive
   - Verify GitHub clone works
   - Test Supabase download

2. **Document Access**
   - Update LEGAL_IP/Version_History_Legal.md with deployment dates
   - Share GitHub repository access with authorized team
   - Document Supabase credentials in secure password manager

3. **Schedule Reviews**
   - Monthly: Review backup logs
   - Quarterly: Test disaster recovery
   - Annually: Audit access controls and rotate credentials

4. **Begin Development**
   - Customize frameworks for specific clients
   - Add industry-specific variations
   - Track changes in Git with detailed commit messages

---

## 📚 Related Documentation

- [PACKAGE_MANIFEST.md](PACKAGE_MANIFEST.md) - Complete package inventory
- [LEGAL_IP/Version_History_Legal.md](LEGAL_IP/Version_History_Legal.md) - Version tracking for IP protection
- [START_HERE/IP_PROTECTION_OVERVIEW.md](START_HERE/IP_PROTECTION_OVERVIEW.md) - IP protection strategy
- [DEPLOYMENT/Quick_Deploy_Checklist.md](DEPLOYMENT/Quick_Deploy_Checklist.md) - System deployment guide

---

**🎉 Congratulations!**

Once you complete this multi-location deployment, you'll have:
- ✅ **4 secure backup locations** for redundancy
- ✅ **Timestamped archives** for IP protection
- ✅ **Version control** via Git/GitHub
- ✅ **Cloud backup** via Supabase
- ✅ **Automated backup schedule** for peace of mind

**Your CircuitOS Local™ intellectual property is now protected and accessible across multiple secure locations!**

---

**© 2025 CircuitOS™. All Rights Reserved.**
**Proprietary & Confidential**
