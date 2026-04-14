#!/usr/bin/env python3
'''
Equivalence testing script for fremorizer vs fre-cli (fre cmor).

Runs the same CMORization operations through both tools and compares
output file structure, netCDF metadata, and data values to validate
that fremorizer produces equivalent results to fre.cmor in fre-cli.

Can be run locally (if both tools are installed) or via CI workflow.

Usage:
    python -m fremorizer.tests.equivalence.compare_with_fre_cli

Environment variables:
    FREMORIZER_CMD  – override the fremorizer CLI entry point
                      (default: "fremor")
    FRE_CLI_CMD     – override the fre-cli cmor entry point
                      (default: "fre cmor")
    TEST_FILES_DIR  – path to shared test fixtures
                      (default: auto-detected from package location)
'''

import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import netCDF4 as nc
import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)5s] %(message)s',
)
logger = logging.getLogger(__name__)

FREMOR_CMD = os.environ.get('FREMORIZER_CMD', 'fremor')
FRE_CLI_CMD = os.environ.get('FRE_CLI_CMD', 'fre cmor')

# Locate test fixtures relative to the package when not overridden
_PKG_DIR = Path(__file__).resolve().parent.parent.parent  # fremorizer/
TEST_FILES_DIR = Path(
    os.environ.get('TEST_FILES_DIR', str(_PKG_DIR / 'tests' / 'test_files'))
)

# Relative tolerance for floating-point data comparison
RTOL = 1e-10
ATOL = 0.0

