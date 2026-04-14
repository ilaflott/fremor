# Phase 2.5: Equivalence Testing with fre-cli

This document outlines the plan for validating that fremorizer produces equivalent output to fre.cmor in fre-cli.

## Objective

Establish confidence that fremorizer operates equivalently to the fre.cmor submodule it was derived from, ensuring no functional regressions were introduced during the package separation.

## Approach

### 1. Test Data Preparation

**Setup Requirements:**
- Install both fremorizer and fre-cli in separate environments
- Prepare identical test datasets for both tools
- Use existing test fixtures from `fremorizer/tests/test_files/`

**Test Cases:**
- Use the same input netCDF files
- Use the same CMOR table configurations (from cmor-tables submodule)
- Use the same experiment configuration JSON files
- Use the same variable lists

### 2. Comparative Testing Strategy

**A. CLI Command Equivalence**

Test that equivalent CLI commands produce identical results:

```bash
# fre-cli command
fre cmor run -d <indir> -l <varlist> -r <table> -p <expconfig> -o <outdir1>

# fremorizer command
fremor run -d <indir> -l <varlist> -r <table> -p <expconfig> -o <outdir2>
```

**B. Output Comparison**

For each test case, compare:
1. **File structure**: Verify output directory structure matches
2. **File metadata**: Compare global attributes, variable attributes
3. **Data values**: Verify numerical equivalence (within tolerance for floating-point precision)
4. **File naming**: Confirm output files follow same naming conventions

**C. Test Scenarios**

Minimum test coverage should include:

1. **Basic CMORization** (`fremor run`)
   - Single variable, monthly data
   - Multiple variables, different frequencies
   - Different MIP tables (Omon, Amon, etc.)

2. **YAML-based workflow** (`fremor yaml`)
   - Simple YAML configuration
   - Multi-component workflow
   - Start/stop year filtering

3. **Variable discovery** (`fremor find`)
   - Search across multiple tables
   - Variable presence validation

4. **Config generation** (`fremor config`)
   - Automatic YAML generation from directory tree
   - Variable list creation

5. **Edge cases**
   - Grid label handling (gn, gr)
   - Calendar type variations
   - Time chunk boundaries

### 3. Implementation Plan

**Option A: Automated CI Workflow** (Recommended)

Create `.github/workflows/equivalence_test.yml`:

```yaml
name: equivalence_test

on:
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  compare-with-fre-cli:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout fremorizer
        uses: actions/checkout@v4
        path: fremorizer

      - name: Checkout fre-cli
        uses: actions/checkout@v4
        with:
          repository: noaa-gfdl/fre-cli
          path: fre-cli

      - name: Setup Conda with miniforge
        uses: conda-incubator/setup-miniconda@v3
        with:
          miniforge-version: latest
          auto-activate-base: false

      - name: Remove unwanted conda channels
        run: |
          conda config --remove channels defaults || true
          conda config --remove channels main || true
          conda config --remove channels r || true
          conda config --set channel_priority strict

      - name: Create fremorizer environment
        run: |
          conda create -n fremorizer-test python>=3.11 -c conda-forge -c noaa-gfdl
          conda activate fremorizer-test
          cd fremorizer
          pip install .

      - name: Create fre-cli environment
        run: |
          conda create -n fre-cli-test python>=3.11 -c conda-forge -c noaa-gfdl
          conda activate fre-cli-test
          cd fre-cli
          pip install .

      - name: Run comparison tests
        run: |
          # Execute comparison script (to be created)
          python fremorizer/tests/equivalence/compare_with_fre_cli.py

      - name: Upload comparison report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: equivalence-report
          path: equivalence_report.md
```

**Option B: Manual Testing Script**

Create `fremorizer/tests/equivalence/compare_with_fre_cli.py`:
- Automated comparison script that can be run locally or in CI
- Generates detailed report of differences (if any)
- Returns exit code 0 for equivalence, non-zero for differences

### 4. Comparison Script Structure

