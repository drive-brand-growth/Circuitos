#!/bin/bash
# CircuitOS Cleanup & Organization Script
# Run these commands in Warp terminal

set -e  # Exit on error

BASE_DIR="/Users/noelpena/Desktop/CircuitOS_Local_Complete_Package"
cd "$BASE_DIR"

echo "🚀 Starting CircuitOS Cleanup & Organization..."
echo ""

# ============================================
# PHASE 1: BACKUP & SAFETY
# ============================================
echo "📦 Phase 1: Creating backup..."
BACKUP_DIR="${BASE_DIR}_BACKUP_$(date +%Y%m%d_%H%M%S)"
echo "Backup location: $BACKUP_DIR"
echo "Run this command to create backup:"
echo "cp -R \"$BASE_DIR\" \"$BACKUP_DIR\""
echo ""

# ============================================
# PHASE 2: CREATE NEW DIRECTORY STRUCTURE
# ============================================
echo "📁 Phase 2: Creating new directory structure..."
mkdir -p Projects
mkdir -p Skills
mkdir -p Tools
mkdir -p Research/MetroFlex
mkdir -p Archive/Old_Assets
echo "✅ Directory structure created"
echo ""

# ============================================
# PHASE 3: MOVE ACTIVE PROJECTS
# ============================================
echo "📦 Phase 3: Moving active projects..."
if [ -d "Active/agentforce_emulator" ]; then
    mv "Active/agentforce_emulator" "Projects/"
    echo "✅ Moved agentforce_emulator"
fi

if [ -d "Active/metroflex-ghl-website" ]; then
    mv "Active/metroflex-ghl-website" "Projects/"
    echo "✅ Moved metroflex-ghl-website"
fi

if [ -d "dmh-metroflex-booth-selector" ]; then
    mv "dmh-metroflex-booth-selector" "Projects/"
    echo "✅ Moved dmh-metroflex-booth-selector"
fi

if [ -d "local_floorplan" ]; then
    mv "local_floorplan" "Projects/"
    echo "✅ Moved local_floorplan"
fi

if [ -d "Active/virtual-agentforce" ]; then
    mv "Active/virtual-agentforce" "Projects/"
    echo "✅ Moved virtual-agentforce"
fi
echo ""

# ============================================
# PHASE 4: MOVE SKILL PACKAGES
# ============================================
echo "🎯 Phase 4: Moving skill packages..."
if [ -d "Active/drn-auto-finance-training-simulator.skill" ]; then
    mv "Active/drn-auto-finance-training-simulator.skill" "Skills/"
    echo "✅ Moved drn-auto-finance-training-simulator.skill"
fi

if [ -d "Active/drn-onboarding-assessment-agent.skill" ]; then
    mv "Active/drn-onboarding-assessment-agent.skill" "Skills/"
    echo "✅ Moved drn-onboarding-assessment-agent.skill"
fi

if [ -d "Active/drn-sales-training-simulator.skill" ]; then
    mv "Active/drn-sales-training-simulator.skill" "Skills/"
    echo "✅ Moved drn-sales-training-simulator.skill"
fi

if [ -d "Active/conversation-to-proposal-builder.skill" ]; then
    mv "Active/conversation-to-proposal-builder.skill" "Skills/"
    echo "✅ Moved conversation-to-proposal-builder.skill"
fi

if [ -d "Active/AI_Content_Humanizer_Skill_Package" ]; then
    mv "Active/AI_Content_Humanizer_Skill_Package" "Skills/"
    echo "✅ Moved AI_Content_Humanizer_Skill_Package"
fi

if [ -f "Active/AI_CONTENT_HUMANIZER_COMPLETE_PACKAGE.skill" ]; then
    mv "Active/AI_CONTENT_HUMANIZER_COMPLETE_PACKAGE.skill" "Skills/"
    echo "✅ Moved AI_CONTENT_HUMANIZER_COMPLETE_PACKAGE.skill"
fi

if [ -d "Active/presentation-builder-gemini" ]; then
    mv "Active/presentation-builder-gemini" "Skills/"
    echo "✅ Moved presentation-builder-gemini"
fi

if [ -d "Active/sales-leader-coach" ]; then
    mv "Active/sales-leader-coach" "Skills/"
    echo "✅ Moved sales-leader-coach"
fi

if [ -d "Active/sales-pipeline-analyzer" ]; then
    mv "Active/sales-pipeline-analyzer" "Skills/"
    echo "✅ Moved sales-pipeline-analyzer"
fi
echo ""

# ============================================
# PHASE 5: MOVE TOOLS
# ============================================
echo "🔧 Phase 5: Moving tools..."
if [ -d "Active/ghl-website-designer" ]; then
    mv "Active/ghl-website-designer" "Tools/"
    echo "✅ Moved ghl-website-designer"
fi

if [ -d "Active/predictive-opportunity-analyzer" ]; then
    mv "Active/predictive-opportunity-analyzer" "Tools/"
    echo "✅ Moved predictive-opportunity-analyzer"
fi
echo ""

# ============================================
# PHASE 6: MOVE RESEARCH DOCUMENTS
# ============================================
echo "📚 Phase 6: Moving research documents..."
if [ -f "BHPH_DEALERSHIP_RESEARCH_COMPLETE.md" ]; then
    mv "BHPH_DEALERSHIP_RESEARCH_COMPLETE.md" "Research/"
    echo "✅ Moved BHPH_DEALERSHIP_RESEARCH_COMPLETE.md"
