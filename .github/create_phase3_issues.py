#!/usr/bin/env python3
"""
Script to create GitHub issues for Phase 3 deferred features.

This script creates individual GitHub issues for each Phase 3 feature
from the PHASE_3_DEFERRED_FEATURES.md tracking document.

Usage:
    python create_phase3_issues.py

Requirements:
    - PyGithub: pip install PyGithub
    - GitHub personal access token with 'repo' scope
    - Set GITHUB_TOKEN environment variable
"""

import os
import sys
from dataclasses import dataclass
from typing import List

try:
    from github import Github
except ImportError:
    print("Error: PyGithub not installed. Install with: pip install PyGithub")
    sys.exit(1)


@dataclass
class Phase3Issue:
    """Represents a Phase 3 deferred feature issue."""
    title: str
    body: str
    labels: List[str]


# Define all Phase 3 issues
PHASE3_ISSUES = [
    Phase3Issue(
        title="PR #832: Harden branded-variable disambiguations",
        body="""**Source**: https://github.com/noaa-gfdl/fre-cli/pull/832

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
- Phase 3 tracking issue: #27
""",
        labels=["enhancement", "phase-3"]
    ),

    Phase3Issue(
        title="PR #833: Improved omission tracking",
        body="""**Source**: https://github.com/noaa-gfdl/fre-cli/pull/833

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
- Phase 3 tracking issue: #27
""",
        labels=["enhancement", "phase-3"]
    ),

    Phase3Issue(
        title="PR #834: New `fremor init` command for config fetching",
        body="""**Source**: https://github.com/noaa-gfdl/fre-cli/pull/834

**Description**:
Add new CLI subcommand to fetch/initialize CMOR configuration files

**Impact**:
Improved user experience for initial setup

**Priority**: Medium - new feature, not a fix

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Adapt code to fremorizer's independent package structure
- Design the CLI interface as `fremor init` (not `fre cmor init`)
- Consider where config files should be fetched from (CMOR tables repository, etc.)
- Document the init workflow in user documentation

**Testing requirements**:
- All existing tests must continue to pass
- Add new tests for `fremor init` command
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
- Phase 3 tracking issue: #27
""",
        labels=["enhancement", "phase-3", "new-feature"]
    ),

    Phase3Issue(
        title="PR #836: Informative error on mip_era/table format mismatch",
        body="""**Source**: https://github.com/noaa-gfdl/fre-cli/pull/836

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
- Phase 3 tracking issue: #27
""",
        labels=["enhancement", "phase-3", "error-handling"]
    ),

    Phase3Issue(
        title="PR #837: Accept CF calendar aliases (noleap/365_day, etc.)",
        body="""**Source**: https://github.com/noaa-gfdl/fre-cli/pull/837

**Description**:
Support CF convention calendar aliases (e.g., "noleap" as alias for "365_day")

**Impact**:
Improved compatibility with various input data conventions

**Priority**: Medium

**fremorizer-specific considerations**:
- Review the original PR in fre-cli for implementation details
- Adapt code to fremorizer's independent package structure
- Ensure all CF standard calendar aliases are supported
- Consider normalization of calendar names internally

**CF calendar aliases to support**:
- `noleap` ↔ `365_day`
- `all_leap` ↔ `366_day`
- `360_day` (standard)
- `julian` (standard)
- `gregorian` ↔ `proleptic_gregorian` ↔ `standard`

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
- Phase 3 tracking issue: #27
""",
        labels=["enhancement", "phase-3", "compatibility"]
    ),

    Phase3Issue(
        title="PR #838: CMIP7 flavored tests",
        body="""**Source**: https://github.com/noaa-gfdl/fre-cli/pull/838

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
- Phase 3 tracking issue: #27
""",
        labels=["enhancement", "phase-3", "testing", "cmip7", "high-priority"]
    ),

    Phase3Issue(
        title="PR #846: Variable list semantics (map modeler vars to MIP table names)",
        body="""**Source**: https://github.com/noaa-gfdl/fre-cli/pull/846

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
- Phase 3 tracking issue: #27
""",
        labels=["enhancement", "phase-3", "variable-mapping"]
    ),

    Phase3Issue(
        title="PR #817: Update cmor to 3.14.2",
        body="""**Source**: https://github.com/noaa-gfdl/fre-cli/pull/817

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
- Phase 3 tracking issue: #27
""",
        labels=["enhancement", "phase-3", "dependencies"]
    ),
]


def create_issues(repo_name: str, dry_run: bool = True):
    """Create GitHub issues for Phase 3 features.

    Args:
        repo_name: Repository in format 'owner/repo'
        dry_run: If True, only print what would be created
    """
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    g = Github(token)

    try:
        repo = g.get_repo(repo_name)
        print(f"Repository: {repo.full_name}")
        print(f"Creating {len(PHASE3_ISSUES)} issues...")
        print()

        created_issues = []

        for i, issue_data in enumerate(PHASE3_ISSUES, 1):
            print(f"[{i}/{len(PHASE3_ISSUES)}] {issue_data.title}")

            if dry_run:
                print(f"  Labels: {', '.join(issue_data.labels)}")
                print(f"  Body preview: {issue_data.body[:100]}...")
                print("  [DRY RUN - Not created]")
            else:
                try:
                    issue = repo.create_issue(
                        title=issue_data.title,
                        body=issue_data.body,
                        labels=issue_data.labels
                    )
                    print(f"  ✓ Created: {issue.html_url}")
                    created_issues.append((issue.number, issue.html_url))
                except Exception as e:
                    print(f"  ✗ Error: {e}")

            print()

        if not dry_run and created_issues:
            print("\nSummary of created issues:")
            print("-" * 60)
            for num, url in created_issues:
                print(f"  #{num}: {url}")

        if dry_run:
            print("\n" + "=" * 60)
            print("DRY RUN MODE - No issues were created")
            print("To create issues, run with: --create")
            print("=" * 60)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Create GitHub issues for Phase 3 deferred features"
    )
    parser.add_argument(
        "--repo",
        default="ilaflott/fremorizer",
        help="Repository in format 'owner/repo' (default: ilaflott/fremorizer)"
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Actually create issues (default is dry-run mode)"
    )

    args = parser.parse_args()

    create_issues(args.repo, dry_run=not args.create)