```python
# fremorizer/tests/equivalence/compare_with_fre_cli.py

import subprocess
import tempfile
import netCDF4 as nc
import numpy as np
from pathlib import Path

class EquivalenceTest:
    def __init__(self, test_name):
        self.test_name = test_name
        self.fremorizer_env = "fremorizer-test"
        self.fre_cli_env = "fre-cli-test"

    def run_fremorizer(self, cmd_args):
        """Run fremor command in fremorizer environment"""
        # Implementation

    def run_fre_cli(self, cmd_args):
        """Run fre cmor command in fre-cli environment"""
        # Implementation

    def compare_outputs(self, dir1, dir2):
        """Compare output directories"""
        # Compare file structure
        # Compare netCDF files
        # Compare metadata
        # Return detailed comparison results

    def compare_netcdf_files(self, file1, file2):
        """Deep comparison of two netCDF files"""
        # Compare dimensions
        # Compare variables
        # Compare attributes
        # Compare data values (with tolerance)

def main():
    tests = [
        ("basic_monthly_amon", {...}),
        ("yaml_workflow", {...}),
        ("multi_variable", {...}),
        # More test cases
    ]

    results = []
    for test_name, test_config in tests:
        test = EquivalenceTest(test_name)
        result = test.run_and_compare(test_config)
        results.append(result)

    # Generate report
    generate_report(results)

    # Exit with appropriate code
    if all(r.passed for r in results):
        sys.exit(0)
    else:
        sys.exit(1)
```

### 5. Success Criteria

Equivalence is established when:

1. ✅ All test cases produce matching output file structures
2. ✅ All netCDF files have identical dimensions and variables
3. ✅ All metadata (global and variable attributes) match
4. ✅ All data values are numerically equivalent (within 1e-10 relative tolerance for floating-point)
5. ✅ No differences in file naming conventions
6. ✅ Same behavior for error cases (e.g., missing variables, invalid configs)

### 6. Known Acceptable Differences

Document any intentional differences (if any exist):

- **Import paths**: `from fre.cmor.X` → `from fremorizer.X` (internal only)
- **CLI command**: `fre cmor` → `fremor` (user-facing difference is intentional)
- **Package metadata**: Version strings, package names in attributes (acceptable)
- **Logging format**: Minor differences in log output format (acceptable if semantic content matches)

### 7. Implementation Timeline

**Prerequisites:**
- ✅ Phase 1-2 complete (package foundation and source files)
- ✅ CI/CD pipelines working (miniforge, correct channels)
- ⏳ Current CI workflows passing

**Implementation Steps:**

1. **Create comparison script** (1-2 days)
   - Basic netCDF comparison logic
   - Output structure validation
   - Report generation

2. **Define test cases** (1 day)
   - Select representative test scenarios
   - Prepare test data
   - Document expected behavior

3. **Create CI workflow** (1 day)
   - Set up dual environment installation
   - Integrate comparison script
   - Configure artifact uploads

4. **Execute and validate** (2-3 days)
   - Run tests locally first
   - Debug any differences found
   - Document acceptable vs. problematic differences
   - Iterate until equivalence achieved

5. **Documentation** (1 day)
   - Update this document with results
   - Add equivalence badge to README
   - Document any known differences

**Total estimated effort**: 6-8 days

### 8. Maintenance

After initial equivalence is established:

- Run equivalence tests on every PR that modifies core functionality
- Update test cases when new features are added
- Re-validate equivalence before each release
- Before implementing Phase 3 features, ensure equivalence baseline is solid

### 9. Notes and Considerations

**Dependencies:**
- Requires `netCDF4` Python library (already in environment.yaml)
- May need `xarray` for easier netCDF comparisons
- Consider using `numpy.testing.assert_allclose` for numerical comparisons

**Challenges:**
- Timestamps in output may differ (creation time, processing time) - these should be excluded from comparison
- Random number generation (if any) may cause differences - need deterministic test data
- File system ordering may affect output order - comparison should be order-independent

**Alternative Approaches:**
- Use existing test suite with both tools and compare pytest output
- Focus on subset of most critical functionality first
- Consider comparing outputs on real-world data from GFDL workflows

## References

- fre-cli repository: https://github.com/noaa-gfdl/fre-cli
- fre.cmor submodule: `fre/cmor/` in fre-cli
- fremorizer test suite: `fremorizer/tests/`
- NetCDF comparison tools: `netCDF4`, `xarray`
