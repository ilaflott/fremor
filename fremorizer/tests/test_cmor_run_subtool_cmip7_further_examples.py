'''
Expanded set of CMIP7 tests for fremor run — cases beyond test_cmor_run_subtool_cmip7.py.

These tests exercise cmor_run_subtool against a variety of variables, tables,
and grid labels drawn from a mock pp-archive, targeting CMIP7 experiment
configuration and CMIP7-format CMOR tables.

.. tip:: pytest temp directories
   By default pytest removes temp directories after the session. To keep
   them around for debugging, run::

       pytest --basetemp=/tmp/fremorizer-debug -k test_case_cmip7 -x

   Output files will then persist under ``/tmp/fremorizer-debug``.
'''

from datetime import date
import glob
from pathlib import Path

import pytest

from fremorizer import cmor_run_subtool
from fremorizer.tests.conftest import ncgen


# ── path constants ──────────────────────────────────────────────────────────
ROOTDIR = 'fremorizer/tests/test_files'
CMORBITE_VARLIST = f'{ROOTDIR}/CMORbite_var_list.json'

# cmip7 table repo
CMIP7_TABLE_REPO_PATH = f'{ROOTDIR}/cmip7-cmor-tables'

# experiment config (materialised by conftest._write_exp_configs)
EXP_CONFIG_CMIP7 = f'{ROOTDIR}/CMOR_CMIP7_input_example.json'

# determined by cmor_run_subtool
YYYYMMDD = date.today().strftime('%Y%m%d')

# mock-archive base paths
MOCK_ARCHIVE_ROOT = f'{ROOTDIR}/ascii_files/mock_archive'
ESM4_DEV_PP_DIR = (
    'USER/CMIP7/ESM4/DEV/ESM4.5v01_om5b04_piC'
    '/gfdl.ncrc5-intel23-prod-openmp/pp'
)

# CMIP7 output dir structure
# (activity_id/source_id/experiment_id/member_id/variable_id/branding_suffix/grid_label)
CMOR_CREATES_DIR_BASE_CMIP7 = (
    'CMIP/DUMMY-MODEL/historical/r3i1p1f3'
)


# ── helper: convert CDLs to NC in a test directory ─────────────────────────
def _ncgen_for_case(testfile_dir, opt_var_name):
    '''Convert the CDL file(s) for *opt_var_name* to NetCDF-4 inside *testfile_dir*.

    Returns the path to the primary NC file. Also generates ancillary files
    (e.g. ``ocean_monthly.static.nc`` for native ocean grid variables).
    '''
    cdl_files = glob.glob(f'{testfile_dir}*.{opt_var_name}.cdl')
    assert len(cdl_files) >= 1, (
        f'no CDL file found for variable {opt_var_name} in {testfile_dir}'
    )
    cdl_file = cdl_files[0]
    nc_file = cdl_file.replace('.cdl', '.nc')
    ncgen(cdl_file, nc_file)

    # ancillary files required by specific variables
    if opt_var_name == 'sos':
        static_cdl = testfile_dir.replace(
            'ts/monthly/5yr/', 'ocean_monthly.static.cdl'
        )
        if Path(static_cdl).exists():
            ncgen(static_cdl, static_cdl.replace('.cdl', '.nc'))

    return nc_file


# ── CMIP7 parametrized tests ──────────────────────────────────────────────
@pytest.mark.skip(reason='under development')
@pytest.mark.parametrize(
    'testfile_dir,table,opt_var_name,grid_label,start,calendar',
    [
        pytest.param(
            f'{MOCK_ARCHIVE_ROOT}/{ESM4_DEV_PP_DIR}'
            '/ocean_monthly_z_1x1deg/ts/monthly/5yr/',
            'CMIP7_ocean', 'so', 'g999', '0001', 'noleap',
            id='ocean_so_g999',
        ),
    ],
)
def test_case_cmip7_ocean_so(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    testfile_dir, table, opt_var_name, grid_label, start, calendar,
    tmp_path, monkeypatch,
):
    '''Run cmor_run_subtool for CMIP7 ocean so variable and assert output exists.'''
    _ncgen_for_case(testfile_dir, opt_var_name)

    table_file = f'{CMIP7_TABLE_REPO_PATH}/tables/{table}.json'
    outdir = str(tmp_path / 'outdir')

    cmor_run_subtool(
        indir=testfile_dir,
        json_var_list=CMORBITE_VARLIST,
        json_table_config=table_file,
        json_exp_config=EXP_CONFIG_CMIP7,
        outdir=outdir,
        run_one_mode=True,
        opt_var_name=opt_var_name,
        grid='FOO_PLACEHOLDER',
        grid_label=grid_label,
        nom_res='10000 km',
        start=start,
        calendar_type=calendar,
    )

    # CMIP7 output_path_template:
    #   <activity_id>/<source_id>/<experiment_id>/<member_id>/
    #   <variable_id>/<branding_suffix>/<grid_label>
    # Use recursive glob to find output regardless of branding suffix.
    cmor_output_glob = (
        f'{outdir}/{CMOR_CREATES_DIR_BASE_CMIP7}'
        f'/{opt_var_name}/**/*{opt_var_name}*{grid_label}*.nc'
    )
    cmor_output_files = glob.glob(cmor_output_glob, recursive=True)
    assert len(cmor_output_files) >= 1, (
        f'no CMOR output found matching {cmor_output_glob}'
    )
    assert Path(cmor_output_files[0]).exists()


