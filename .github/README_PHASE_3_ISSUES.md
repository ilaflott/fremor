# Creating Phase 3 GitHub Issues

This directory contains resources for creating individual GitHub issues for each Phase 3 deferred feature from fre.cmor.

## Files in this directory

- `PHASE_3_ISSUES.md` - Complete issue templates with all content
- `/tmp/create_phase3_issues.py` - Python script for automated issue creation

## Option 1: Using the Python Script (Recommended for bulk creation)

The Python script uses the PyGithub library to create all issues automatically.

### Prerequisites
```bash
pip install PyGithub
export GITHUB_TOKEN="your_personal_access_token"
```

### Dry run (preview what will be created)
```bash
python /tmp/create_phase3_issues.py
```

### Actually create the issues
```bash
python /tmp/create_phase3_issues.py --create
```

## Option 2: Manual Creation via GitHub Web UI

1. Go to https://github.com/ilaflott/fremorizer/issues/new
2. Open `PHASE_3_ISSUES.md` in this directory
3. For each issue section:
   - Copy the title
   - Copy the body content
   - Add the labels specified
   - Click "Submit new issue"

## Option 3: Using GitHub CLI (gh)

If you have `gh` CLI installed and authenticated, you can create issues one by one:

```bash
gh issue create \
  --repo ilaflott/fremorizer \
  --title "PR #832: Harden branded-variable disambiguations" \
  --body-file - \
  --label "enhancement,phase-3" <<'EOF'
[paste issue body here]
EOF
```

## Issues to Create

The following 8 issues should be created:

1. **PR #832**: Harden branded-variable disambiguations
2. **PR #833**: Improved omission tracking
3. **PR #834**: New `fremor init` command for config fetching
4. **PR #836**: Informative error on mip_era/table format mismatch
5. **PR #837**: Accept CF calendar aliases (noleap/365_day, etc.)
6. **PR #838**: CMIP7 flavored tests
7. **PR #846**: Variable list semantics (map modeler vars to MIP table names)
8. **PR #817**: Update cmor to 3.14.2

## After Creating Issues

Once all issues are created:

1. Update `PHASE_3_DEFERRED_FEATURES.md` to link to the newly created issues
2. Add a comment on tracking issue #27 with links to all individual issues
3. Consider creating a GitHub project board to track Phase 3 implementation
4. Mark issue #27 as complete or update its description to reference the individual issues

## Labels Used

Make sure these labels exist in the repository:
- `enhancement` - Feature enhancements
- `phase-3` - Phase 3 deferred features
- `new-feature` - New functionality (PR #834)
- `error-handling` - Error handling improvements (PR #836)
- `compatibility` - Compatibility enhancements (PR #837)
- `testing` - Testing-related (PR #838)
- `cmip7` - CMIP7 specific (PR #838)
- `high-priority` - High priority items (PR #838)
- `variable-mapping` - Variable mapping features (PR #846)
- `dependencies` - Dependency updates (PR #817)
