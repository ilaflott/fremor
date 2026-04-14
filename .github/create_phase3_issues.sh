#!/bin/bash
# Script to create all Phase 3 GitHub issues
# Usage: ./create_phase3_issues.sh [--dry-run]

set -e

REPO="ilaflott/fremorizer"
DRY_RUN=false

if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "=== DRY RUN MODE ==="
    echo ""
fi

# Issue 1: PR #832
echo "Creating issue 1/8: PR #832: Harden branded-variable disambiguations"
ISSUE_1_TITLE="PR #832: Harden branded-variable disambiguations"
ISSUE_1_BODY="**Source**: https://github.com/noaa-gfdl/fre-cli/pull/832

**Description**:
Improve handling of branded variable name disambiguation (e.g., when multiple variables map to same target)

**Impact**:
More robust variable handling in edge cases

**Priority**: Medium

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Adapt code to fremorizer's independent package structure
- Ensure changes work with fremorizer's variable mapping logic

**Testing requirements**:
- All existing tests must continue to pass
- Add new tests for edge cases with multiple variables mapping to the same target
- Phase 2.5 equivalence tests should still pass after implementation
- Test with various branded variable scenarios

**Implementation notes**:
- This is a Phase 3 deferred feature from fre.cmor
- Should be implemented after Phase 2.5 (equivalence testing) is complete
- Part of tracking issue #27

**References**:
- Original fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- Phase 3 tracking document: PHASE_3_DEFERRED_FEATURES.md
- Phase 3 tracking issue: #27"

if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would create issue with labels: enhancement,phase-3"
else
    gh issue create --repo "$REPO" --title "$ISSUE_1_TITLE" --body "$ISSUE_1_BODY" --label "enhancement,phase-3"
fi
echo ""

# Issue 2: PR #833
echo "Creating issue 2/8: PR #833: Improved omission tracking"
ISSUE_2_TITLE="PR #833: Improved omission tracking"
ISSUE_2_BODY="**Source**: https://github.com/noaa-gfdl/fre-cli/pull/833

**Description**:
Better tracking and reporting of variables that are omitted during CMORization

**Impact**:
Improved user feedback and debugging capabilities

**Priority**: Medium

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Adapt code to fremorizer's independent package structure
- Ensure omission tracking integrates with fremorizer's logging system
- Consider adding summary reporting at the end of CMORization runs

**Testing requirements**:
- All existing tests must continue to pass
- Add new tests that verify omission tracking works correctly
- Test with scenarios where variables are intentionally omitted
- Verify logging output includes omission information
- Phase 2.5 equivalence tests should still pass after implementation

**Implementation notes**:
- This is a Phase 3 deferred feature from fre.cmor
- Should be implemented after Phase 2.5 (equivalence testing) is complete
- Part of tracking issue #27

**References**:
- Original fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- Phase 3 tracking document: PHASE_3_DEFERRED_FEATURES.md
- Phase 3 tracking issue: #27"

if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would create issue with labels: enhancement,phase-3"
else
    gh issue create --repo "$REPO" --title "$ISSUE_2_TITLE" --body "$ISSUE_2_BODY" --label "enhancement,phase-3"
fi
echo ""

# Issue 3: PR #834
echo "Creating issue 3/8: PR #834: New \`fremor init\` command for config fetching"
ISSUE_3_TITLE="PR #834: New \`fremor init\` command for config fetching"
ISSUE_3_BODY="**Source**: https://github.com/noaa-gfdl/fre-cli/pull/834

**Description**:
Add new CLI subcommand to fetch/initialize CMOR configuration files

**Impact**:
Improved user experience for initial setup