@pytest.mark.skip(reason='under development')
@pytest.mark.parametrize(
    'testfile_dir,table,opt_var_name,grid_label,start,calendar',
    [
        pytest.param(
            f'{MOCK_ARCHIVE_ROOT}/{ESM4_DEV_PP_DIR}'
            '/ocean_monthly/ts/monthly/5yr/',
            'CMIP7_ocean', 'sos', 'g999', '0001', 'noleap',
            id='ocean_sos_g999',
        ),
    ],
)
def test_case_cmip7_ocean_sos(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    testfile_dir, table, opt_var_name, grid_label, start, calendar,
    tmp_path, monkeypatch,
):
    '''Run cmor_run_subtool for CMIP7 ocean sos variable and assert output exists.'''
    _ncgen_for_case(testfile_dir, opt_var_name)

    table_file = f'{CMIP7_TABLE_REPO_PATH}/tables/{table}.json'
    outdir = str(tmp_path / 'outdir')

    cmor_run_subtool(
        indir=testfile_dir,
        json_var_list=CMORBITE_VARLIST,
        json_table_config=table_file,
        json_exp_config=EXP_CONFIG_CMIP7,
        outdir=outdir,
        run_one_mode=True,
        opt_var_name=opt_var_name,
        grid='FOO_PLACEHOLDER',
        grid_label=grid_label,
        nom_res='10000 km',
        start=start,
        calendar_type=calendar,
    )

    cmor_output_glob = (
        f'{outdir}/{CMOR_CREATES_DIR_BASE_CMIP7}'
        f'/{opt_var_name}/**/*{opt_var_name}*{grid_label}*.nc'
    )
    cmor_output_files = glob.glob(cmor_output_glob, recursive=True)
    assert len(cmor_output_files) >= 1, (
        f'no CMOR output found matching {cmor_output_glob}'
    )
    assert Path(cmor_output_files[0]).exists()


@pytest.mark.skip(reason='under development')
@pytest.mark.parametrize(
    'testfile_dir,table,opt_var_name,grid_label,start,calendar',
    [
        pytest.param(
            f'{MOCK_ARCHIVE_ROOT}/{ESM4_DEV_PP_DIR}'
            '/land/ts/monthly/5yr/',
            'CMIP7_land', 'lai', 'g999', '0001', 'noleap',
            id='land_lai_g999',
        ),
    ],
)
def test_case_cmip7_land_lai(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    testfile_dir, table, opt_var_name, grid_label, start, calendar,
    tmp_path, monkeypatch,
):
    '''Run cmor_run_subtool for CMIP7 land lai variable and assert output exists.'''
    _ncgen_for_case(testfile_dir, opt_var_name)

    table_file = f'{CMIP7_TABLE_REPO_PATH}/tables/{table}.json'
    outdir = str(tmp_path / 'outdir')

    cmor_run_subtool(
        indir=testfile_dir,
        json_var_list=CMORBITE_VARLIST,
        json_table_config=table_file,
        json_exp_config=EXP_CONFIG_CMIP7,
        outdir=outdir,
        run_one_mode=True,
        opt_var_name=opt_var_name,
        grid='FOO_PLACEHOLDER',
        grid_label=grid_label,
        nom_res='10000 km',
        start=start,
        calendar_type=calendar,
    )

    cmor_output_glob = (
        f'{outdir}/{CMOR_CREATES_DIR_BASE_CMIP7}'
        f'/{opt_var_name}/**/*{opt_var_name}*{grid_label}*.nc'
    )
    cmor_output_files = glob.glob(cmor_output_glob, recursive=True)
    assert len(cmor_output_files) >= 1, (
        f'no CMOR output found matching {cmor_output_glob}'
    )
    assert Path(cmor_output_files[0]).exists()