# Global attributes that are expected to differ between tools
IGNORED_GLOBAL_ATTRS = frozenset({
    'history',          # timestamps differ
    'creation_date',    # timestamps differ
    'tracking_id',      # UUID, always differs
})

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ComparisonResult:
    '''Result of a single equivalence comparison.'''
    test_name: str
    passed: bool = True
    messages: list = field(default_factory=list)

    def fail(self, msg: str):
        '''Record a failure message.'''
        self.passed = False
        self.messages.append(f'FAIL: {msg}')

    def info(self, msg: str):
        '''Record an informational message.'''
        self.messages.append(f'INFO: {msg}')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_cli(cmd_str: str, label: str) -> subprocess.CompletedProcess:
    '''Run a CLI command string and return the CompletedProcess.'''
    logger.info('Running [%s]: %s', label, cmd_str)
    result = subprocess.run(
        cmd_str,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        logger.warning(
            '[%s] non-zero exit (%d):\nstdout: %s\nstderr: %s',
            label, result.returncode, result.stdout, result.stderr,
        )
    return result


def _find_nc_files(directory: Path) -> list:
    '''Recursively find all .nc files under *directory*, sorted.'''
    return sorted(directory.rglob('*.nc'))


def _relative_nc_paths(base: Path, nc_files: list) -> list:
    '''Return sorted list of paths relative to *base*.'''
    return sorted(str(p.relative_to(base)) for p in nc_files)


# ---------------------------------------------------------------------------
# NetCDF comparison
# ---------------------------------------------------------------------------

def compare_netcdf_files(file1: Path, file2: Path, result: ComparisonResult):
    '''
    Deep comparison of two netCDF files.

    Checks dimensions, variables, attributes, and data values.
    Differences are recorded on *result*.
    '''
    ds1 = nc.Dataset(str(file1), 'r')
    ds2 = nc.Dataset(str(file2), 'r')

    try:
        _compare_dimensions(ds1, ds2, file1.name, result)
        _compare_variables(ds1, ds2, file1.name, result)
        _compare_global_attrs(ds1, ds2, file1.name, result)
    finally:
        ds1.close()
        ds2.close()


def _compare_dimensions(ds1, ds2, fname, result):
    dims1 = set(ds1.dimensions.keys())
    dims2 = set(ds2.dimensions.keys())
    if dims1 != dims2:
        result.fail(
            f'{fname}: dimension mismatch — '
            f'only in fremorizer: {dims1 - dims2}, only in fre-cli: {dims2 - dims1}'
        )
        return

    for dim in sorted(dims1):
        len1 = len(ds1.dimensions[dim])
        len2 = len(ds2.dimensions[dim])
        if len1 != len2:
            result.fail(
                f'{fname}: dimension "{dim}" length differs '
                f'(fremorizer={len1}, fre-cli={len2})'
            )


def _compare_variables(ds1, ds2, fname, result):
    vars1 = set(ds1.variables.keys())
    vars2 = set(ds2.variables.keys())
    if vars1 != vars2:
        result.fail(
            f'{fname}: variable mismatch — '
            f'only in fremorizer: {vars1 - vars2}, only in fre-cli: {vars2 - vars1}'
        )

    common_vars = vars1 & vars2
    for var in sorted(common_vars):
        v1 = ds1.variables[var]
        v2 = ds2.variables[var]

        # Compare variable attributes
        attrs1 = set(v1.ncattrs())
        attrs2 = set(v2.ncattrs())
        if attrs1 != attrs2:
            result.fail(
                f'{fname}: variable "{var}" attribute mismatch — '
                f'only in fremorizer: {attrs1 - attrs2}, '
                f'only in fre-cli: {attrs2 - attrs1}'
            )
        for attr in sorted(attrs1 & attrs2):
            val1 = v1.getncattr(attr)
            val2 = v2.getncattr(attr)
            if isinstance(val1, np.ndarray):
                if not np.allclose(val1, val2, rtol=RTOL, atol=ATOL, equal_nan=True):
                    result.fail(
                        f'{fname}: variable "{var}" attr "{attr}" data differs'
                    )
            elif val1 != val2:
                result.fail(
                    f'{fname}: variable "{var}" attr "{attr}" differs '
                    f'(fremorizer={val1!r}, fre-cli={val2!r})'
                )

        # Compare data values
        try:
            data1 = v1[:]
            data2 = v2[:]
        except Exception as exc:  # pylint: disable=broad-except
            result.fail(f'{fname}: could not read data for variable "{var}": {exc}')
            continue

        if isinstance(data1, np.ma.MaskedArray) or isinstance(data2, np.ma.MaskedArray):
            d1 = np.ma.filled(data1, fill_value=np.nan)
            d2 = np.ma.filled(data2, fill_value=np.nan)
        else:
            d1 = np.asarray(data1)
            d2 = np.asarray(data2)

        if d1.shape != d2.shape:
            result.fail(
                f'{fname}: variable "{var}" shape differs '
                f'(fremorizer={d1.shape}, fre-cli={d2.shape})'
            )
            continue

        if not np.allclose(d1, d2, rtol=RTOL, atol=ATOL, equal_nan=True):
            max_diff = float(np.nanmax(np.abs(d1 - d2)))
            result.fail(
                f'{fname}: variable "{var}" data differs (max abs diff={max_diff})'
            )


def _compare_global_attrs(ds1, ds2, fname, result):
    attrs1 = set(ds1.ncattrs()) - IGNORED_GLOBAL_ATTRS
    attrs2 = set(ds2.ncattrs()) - IGNORED_GLOBAL_ATTRS
    if attrs1 != attrs2:
        result.fail(
            f'{fname}: global attribute mismatch — '
            f'only in fremorizer: {attrs1 - attrs2}, '
            f'only in fre-cli: {attrs2 - attrs1}'
        )

    for attr in sorted(attrs1 & attrs2):
        val1 = ds1.getncattr(attr)
        val2 = ds2.getncattr(attr)
        if isinstance(val1, np.ndarray):
            if not np.allclose(val1, val2, rtol=RTOL, atol=ATOL, equal_nan=True):
                result.fail(f'{fname}: global attr "{attr}" data differs')
        elif val1 != val2:
            result.fail(
                f'{fname}: global attr "{attr}" differs '
                f'(fremorizer={val1!r}, fre-cli={val2!r})'
            )


# ---------------------------------------------------------------------------
# Output directory comparison
# ---------------------------------------------------------------------------

def compare_output_dirs(dir1: Path, dir2: Path, result: ComparisonResult):
    '''
    Compare two output directory trees produced by fremorizer and fre-cli.

    Checks file-structure equivalence then compares each netCDF file.
    '''
    nc_files1 = _find_nc_files(dir1)
    nc_files2 = _find_nc_files(dir2)

    rel1 = _relative_nc_paths(dir1, nc_files1)
    rel2 = _relative_nc_paths(dir2, nc_files2)

    if rel1 != rel2:
        only1 = set(rel1) - set(rel2)
        only2 = set(rel2) - set(rel1)
        result.fail(
            f'Output file structure differs — '
            f'only in fremorizer: {only1}, only in fre-cli: {only2}'
        )
        # Still compare common files
        common = sorted(set(rel1) & set(rel2))
    else:
        common = rel1
        result.info(f'File structure matches ({len(common)} netCDF file(s))')

    for rel_path in common:
        f1 = dir1 / rel_path
        f2 = dir2 / rel_path
        compare_netcdf_files(f1, f2, result)


# ---------------------------------------------------------------------------
# Test-case runners
# ---------------------------------------------------------------------------

class EquivalenceTest:
    '''Orchestrates a single equivalence test between fremorizer and fre-cli.'''

    def __init__(self, test_name: str, work_dir: Path):
        self.test_name = test_name
        self.work_dir = work_dir
        self.fremor_outdir = work_dir / 'fremor_out'
        self.frecli_outdir = work_dir / 'frecli_out'
        self.fremor_outdir.mkdir(parents=True, exist_ok=True)
        self.frecli_outdir.mkdir(parents=True, exist_ok=True)

    def run_fremorizer(self, subcmd: str, args: str) -> subprocess.CompletedProcess:
        '''Run a fremor <subcmd> <args> command.'''
        cmd = f'{FREMOR_CMD} {subcmd} {args}'
        return _run_cli(cmd, f'fremorizer/{self.test_name}')

    def run_fre_cli(self, subcmd: str, args: str) -> subprocess.CompletedProcess:
        '''Run a fre cmor <subcmd> <args> command.'''
        cmd = f'{FRE_CLI_CMD} {subcmd} {args}'
        return _run_cli(cmd, f'fre-cli/{self.test_name}')

    def compare(self) -> ComparisonResult:
        '''Compare outputs produced by both tools.'''
        result = ComparisonResult(test_name=self.test_name)
        compare_output_dirs(self.fremor_outdir, self.frecli_outdir, result)
        return result


# ---------------------------------------------------------------------------
# Concrete test cases
# ---------------------------------------------------------------------------

def _prepare_nc_input(test_files_dir: Path):
    '''
    Ensure the netCDF input file exists by running ncgen on the CDL source.
    Returns the path to the directory containing the .nc file.
    '''
    cdl_file = test_files_dir / 'reduced_ascii_files' / \
        'reduced_ocean_monthly_1x1deg.199301-199302.sos.cdl'
    nc_dir = test_files_dir / 'ocean_sos_var_file'
    nc_file = nc_dir / 'reduced_ocean_monthly_1x1deg.199301-199302.sos.nc'

    nc_dir.mkdir(parents=True, exist_ok=True)
    if not nc_file.exists():
        subprocess.run(
            ['ncgen3', '-k', 'netCDF-4', '-o', str(nc_file), str(cdl_file)],
            check=True,
        )
    return nc_dir


def test_basic_cmor_run(work_dir: Path) -> ComparisonResult:
    '''
    Basic CMORization run: single variable (sos), monthly ocean data.

    Equivalent to:
        fremor run -d <indir> -l <varlist> -r <table> -p <expconfig> -o <outdir> --run_one \
            -g gr --grid_desc "..." --nom_res "..." --calendar julian

        fre cmor run -d <indir> -l <varlist> -r <table> -p <expconfig> -o <outdir> --run_one \
            -g gr --grid_desc "..." --nom_res "..." --calendar julian
    '''
    test = EquivalenceTest('basic_cmor_run', work_dir / 'basic_cmor_run')

    indir = _prepare_nc_input(TEST_FILES_DIR)
    varlist = TEST_FILES_DIR / 'varlist'
    table_config = TEST_FILES_DIR / 'cmip6-cmor-tables' / 'Tables' / 'CMIP6_Omon.json'
    exp_config = TEST_FILES_DIR / 'CMOR_input_example.json'

    shared_args = (
        f'-d {indir} '
        f'-l {varlist} '
        f'-r {table_config} '
        f'-p {exp_config} '
        f'-o {{outdir}} '
        f'--run_one '
        f'-g gr '
        f'--grid_desc "regridded to FOO grid from native" '
        f'--nom_res "10000 km" '
        f'--calendar julian'
    )

    res_fremor = test.run_fremorizer(
        'run', shared_args.format(outdir=test.fremor_outdir)
    )
    res_frecli = test.run_fre_cli(
        'run', shared_args.format(outdir=test.frecli_outdir)
    )

    result = ComparisonResult(test_name='basic_cmor_run')

    # Check both commands completed
    if res_fremor.returncode != 0:
        result.fail(f'fremorizer exited with code {res_fremor.returncode}: {res_fremor.stderr}')
    if res_frecli.returncode != 0:
        result.fail(f'fre-cli exited with code {res_frecli.returncode}: {res_frecli.stderr}')

    if res_fremor.returncode == 0 and res_frecli.returncode == 0:
        compare_output_dirs(test.fremor_outdir, test.frecli_outdir, result)
    else:
        result.info('Skipping output comparison due to command failure(s)')

    return result


def test_basic_cmor_run_diff_varlist(work_dir: Path) -> ComparisonResult:
    '''
    CMORization with a variable list where local/target names differ.
    '''
    test = EquivalenceTest(
        'cmor_run_diff_varlist', work_dir / 'cmor_run_diff_varlist'
    )

    indir = _prepare_nc_input(TEST_FILES_DIR)
    varlist = TEST_FILES_DIR / 'varlist_local_target_vars_differ'
    table_config = TEST_FILES_DIR / 'cmip6-cmor-tables' / 'Tables' / 'CMIP6_Omon.json'
    exp_config = TEST_FILES_DIR / 'CMOR_input_example.json'

    # Ensure the copy of the nc input with different name exists
    src_nc = indir / 'reduced_ocean_monthly_1x1deg.199301-199302.sos.nc'
    dst_nc = indir / 'reduced_ocean_monthly_1x1deg.199301-199302.sosV2.nc'
    if not dst_nc.exists() and src_nc.exists():
        shutil.copy(str(src_nc), str(dst_nc))

    shared_args = (
        f'-d {indir} '
        f'-l {varlist} '
        f'-r {table_config} '
        f'-p {exp_config} '
        f'-o {{outdir}} '
        f'--run_one '
        f'-g gr '
        f'--grid_desc "regridded to FOO grid from native" '
        f'--nom_res "10000 km" '
        f'--calendar julian'
    )

    res_fremor = test.run_fremorizer(
        'run', shared_args.format(outdir=test.fremor_outdir)
    )
    res_frecli = test.run_fre_cli(
        'run', shared_args.format(outdir=test.frecli_outdir)
    )

    result = ComparisonResult(test_name='cmor_run_diff_varlist')

    if res_fremor.returncode != 0:
        result.fail(f'fremorizer exited with code {res_fremor.returncode}: {res_fremor.stderr}')
    if res_frecli.returncode != 0:
        result.fail(f'fre-cli exited with code {res_frecli.returncode}: {res_frecli.stderr}')

    if res_fremor.returncode == 0 and res_frecli.returncode == 0:
        compare_output_dirs(test.fremor_outdir, test.frecli_outdir, result)
    else:
        result.info('Skipping output comparison due to command failure(s)')

    return result


def test_find_subtool(work_dir: Path) -> ComparisonResult:
    '''
    Variable discovery: search across CMIP6 tables for a known variable.

    Compares stdout output of both tools (stripping timestamps/paths that differ).
    '''
    result = ComparisonResult(test_name='find_subtool')

    varlist = TEST_FILES_DIR / 'varlist'
    table_dir = TEST_FILES_DIR / 'cmip6-cmor-tables' / 'Tables'

    fremor_res = _run_cli(
        f'{FREMOR_CMD} find -l {varlist} -r {table_dir}',
        'fremorizer/find',
    )
    frecli_res = _run_cli(
        f'{FRE_CLI_CMD} find -l {varlist} -r {table_dir}',
        'fre-cli/find',
    )

    if fremor_res.returncode != frecli_res.returncode:
        result.fail(
            f'Exit code mismatch: fremorizer={fremor_res.returncode}, '
            f'fre-cli={frecli_res.returncode}'
        )
    else:
        result.info(f'Both exited with code {fremor_res.returncode}')

    # Compare stdout line-by-line (ignoring blank-line differences)
    out1 = [l.strip() for l in fremor_res.stdout.splitlines() if l.strip()]
    out2 = [l.strip() for l in frecli_res.stdout.splitlines() if l.strip()]
    if out1 != out2:
        result.fail('stdout differs between fremorizer and fre-cli find output')
        result.info(f'fremorizer output ({len(out1)} lines): {out1[:10]}...')
        result.info(f'fre-cli output ({len(out2)} lines): {out2[:10]}...')
    else:
        result.info(f'stdout matches ({len(out1)} lines)')

    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(results: list, report_path: Path):
    '''Write a Markdown equivalence report.'''
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    lines = [
        '# Equivalence Test Report',
        '',
        f'**Generated:** {now}',
        '',
        '## Summary',
        '',
        f'| Test | Status |',
        f'|------|--------|',
    ]
    for r in results:
        status = '✅ PASS' if r.passed else '❌ FAIL'
        lines.append(f'| {r.test_name} | {status} |')

    all_passed = all(r.passed for r in results)
    lines.extend([
        '',
        f'**Overall:** {"✅ ALL PASSED" if all_passed else "❌ FAILURES DETECTED"}',
        '',
    ])

    for r in results:
        lines.extend([
            f'## {r.test_name}',
            '',
        ])
        if r.messages:
            for msg in r.messages:
                lines.append(f'- {msg}')
        else:
            lines.append('- No issues detected.')
        lines.append('')

    lines.extend([
        '## Known Acceptable Differences',
        '',
        '- **Import paths**: `from fre.cmor.X` → `from fremorizer.X` (internal only)',
        '- **CLI command**: `fre cmor` → `fremor` (user-facing difference is intentional)',
        '- **Package metadata**: Version strings, package names in attributes (acceptable)',
        '- **Logging format**: Minor differences in log output format (acceptable)',
        '- **history / creation_date / tracking_id**: Timestamps and UUIDs excluded from comparison',
        '',
    ])

    report_path.write_text('\n'.join(lines), encoding='utf-8')
    logger.info('Report written to %s', report_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    '''Run all equivalence tests and generate a report.'''
    # Verify both tools are available
    for cmd, label in [(FREMOR_CMD, 'fremorizer'), (FRE_CLI_CMD.split()[0], 'fre-cli')]:
        if shutil.which(cmd) is None:
            logger.error('%s CLI (%s) not found on PATH', label, cmd)
            sys.exit(2)

    work_dir = Path(tempfile.mkdtemp(prefix='equiv_test_'))
    logger.info('Working directory: %s', work_dir)

    test_cases = [
        test_basic_cmor_run,
        test_basic_cmor_run_diff_varlist,
        test_find_subtool,
    ]

    results = []
    for test_fn in test_cases:
        logger.info('--- Running: %s ---', test_fn.__name__)
        try:
            result = test_fn(work_dir)
        except Exception as exc:  # pylint: disable=broad-except
            result = ComparisonResult(test_name=test_fn.__name__)
            result.fail(f'Unhandled exception: {exc}')
        results.append(result)
        status = 'PASS' if result.passed else 'FAIL'
        logger.info('--- %s: %s ---', test_fn.__name__, status)

    # Write report
    report_path = Path(os.environ.get(
        'EQUIVALENCE_REPORT_PATH', 'equivalence_report.md'
    ))
    generate_report(results, report_path)

    # Exit
    if all(r.passed for r in results):
        logger.info('All equivalence tests passed.')
        sys.exit(0)
    else:
        n_fail = sum(1 for r in results if not r.passed)
        logger.error('%d of %d equivalence test(s) failed.', n_fail, len(results))
        sys.exit(1)


if __name__ == '__main__':
    main()