**Priority**: Medium - new feature, not a fix

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Adapt code to fremorizer's independent package structure
- Design the CLI interface as \`fremor init\` (not \`fre cmor init\`)
- Consider where config files should be fetched from (CMOR tables repository, etc.)
- Document the init workflow in user documentation

**Testing requirements**:
- All existing tests must continue to pass
- Add new tests for \`fremor init\` command
- Test fetching configs from various sources
- Verify config files are placed in correct locations
- Test error handling for network failures, missing configs, etc.
- Phase 2.5 equivalence tests should still pass after implementation

**Implementation notes**:
- This is a Phase 3 deferred feature from fre.cmor
- Should be implemented after Phase 2.5 (equivalence testing) is complete
- Part of tracking issue #27
- This is a new feature, not a bug fix

**References**:
- Original fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- Phase 3 tracking document: PHASE_3_DEFERRED_FEATURES.md
- Phase 3 tracking issue: #27"

if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would create issue with labels: enhancement,phase-3,new-feature"
else
    gh issue create --repo "$REPO" --title "$ISSUE_3_TITLE" --body "$ISSUE_3_BODY" --label "enhancement,phase-3,new-feature"
fi
echo ""

# Issue 4: PR #836
echo "Creating issue 4/8: PR #836: Informative error on mip_era/table format mismatch"
ISSUE_4_TITLE="PR #836: Informative error on mip_era/table format mismatch"
ISSUE_4_BODY="**Source**: https://github.com/noaa-gfdl/fre-cli/pull/836

**Description**:
Provide clear error messages when MIP era and table format don't match

**Impact**:
Better user experience and faster debugging

**Priority**: Medium

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Adapt code to fremorizer's independent package structure
- Ensure error messages are clear and actionable
- Consider providing suggestions for resolving the mismatch

**Testing requirements**:
- All existing tests must continue to pass
- Add new tests that verify correct error messages for mismatches
- Test various combinations of MIP eras and table formats
- Verify error messages are helpful and informative
- Phase 2.5 equivalence tests should still pass after implementation

**Implementation notes**:
- This is a Phase 3 deferred feature from fre.cmor
- Should be implemented after Phase 2.5 (equivalence testing) is complete
- Part of tracking issue #27

**References**:
- Original fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- Phase 3 tracking document: PHASE_3_DEFERRED_FEATURES.md
- Phase 3 tracking issue: #27"

if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would create issue with labels: enhancement,phase-3,error-handling"
else
    gh issue create --repo "$REPO" --title "$ISSUE_4_TITLE" --body "$ISSUE_4_BODY" --label "enhancement,phase-3,error-handling"
fi
echo ""

# Issue 5: PR #837
echo "Creating issue 5/8: PR #837: Accept CF calendar aliases (noleap/365_day, etc.)"
ISSUE_5_TITLE="PR #837: Accept CF calendar aliases (noleap/365_day, etc.)"
ISSUE_5_BODY="**Source**: https://github.com/noaa-gfdl/fre-cli/pull/837

**Description**:
Support CF convention calendar aliases (e.g., \"noleap\" as alias for \"365_day\")

**Impact**:
Improved compatibility with various input data conventions

**Priority**: Medium

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Adapt code to fremorizer's independent package structure
- Ensure all CF standard calendar aliases are supported
- Consider normalization of calendar names internally

**CF calendar aliases to support**:
- \`noleap\` ↔ \`365_day\`
- \`all_leap\` ↔ \`366_day\`
- \`360_day\` (standard)
- \`julian\` (standard)
- \`gregorian\` ↔ \`proleptic_gregorian\` ↔ \`standard\`

**Testing requirements**:
- All existing tests must continue to pass
- Add new tests for each calendar alias
- Test conversion between aliases
- Verify CMOR output uses correct calendar format
- Phase 2.5 equivalence tests should still pass after implementation

**Implementation notes**:
- This is a Phase 3 deferred feature from fre.cmor
- Should be implemented after Phase 2.5 (equivalence testing) is complete
- Part of tracking issue #27

**References**:
- Original fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- CF Conventions: http://cfconventions.org/Data/cf-conventions/cf-conventions-1.10/cf-conventions.html#calendar
- Phase 3 tracking document: PHASE_3_DEFERRED_FEATURES.md
- Phase 3 tracking issue: #27"

if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would create issue with labels: enhancement,phase-3,compatibility"
else
    gh issue create --repo "$REPO" --title "$ISSUE_5_TITLE" --body "$ISSUE_5_BODY" --label "enhancement,phase-3,compatibility"
fi
echo ""

# Issue 6: PR #838
echo "Creating issue 6/8: PR #838: CMIP7 flavored tests"
ISSUE_6_TITLE="PR #838: CMIP7 flavored tests"
ISSUE_6_BODY="**Source**: https://github.com/noaa-gfdl/fre-cli/pull/838

**Description**:
Add test cases specifically for CMIP7 conventions and requirements

**Impact**:
Ensure CMIP7 compatibility and catch CMIP7-specific issues

**Priority**: High - CMIP7 support is important for future-proofing

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Adapt code to fremorizer's independent package structure
- Ensure tests cover CMIP7-specific requirements
- Consider setting up separate test fixtures for CMIP7 data
- Document CMIP7-specific behavior

**Testing requirements**:
- Add comprehensive CMIP7 test cases
- Test CMIP7 table formats
- Test CMIP7 metadata requirements
- Test CMIP7 file naming conventions
- Verify CMIP7 output complies with CMIP7 standards
- All existing CMIP6 tests must continue to pass
- Phase 2.5 equivalence tests should still pass after implementation

**Implementation notes**:
- This is a Phase 3 deferred feature from fre.cmor
- Should be implemented after Phase 2.5 (equivalence testing) is complete
- Part of tracking issue #27
- High priority for future-proofing

**References**:
- Original fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- CMIP7 specifications: https://wcrp-cmip.org/
- Phase 3 tracking document: PHASE_3_DEFERRED_FEATURES.md
- Phase 3 tracking issue: #27"

if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would create issue with labels: enhancement,phase-3,testing,cmip7,high-priority"
else
    gh issue create --repo "$REPO" --title "$ISSUE_6_TITLE" --body "$ISSUE_6_BODY" --label "enhancement,phase-3,testing,cmip7,high-priority"
fi
echo ""

# Issue 7: PR #846
echo "Creating issue 7/8: PR #846: Variable list semantics (map modeler vars to MIP table names)"
ISSUE_7_TITLE="PR #846: Variable list semantics (map modeler vars to MIP table names)"
ISSUE_7_BODY="**Source**: https://github.com/noaa-gfdl/fre-cli/pull/846

**Description**:
Improve variable list handling to better map model variable names to MIP table variable names

**Impact**:
More flexible and intuitive variable mapping

**Priority**: Medium

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Adapt code to fremorizer's independent package structure
- Ensure variable mapping is intuitive and well-documented
- Consider backward compatibility with existing variable lists
- Update documentation with examples of new variable list semantics

**Testing requirements**:
- All existing tests must continue to pass
- Add new tests for improved variable list semantics
- Test mapping between modeler variable names and MIP table names
- Test edge cases and ambiguous mappings
- Verify backward compatibility with existing variable lists
- Phase 2.5 equivalence tests should still pass after implementation

**Implementation notes**:
- This is a Phase 3 deferred feature from fre.cmor
- Should be implemented after Phase 2.5 (equivalence testing) is complete
- Part of tracking issue #27

**References**:
- Original fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- Phase 3 tracking document: PHASE_3_DEFERRED_FEATURES.md
- Phase 3 tracking issue: #27"

if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would create issue with labels: enhancement,phase-3,variable-mapping"
else
    gh issue create --repo "$REPO" --title "$ISSUE_7_TITLE" --body "$ISSUE_7_BODY" --label "enhancement,phase-3,variable-mapping"
fi
echo ""

# Issue 8: PR #817
echo "Creating issue 8/8: PR #817: Update cmor to 3.14.2"
ISSUE_8_TITLE="PR #817: Update cmor to 3.14.2"
ISSUE_8_BODY="**Source**: https://github.com/noaa-gfdl/fre-cli/pull/817

**Description**:
Update the CMOR library dependency from current version to 3.14.2

**Impact**:
Access to latest CMOR features and bug fixes

**Priority**: Medium - should verify compatibility before upgrading

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Check CMOR 3.14.2 changelog for breaking changes
- Update conda environment.yaml with new version constraint
- Test thoroughly for any compatibility issues
- Update documentation if API changes require it

**Testing requirements**:
- All existing tests must continue to pass with CMOR 3.14.2
- Test for any new warnings or deprecations
- Verify output files are still valid
- Test with various MIP tables (CMIP6, CMIP7)
- Benchmark performance if significant changes in CMOR
- Phase 2.5 equivalence tests should still pass after implementation

**Implementation notes**:
- This is a Phase 3 deferred feature from fre.cmor
- Should be implemented after Phase 2.5 (equivalence testing) is complete
- Part of tracking issue #27
- Check conda-forge availability of CMOR 3.14.2

**References**:
- Original fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- CMOR GitHub: https://github.com/PCMDI/cmor
- Phase 3 tracking document: PHASE_3_DEFERRED_FEATURES.md
- Phase 3 tracking issue: #27"

if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would create issue with labels: enhancement,phase-3,dependencies"
else
    gh issue create --repo "$REPO" --title "$ISSUE_8_TITLE" --body "$ISSUE_8_BODY" --label "enhancement,phase-3,dependencies"
fi
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "=== DRY RUN COMPLETE ==="
    echo "To actually create issues, run: $0"
else
    echo "=== ALL ISSUES CREATED SUCCESSFULLY ==="
fi