fi

if [ -f "DRN_OBJECTION_PROFILES_BY_SEGMENT.md" ]; then
    mv "DRN_OBJECTION_PROFILES_BY_SEGMENT.md" "Research/"
    echo "✅ Moved DRN_OBJECTION_PROFILES_BY_SEGMENT.md"
fi

if [ -f "MetroFlex_2026_Executive_Summary.md" ]; then
    mv "MetroFlex_2026_Executive_Summary.md" "Research/MetroFlex/"
    echo "✅ Moved MetroFlex_2026_Executive_Summary.md"
fi

if [ -f "MetroFlex_2026_Roadmap_Internal.md" ]; then
    mv "MetroFlex_2026_Roadmap_Internal.md" "Research/MetroFlex/"
    echo "✅ Moved MetroFlex_2026_Roadmap_Internal.md"
fi

if [ -f "MetroFlex_2026_Roadmap_Plain_Text.txt" ]; then
    mv "MetroFlex_2026_Roadmap_Plain_Text.txt" "Research/MetroFlex/"
    echo "✅ Moved MetroFlex_2026_Roadmap_Plain_Text.txt"
fi
echo ""

# ============================================
# PHASE 7: CLEAN UP DUPLICATES
# ============================================
echo "🧹 Phase 7: Cleaning up duplicates..."
if [ -d "Active/circuit-script-runtime" ]; then
    echo "⚠️  Found duplicate circuit-script-runtime in Active/"
    echo "   This is superseded by CircuitScript_Steve_Jobs_Edition"
    echo "   Moving to Archive..."
    mv "Active/circuit-script-runtime" "Archive/Old_Deployments/"
    echo "✅ Moved circuit-script-runtime to Archive"
fi

if [ -d "Documentation/CircuitScript_World_Class_Analysis" ]; then
    echo "⚠️  Found CircuitScript_World_Class_Analysis in Documentation/"
    echo "   This is superseded by CircuitScript_Steve_Jobs_Edition"
    echo "   Moving to Archive..."
    mv "Documentation/CircuitScript_World_Class_Analysis" "Archive/Old_Deployments/"
    echo "✅ Moved CircuitScript_World_Class_Analysis to Archive"
fi

if [ -f "Active/COMPLETE_PROJECT_SUMMARY.txt" ]; then
    mv "Active/COMPLETE_PROJECT_SUMMARY.txt" "Documentation/"
    echo "✅ Moved COMPLETE_PROJECT_SUMMARY.txt"
fi

if [ -f "Active/GEMINI_CUSTOM_GPT_SETUP.txt" ]; then
    mv "Active/GEMINI_CUSTOM_GPT_SETUP.txt" "Documentation/"
    echo "✅ Moved GEMINI_CUSTOM_GPT_SETUP.txt"
fi
echo ""

# ============================================
# PHASE 8: CLEAN UP ARCHIVE
# ============================================
echo "📦 Phase 8: Cleaning up Archive..."
if [ -d "Archive/Temp" ]; then
    echo "⚠️  Found Archive/Temp with potential duplicates"
    echo "   Review and consolidate manually if needed"
    # Optionally move to Old_Deployments
    # mv Archive/Temp/* Archive/Old_Deployments/ 2>/dev/null || true
fi

# Move old HTML and scripts to Old_Assets if they exist
if [ -d "Archive/Old_HTML" ] && [ "$(ls -A Archive/Old_HTML 2>/dev/null)" ]; then
    mv Archive/Old_HTML/* Archive/Old_Assets/ 2>/dev/null || true
    rmdir Archive/Old_HTML 2>/dev/null || true
    echo "✅ Consolidated Old_HTML"
fi

if [ -d "Archive/Old_Scripts" ] && [ "$(ls -A Archive/Old_Scripts 2>/dev/null)" ]; then
    mv Archive/Old_Scripts/* Archive/Old_Assets/ 2>/dev/null || true
    rmdir Archive/Old_Scripts 2>/dev/null || true
    echo "✅ Consolidated Old_Scripts"
fi
echo ""

# ============================================
# PHASE 9: CLEAN UP EMPTY ACTIVE FOLDER
# ============================================
echo "🧹 Phase 9: Cleaning up empty Active folder..."
if [ -d "Active" ]; then
    if [ -z "$(ls -A Active 2>/dev/null)" ]; then
        rmdir Active
        echo "✅ Removed empty Active folder"
    else
        echo "⚠️  Active folder still contains:"
        ls -la Active
        echo "   Review and move remaining items manually"
    fi
fi
echo ""

# ============================================
# PHASE 10: SUMMARY
# ============================================
echo "✅ Cleanup complete!"
echo ""
echo "📊 New structure:"
echo "   Projects/     - Active development projects"
echo "   Skills/       - All skill packages"
echo "   Tools/        - Utility tools"
echo "   Research/     - Research documents"
echo "   Documentation/ - Consolidated documentation"
echo "   Archive/      - Historical files"
echo "   Assets/       - Brand assets"
echo ""
echo "⚠️  Next steps:"
echo "   1. Review the new structure"
echo "   2. Check for any broken paths"
echo "   3. Update any scripts that reference old paths"
echo "   4. Consider removing Archive/Temp if duplicates confirmed"
echo ""

