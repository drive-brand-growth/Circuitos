# CircuitOS Folder Cleanup Plan

**Current State**: 100+ files/folders at root level - needs organization!

---

## 🐳 Docker Question - ANSWERED

**Yes, Docker is being used!**

**Location**: `/agentforce_emulator/docker-compose.local.yml`

**Purpose**: **Salesforce Agentforce Emulator** (DRN work - NOT GHL/CircuitOS)

**What it does**:
- Runs Postgres database (port 5434)
- Runs Redis cache (port 6380)
- Runs OpenTelemetry collector (monitoring)
- Runs Grafana dashboard (port 5400)

**This is for**: Your DRN Salesforce consulting work (Lost Opportunity agents, etc.)

**NOT for**: GHL CircuitOS training (that's separate)

**To use it**:
```bash
cd agentforce_emulator
docker-compose -f docker-compose.local.yml up
```

---

## 📂 Proposed Clean Structure

### Current Mess (100 files at root)
```
CircuitOS_Local_Complete_Package/
├── AGENTFORCE_EXECUTIVE_REPORTING_OVERVIEW.txt
├── AI_CONTENT_HUMANIZER_COMPLETE_PACKAGE.md
├── DARK-KNIGHT-EXECUTIVE-SUMMARY.md
├── DEPLOYMENT-COMPLETE-SUMMARY.md
├── ... (96 more files at root!)
```

### Proposed Clean Structure

```
CircuitOS_Local_Complete_Package/
│
├── README.md                          # ⭐ START HERE
├── QUICK_START.md                     # Quick links to everything
│
├── 01_GHL_CircuitOS/                  # ⭐ Main GHL/CircuitOS System
│   ├── README.md
│   ├── Training/
│   │   ├── ghl-circuitos-complete-training.html
│   │   └── serve-local.sh
│   ├── SDK_Training/
│   │   ├── circuitos_ghl_sdk/
│   │   └── examples/
│   ├── GHL-Setup/
│   │   ├── AI-Employees/
│   │   └── Integration-Guides/
│   └── Deployment/
│       ├── deploy-github.sh
│       └── guides/
│
├── 02_Salesforce_DRN/                 # ⭐ Salesforce Agentforce (Separate)
│   ├── README.md
│   ├── agentforce_emulator/           # Docker stuff here
│   │   ├── docker-compose.local.yml
│   │   └── ...
│   ├── virtual-agentforce/
│   ├── Playbooks/
│   │   ├── DRN_LEAD_SCORING_AGENT_PLAYBOOK.md
│   │   ├── DRN_LOST_OPPORTUNITY_AGENT_PLAYBOOK.md
│   │   └── ...
│   └── Documentation/
│
├── 03_UMich_CDAIO/                    # ⭐ Chief Data & AI Officer Program
│   ├── README.md
│   ├── Curriculum/
│   ├── Modules/
│   └── Analysis/
│
├── 04_Skills/                         # ⭐ Claude Code Skills
│   ├── .claude/skills/                # Active skills
│   ├── Documentation/
│   └── Templates/
│
├── 05_Web_Assets/                     # ⭐ Web/UI Components
│   ├── HTML/
│   ├── CSS/
│   ├── JavaScript/
│   ├── Animations/
│   └── Brand-Assets/
│
├── 06_Documentation/                  # ⭐ Guides & References
│   ├── Setup-Guides/
│   ├── API-Documentation/
│   ├── Architecture/
│   └── Best-Practices/
│
├── 07_Archives/                       # ⭐ Old/Duplicate Files
│   ├── old-deployment-guides/
│   ├── duplicate-summaries/
│   └── deprecated/
│
└── 08_Temp/                           # ⭐ Temporary/Working Files
    └── temp_check/
```

---

## 🎯 Cleanup Actions

### Phase 1: Create Clean Structure (Safe - No Deletion)

1. **Create new organized folders**
2. **Copy files to new locations**
3. **Keep originals in place** (for safety)
4. **You verify it looks good**
5. **Then we archive originals**

### Phase 2: Archive Old Files

1. **Move duplicates to Archives**
2. **Move old deployment guides to Archives**
3. **Move temporary files to Temp**

### Phase 3: Create Index Files

1. **README.md in each folder** explaining contents
2. **QUICK_START.md at root** with links to everything
3. **Navigation guide**

---

## 🚨 Files to Keep at Root (Minimal)

Only these stay at root level:
- `README.md` (main entry point)
- `QUICK_START.md` (fast navigation)
- `.gitignore`
- `.env` (if used)
- `LICENSE`

Everything else goes into organized folders.

---

## 📋 File Categories to Organize

### GHL/CircuitOS (70% of files)
- Training HTML files
- SDK code
- GHL setup guides
- Deployment scripts
- AI employee configs

### Salesforce/DRN (15% of files)
- Agentforce emulator (Docker)
- Playbooks
- Lost opp agents
- Salesforce integration guides

### UMich CDAIO (10% of files)
- Curriculum analysis
- Module content
- Training platform

### Documentation (Multiple copies - 5%)
- Deployment guides (10+ versions!)
- Summary files (20+ duplicates!)
- Quick reference guides

---

## ⚠️ Duplicate Files Found

**Deployment guides** (at least 10 versions):
- DEPLOYMENT-COMPLETE-SUMMARY.md
- DEPLOYMENT-COMPLETE.md
- DEPLOYMENT-SUMMARY.txt
- DEPLOYMENT_GUIDE.md
- DEPLOYMENT_GUIDE_MULTI_LOCATION.md
- COMPLETE-DEPLOYMENT-SUMMARY.md
- FINAL-DEPLOYMENT-READY.md
- ... and more

**Action**: Keep latest, archive rest

**Summary files** (20+ versions):
- DAY-END-SUMMARY.md
- WRAP-UP-AND-NEXT-STEPS.md
- CAIO_TRAINING_PLATFORM_SUMMARY.md
- CAIO_TRAINING_PLATFORM_FINAL_SUMMARY.md
- ... and more

**Action**: Consolidate into one SUMMARY.md

---

## ✅ Benefits of Clean Structure

### Before (Current)
- 100 files at root
- Hard to find anything
- Duplicates everywhere
- No clear organization
- GHL mixed with Salesforce

### After (Proposed)
- 8 clear folders
- Everything categorized
- Easy navigation
- No duplicates
- Clear separation (GHL vs Salesforce)

---

## 🚀 Execute Cleanup?

**Option A: Full Cleanup** (Recommended)
- Create organized structure
- Move all files
- Archive duplicates
- Clean root to 5 files

**Option B: Minimal Cleanup**
- Just create folders
- Move obvious duplicates
- Keep most at root

**Option C: Manual Review**
- I create the plan
- You move files yourself
- I help with questions

---

**Ready to clean up? Which option do you prefer?**

I can also show you exactly what would move where before we do it.
