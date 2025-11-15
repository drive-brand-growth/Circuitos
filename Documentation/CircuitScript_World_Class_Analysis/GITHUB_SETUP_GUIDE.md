# Circuit Script™ - GitHub Setup Guide
## Create New Repository for Clean Start

**Goal:** Push Circuit Script to a new GitHub repository, separate from the CircuitOS mess

---

## Step 1: Initialize Git (5 minutes)

```bash
cd /Users/noelpena/Desktop/CircuitScript_Steve_Jobs_Edition

# Initialize new Git repo
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Circuit Script Steve Jobs Edition

- Complete architecture documentation
- 10-week build plan
- Trademark/IP strategy
- Directory structure for Flask implementation
- Based on 34,357 lines of CircuitOS agent logic
- Steve Jobs simplicity principles applied

© 2025 CircuitOS™ - Circuit Script™"
```

---

## Step 2: Create GitHub Repository (3 minutes)

### Option A: Using GitHub CLI (fastest)

```bash
# Create private repo
gh repo create circuit-script --private --description "Salesforce Apex for GoHighLevel - unified execution platform for AI agents" --source=.

# Push to GitHub
git push -u origin main
```

### Option B: Using GitHub Web Interface

1. Go to https://github.com/new
2. **Repository name:** `circuit-script`
3. **Description:** "Salesforce Apex for GoHighLevel - unified execution platform for AI agents"
4. **Visibility:** Private (recommended) or Public
5. **Do NOT initialize** with README (you already have one)
6. Click "Create repository"

Then push:

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/circuit-script.git

# Push
git branch -M main
git push -u origin main
```

---

## Step 3: Configure Repository Settings (2 minutes)

### A. Branch Protection (Prevent Accidental Deletes)

1. Go to repo → Settings → Branches
2. Add rule for `main` branch:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass (will add tests in Week 6-7)
   - ✅ Include administrators (protects even you)

### B. Secrets (API Keys)

1. Go to repo → Settings → Secrets and variables → Actions
2. Add these secrets (will need for deployment):
   - `OPENAI_API_KEY` (your OpenAI key)
   - `SUPABASE_URL` (from Supabase dashboard)
   - `SUPABASE_KEY` (from Supabase dashboard)
   - `GHL_API_KEY` (from GoHighLevel)
   - `HEROKU_API_KEY` (from Heroku dashboard)

### C. Topics/Tags

1. Go to repo → About (top right)
2. Add topics:
   - `salesforce-apex`
   - `gohighlevel`
   - `ai-agents`
   - `python-flask`
   - `circuit-script`
   - `virtual-lpr`

---

## Step 4: Add .gitignore (1 minute)

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing
.coverage
htmlcov/
.pytest_cache/

# Supabase local
supabase/.branches/
supabase/.temp/

# Secrets (NEVER commit)
config/secrets.yml
keys/
*.pem
*.key

# Heroku
.heroku/

# Temp files
tmp/
temp/
*.tmp
EOF

git add .gitignore
git commit -m "Add .gitignore for Python/Flask project"
git push
```

---

## Step 5: README Badges (Optional, 2 minutes)

Add to top of README.md:

```markdown
# Circuit Script™ - Steve Jobs Edition

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-Proprietary-red)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Build](https://img.shields.io/badge/Build-Week%201%20of%2010-orange)
```

---

## Step 6: License File (1 minute)

```bash
cat > LICENSE << 'EOF'
# Circuit Script™ - Proprietary License

Copyright © 2025 CircuitOS™. All Rights Reserved.

This software and associated documentation files (the "Software") are proprietary
and confidential. Unauthorized copying, distribution, modification, or use of this
Software, via any medium, is strictly prohibited without the express written
permission of CircuitOS™.

## Permitted Use

This Software is licensed, not sold. You may use this Software only as expressly
permitted in your licensing agreement with CircuitOS™.

## Restrictions

- You may NOT copy, modify, distribute, or create derivative works
- You may NOT reverse-engineer, decompile, or disassemble the Software
- You may NOT remove copyright or proprietary notices
- You may NOT sublicense or transfer your rights to the Software

## Trademarks

Circuit Script™, CircuitOS™, Virtual LPR™, and 17-Level Judgment Protocol™ are
trademarks of CircuitOS™.

## Contact

For licensing inquiries: [your-email@domain.com]

EOF

git add LICENSE
git commit -m "Add proprietary license"
git push
```

---

## Step 7: Project Structure Documentation (2 minutes)

