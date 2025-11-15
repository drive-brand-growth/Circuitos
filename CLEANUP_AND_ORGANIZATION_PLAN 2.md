# CircuitOS Cleanup & Organization Plan

## Current Issues Identified

### 1. Duplicate Content
- **CircuitScript**: Exists in 3 places
  - `Active/circuit-script-runtime/` (incomplete)
  - `Documentation/CircuitScript_World_Class_Analysis/` (complete docs)
  - `/Users/noelpena/Desktop/CircuitScript_Steve_Jobs_Edition/` (clean repo - KEEP THIS)
  
- **Temp files**: Duplicated in `Archive/Temp/` and `Archive/Old_Deployments/`

### 2. Loose Files at Root
- `BHPH_DEALERSHIP_RESEARCH_COMPLETE.md`
- `DRN_OBJECTION_PROFILES_BY_SEGMENT.md`
- `MetroFlex_2026_Executive_Summary.md`
- `MetroFlex_2026_Roadmap_Internal.md`
- `MetroFlex_2026_Roadmap_Plain_Text.txt`

### 3. Organization Needed
- Skill packages scattered in `Active/`
- Documentation spread across `Documentation/` and project folders
- Archive needs consolidation

## Proposed Structure

```
CircuitOS_Local_Complete_Package/
├── README.md                          # Main overview
├── .gitignore                         # If using git
│
├── Projects/                          # Active development projects
│   ├── agentforce_emulator/
│   ├── metroflex-ghl-website/
│   ├── dmh-metroflex-booth-selector/
│   ├── virtual-agentforce/
│   └── local_floorplan/
│
├── Skills/                            # All skill packages
│   ├── drn-auto-finance-training-simulator.skill/
│   ├── drn-onboarding-assessment-agent.skill/
│   ├── drn-sales-training-simulator.skill/
│   ├── conversation-to-proposal-builder.skill/
│   ├── AI_Content_Humanizer_Skill_Package/
│   ├── presentation-builder-gemini/
│   ├── sales-leader-coach/
│   └── sales-pipeline-analyzer/
│
├── Tools/                             # Utility tools
│   ├── ghl-website-designer/
│   └── predictive-opportunity-analyzer/
│
├── Research/                          # Research documents
│   ├── BHPH_DEALERSHIP_RESEARCH_COMPLETE.md
│   ├── DRN_OBJECTION_PROFILES_BY_SEGMENT.md
│   └── MetroFlex/
│       ├── MetroFlex_2026_Executive_Summary.md
│       ├── MetroFlex_2026_Roadmap_Internal.md
│       └── MetroFlex_2026_Roadmap_Plain_Text.txt
│
├── Documentation/                     # Consolidated docs
│   ├── Business/
│   ├── Salesforce/
│   ├── UMich_CDAIO/
│   └── [other organized docs]
│
├── Archive/                           # Cleaned archive
│   ├── Old_Deployments/               # Historical deployments
│   └── Old_Assets/                    # Old HTML, scripts, etc.
│
└── Assets/                            # Brand assets (keep as is)
    ├── Circuit OS logo.pdf
    └── circuit-icons.svg
```

## Cleanup Steps

### Phase 1: Backup & Safety
1. Create backup of entire directory
2. Verify CircuitScript_Steve_Jobs_Edition is separate (don't touch it)

### Phase 2: Remove Duplicates
1. Remove `Active/circuit-script-runtime/` (duplicate, incomplete)
2. Move `Documentation/CircuitScript_World_Class_Analysis/` to Archive (superseded by CircuitScript_Steve_Jobs_Edition)
3. Clean up `Archive/Temp/` duplicates

### Phase 3: Organize Active Projects
1. Move projects to `Projects/`
2. Move skills to `Skills/`
3. Move tools to `Tools/`
4. Move research docs to `Research/`

### Phase 4: Clean Archive
1. Consolidate `Archive/Temp/` into `Archive/Old_Deployments/`
2. Remove duplicate files
3. Organize by date/project

### Phase 5: Final Organization
1. Update README.md with new structure
2. Create index files for major sections
3. Verify all paths still work

## Files to Keep Separate
- `/Users/noelpena/Desktop/CircuitScript_Steve_Jobs_Edition/` - DO NOT TOUCH (clean repo)

