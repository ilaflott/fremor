# Phase 3: Deferred Features from fre.cmor

This document tracks features from open fre.cmor pull requests that are intentionally deferred for future implementation in fremorizer. Each item corresponds to a specific PR in the [fre-cli repository](https://github.com/noaa-gfdl/fre-cli).

## Purpose

Phase 3 features represent enhancements and improvements that were in progress in the fre.cmor submodule. These are deferred to focus on:
1. Establishing a stable, working independent fremorizer package (Phase 1-2)
2. Validating equivalence with existing fre-cli functionality (Phase 2.5)
3. Ensuring CI/CD pipelines are robust and reliable

Once the foundation is solid and equivalence testing is complete, these features can be incorporated systematically.

## Phase 3 Items

### 1. ~~PR #826: Replace nccmp with netCDF4 in tests~~ ✅ COMPLETED
- **Source**: https://github.com/noaa-gfdl/fre-cli/pull/826
- **Description**: Replace external `nccmp` tool dependency with Python `netCDF4` library for comparing netCDF files in tests
- **Impact**: Eliminated external tool dependency, making tests more portable and reliable
- **Status**: Implemented — `nccmp` subprocess calls replaced with `netCDF4`/`numpy` assertions in `test_cmor_run_subtool.py`

### 2. PR #832: Harden branded-variable disambiguations
- **Source**: https://github.com/noaa-gfdl/fre-cli/pull/832
- **Description**: Improve handling of branded variable name disambiguation (e.g., when multiple variables map to same target)
- **Impact**: More robust variable handling in edge cases
- **Priority**: Medium

### 3. PR #833: Improved omission tracking
- **Source**: https://github.com/noaa-gfdl/fre-cli/pull/833
- **Description**: Better tracking and reporting of variables that are omitted during CMORization
- **Impact**: Improved user feedback and debugging capabilities
- **Priority**: Medium

### 4. PR #834: New `fremor init` command for config fetching
- **Source**: https://github.com/noaa-gfdl/fre-cli/pull/834
- **Description**: Add new CLI subcommand to fetch/initialize CMOR configuration files
- **Impact**: Improved user experience for initial setup
- **Priority**: Medium - new feature, not a fix

### 5. PR #836: Informative error on mip_era/table format mismatch
- **Source**: https://github.com/noaa-gfdl/fre-cli/pull/836
- **Description**: Provide clear error messages when MIP era and table format don't match
- **Impact**: Better user experience and faster debugging
- **Priority**: Medium

### 6. PR #837: Accept CF calendar aliases (noleap/365_day, etc.)
- **Source**: https://github.com/noaa-gfdl/fre-cli/pull/837
- **Description**: Support CF convention calendar aliases (e.g., "noleap" as alias for "365_day")
- **Impact**: Improved compatibility with various input data conventions
- **Priority**: Medium

### 7. PR #838: CMIP7 flavored tests
- **Source**: https://github.com/noaa-gfdl/fre-cli/pull/838
- **Description**: Add test cases specifically for CMIP7 conventions and requirements
- **Impact**: Ensure CMIP7 compatibility and catch CMIP7-specific issues
- **Priority**: High - CMIP7 support is important for future-proofing

### 8. PR #846: Variable list semantics (map modeler vars to MIP table names)
- **Source**: https://github.com/noaa-gfdl/fre-cli/pull/846
- **Description**: Improve variable list handling to better map model variable names to MIP table variable names
- **Impact**: More flexible and intuitive variable mapping
- **Priority**: Medium

### 9. PR #817: Update cmor to 3.14.2
- **Source**: https://github.com/noaa-gfdl/fre-cli/pull/817
- **Description**: Update the CMOR library dependency from current version to 3.14.2
- **Impact**: Access to latest CMOR features and bug fixes
- **Priority**: Medium - should verify compatibility before upgrading

## Implementation Strategy

When ready to implement Phase 3 features:

1. **Create individual GitHub issues** for each item above with:
   - Link to the original fre-cli PR
   - Description of the feature/fix
   - Any fremorizer-specific considerations
   - Testing requirements

2. **Prioritize based on**:
   - User impact (e.g., PR #826 fixes current test failures)
   - Dependencies between features
   - Alignment with CMIP6/CMIP7 timelines

3. **Implementation approach**:
   - Review the original PR in fre-cli for implementation details
   - Adapt code to fremorizer's independent package structure
   - Ensure all changes maintain test coverage
   - Update documentation as needed
   - Validate no regressions in existing functionality

4. **Testing requirements**:
   - All existing tests must continue to pass
   - New tests should be added for new features
   - Phase 2.5 equivalence tests should still pass after each feature addition

## Notes

- Phase 2.5 (equivalence testing with fre-cli) should be completed **before** implementing Phase 3 features
- Each Phase 3 feature should be implemented in a separate PR for easier review and rollback if needed
- Consider creating a project board to track Phase 3 implementation progress

## References

- Original fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- fre.cmor submodule path: `fre/cmor/` in fre-cli
- This fremorizer PR: https://github.com/ilaflott/fremorizer/pull/1