```bash
cat > PROJECT_STRUCTURE.md << 'EOF'
# Circuit Script™ - Project Structure

## Directory Layout

```
CircuitScript_Steve_Jobs_Edition/
├── README.md                           # Start here
├── LICENSE                             # Proprietary license
├── .gitignore                          # Git exclusions
├── requirements.txt                    # Python dependencies
├── Procfile                            # Heroku deployment
├── runtime.txt                         # Python version for Heroku
│
├── TRADEMARK_AND_IP_STRATEGY.md        # IP protection plan
├── GITHUB_SETUP_GUIDE.md               # This file
├── SUPABASE_SETUP_GUIDE.md             # Database setup
│
├── docs/                               # Documentation
│   ├── START_HERE_STEVE_JOBS_REVIEW.md      # 5-min decision doc
│   ├── CIRCUIT_SCRIPT_FINAL_DECISION.md     # Complete review
│   ├── WORLD_CLASS_GAP_ANALYSIS.md          # Gap analysis
│   ├── CORRECTED_GAP_ANALYSIS.md            # Stack analysis
│   ├── BEFORE_VS_AFTER.md                   # Code comparisons
│   ├── ARCHITECTURE_DIAGRAMS.md             # Mermaid diagrams
│   └── 10_WEEK_BUILD_PLAN.md                # Build timeline
│
├── circuit_script/                     # Main application
│   ├── __init__.py
│   ├── app.py                          # Flask app entry point
│   │
│   ├── runtime/                        # Core runtime
│   │   ├── __init__.py
│   │   ├── governor.py                 # Resource limits
│   │   ├── logger.py                   # Centralized logging
│   │   ├── security.py                 # 17-level Tondi Enhanced
│   │   └── trigger_registry.py         # Webhook → trigger mapping
│   │
│   ├── core/                           # Framework classes
│   │   ├── __init__.py
│   │   ├── CircuitDB.py                # GHL/SF API wrapper
│   │   ├── CircuitTrigger.py           # Base trigger class
│   │   ├── CircuitLog.py               # Logging interface
│   │   └── OpenAI.py                   # GPT-4o-mini wrapper
│   │
│   ├── agents/                         # Your 34,357 lines
│   │   ├── __init__.py
│   │   ├── VirtualLPR.py               # Lead scoring (1,505 lines)
│   │   ├── ReputationGuardian.py       # Reviews (1,038 lines)
│   │   ├── OmnichannelOrchestrator.py  # Sequences (1,061 lines)
│   │   └── MLFeedbackLoop.py           # Self-improving (~700 lines)
│   │
│   └── triggers/                       # Apex-style triggers
│       ├── __init__.py
│       ├── ContactTrigger.py           # Contact events
│       ├── OpportunityTrigger.py       # Opportunity events
│       ├── ReviewTrigger.py            # Review events
│       └── CampaignTrigger.py          # Campaign events
│
├── tests/                              # Test suite (Week 6-7)
│   ├── __init__.py
│   ├── conftest.py                     # Pytest config
│   ├── test_governor.py
│   ├── test_security.py
│   ├── test_virtual_lpr.py
│   └── test_triggers.py
│
├── deployment/                         # Deployment configs
│   ├── heroku/
│   │   ├── Procfile
│   │   ├── runtime.txt
│   │   └── requirements.txt
│   │
│   └── supabase/
│       ├── schema.sql                  # Database schema
│       └── seed.sql                    # Initial data
│
└── examples/                           # Usage examples
    ├── ContactTrigger_example.py
    ├── ReviewTrigger_example.py
    └── webhook_setup_guide.md
```

## File Purposes

### Root Files
- `README.md` - Project overview, quick start
- `LICENSE` - Proprietary license
- `.gitignore` - Git exclusions
- `requirements.txt` - Python dependencies
- `Procfile` - Heroku deployment command
- `runtime.txt` - Python 3.11 specification

### Documentation (`docs/`)
- All strategic/architectural documentation
- Read `START_HERE_STEVE_JOBS_REVIEW.md` first

### Application (`circuit_script/`)
- `runtime/` - Core execution engine
- `core/` - Framework base classes
- `agents/` - Your agent logic (migrated from .claude/skills)
- `triggers/` - Apex-style event handlers

### Tests (`tests/`)
- 75% coverage required (Week 6-7)
- Pytest framework
- Mocked APIs for fast testing

### Deployment (`deployment/`)
- Heroku configuration
- Supabase database schemas

### Examples (`examples/`)
- Usage documentation
- Trigger examples
- Webhook configuration guides

EOF

git add PROJECT_STRUCTURE.md
git commit -m "Add project structure documentation"
git push
```

---

## Step 8: Add GitHub Actions (Week 7 - Testing Pipeline)

Will add in Week 7, but here's the structure:

```bash
mkdir -p .github/workflows

cat > .github/workflows/test.yml << 'EOF'
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest tests/ --cov=circuit_script --cov-report=term-missing --cov-fail-under=75

    - name: Upload coverage
      uses: codecov/codecov-action@v2
EOF

# Don't commit yet (Week 7)
```

---

## Repository URLs (After Creation)

**GitHub:** `https://github.com/YOUR_USERNAME/circuit-script`
**Clone URL:** `git@github.com:YOUR_USERNAME/circuit-script.git`
**Issues:** `https://github.com/YOUR_USERNAME/circuit-script/issues`
**Wiki:** `https://github.com/YOUR_USERNAME/circuit-script/wiki`

---

## Next Steps

1. ✅ Repository created
2. ✅ Initial commit pushed
3. ✅ Branch protection enabled
4. ✅ Secrets configured
5. → **Next:** [SUPABASE_SETUP_GUIDE.md](./SUPABASE_SETUP_GUIDE.md) (create database space)
6. → **Then:** Start Week 1 (build `governor.py`)

---

**© 2025 CircuitOS™ - GitHub Setup Complete**
