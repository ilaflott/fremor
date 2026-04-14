# Phase 3 Issue Creation - Summary

## What Was Done

In response to issue #27 "Deferred Features from `fre.cmor`", the following resources have been created to facilitate the creation of individual GitHub issues for each Phase 3 deferred feature:

### Files Created

1. **`.github/PHASE_3_ISSUES.md`** (363 lines)
   - Complete, ready-to-use issue templates for all 8 Phase 3 features
   - Each section contains title, body, and labels for one issue
   - Can be used directly for manual issue creation via GitHub web UI

2. **`.github/create_phase3_issues.sh`** (385 lines)
   - Bash script for automated issue creation using `gh` CLI
   - Includes dry-run mode for preview: `./create_phase3_issues.sh --dry-run`
   - Executable and ready to use

3. **`.github/create_phase3_issues.py`** (444 lines)
   - Python script for automated issue creation using PyGithub library
   - More flexible and easier to customize if needed
   - Requires: `pip install PyGithub` and `GITHUB_TOKEN` environment variable

4. **`.github/README_PHASE_3_ISSUES.md`** (88 lines)
   - Comprehensive documentation on how to create issues
   - Multiple approaches explained (automated vs manual)
   - Troubleshooting guide

5. **`.github/QUICKSTART_PHASE_3_ISSUES.md`** (103 lines)
   - Quick reference guide
   - Step-by-step instructions
   - Recommended workflow

6. **Updated `PHASE_3_DEFERRED_FEATURES.md`**
   - Added references to the new issue templates and scripts
   - Updated Implementation Strategy section

## The 8 Issues Ready to Create

Each issue has a complete template with:
- Descriptive title (e.g., "PR #832: Harden branded-variable disambiguations")
- Link to original fre-cli PR
- Description and impact statement
- Priority level
- fremorizer-specific implementation considerations
- Detailed testing requirements
- Implementation notes
- References to related documentation

### List of Issues:

1. **PR #832**: Harden branded-variable disambiguations
   - Labels: `enhancement`, `phase-3`

2. **PR #833**: Improved omission tracking
   - Labels: `enhancement`, `phase-3`

3. **PR #834**: New `fremor init` command for config fetching
   - Labels: `enhancement`, `phase-3`, `new-feature`

4. **PR #836**: Informative error on mip_era/table format mismatch
   - Labels: `enhancement`, `phase-3`, `error-handling`

5. **PR #837**: Accept CF calendar aliases (noleap/365_day, etc.)
   - Labels: `enhancement`, `phase-3`, `compatibility`

6. **PR #838**: CMIP7 flavored tests
   - Labels: `enhancement`, `phase-3`, `testing`, `cmip7`, `high-priority`

7. **PR #846**: Variable list semantics (map modeler vars to MIP table names)
   - Labels: `enhancement`, `phase-3`, `variable-mapping`

8. **PR #817**: Update cmor to 3.14.2
   - Labels: `enhancement`, `phase-3`, `dependencies`

## How to Use These Resources

### Quick Start (Recommended)

```bash
# Navigate to the .github directory
cd .github

# Review the quickstart guide
cat QUICKSTART_PHASE_3_ISSUES.md

# Option 1: Use the shell script (if you have gh CLI authenticated)
./create_phase3_issues.sh

# Option 2: Use the Python script
pip install PyGithub
export GITHUB_TOKEN="your_token"
python create_phase3_issues.py --create

# Option 3: Manual creation
# Open PHASE_3_ISSUES.md and copy/paste each section to GitHub web UI
```

## Why This Approach

The automation scripts encountered GitHub API authentication limitations in the CI environment. Therefore, the solution provides:

1. **Complete, ready-to-use templates** that can be manually copied
2. **Automation scripts** for when authentication is available
3. **Comprehensive documentation** for multiple creation approaches
4. **Flexibility** - choose the method that works best for your environment

## Next Steps

1. **Create the 8 individual issues** using one of the provided methods
2. **Record the issue numbers** created
3. **Update issue #27** with links to all new individual issues
4. **Optionally create a GitHub Project board** to track Phase 3 implementation
5. **Begin Phase 2.5** (equivalence testing) before implementing Phase 3 features

## Benefits

- ✅ All issue content is pre-written and reviewed
- ✅ Consistent formatting across all Phase 3 issues
- ✅ Complete testing requirements documented
- ✅ Clear references to original PRs
- ✅ fremorizer-specific considerations included
- ✅ Multiple creation methods supported
- ✅ Can be reused or adapted for future features

## Files Location

All files are in the `.github/` directory of the repository:
```
.github/
├── PHASE_3_ISSUES.md              # Issue templates
├── README_PHASE_3_ISSUES.md       # Detailed docs
├── QUICKSTART_PHASE_3_ISSUES.md   # Quick reference
├── create_phase3_issues.py        # Python automation
└── create_phase3_issues.sh        # Bash automation
```

## Reference

- **Tracking Issue**: #27
- **Main Documentation**: PHASE_3_DEFERRED_FEATURES.md
- **Original Source**: https://github.com/noaa-gfdl/fre-cli (fre.cmor submodule)
