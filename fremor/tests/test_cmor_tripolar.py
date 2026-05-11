"""
tests for fremor.cmor_tripolar.load_tripolar_grid
"""

from pathlib import Path
import shutil

import netCDF4
import numpy as np
import pytest

from fremor.cmor_tripolar import load_tripolar_grid


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _make_mock_statics_nc(path: Path,
                          yh_size: int = 4,
                          xh_size: int = 5) -> None:
    """
    Write a minimal ocean-statics-like NetCDF file at *path* that contains
    the variables load_tripolar_grid expects:
    geolat, geolon, geolat_c, geolon_c, yh, xh, yq, xq.
    """
    yq_size = yh_size + 1
    xq_size = xh_size + 1

    ds = netCDF4.Dataset(str(path), 'w')
    ds.createDimension('yh', yh_size)
    ds.createDimension('xh', xh_size)
    ds.createDimension('yq', yq_size)
    ds.createDimension('xq', xq_size)

    # 2-D center coordinates
    geolat = ds.createVariable('geolat', 'f4', ('yh', 'xh'))
    geolat[:] = np.linspace(-90, 90, yh_size * xh_size).reshape(yh_size, xh_size)
    geolon = ds.createVariable('geolon', 'f4', ('yh', 'xh'))
    geolon[:] = np.linspace(0, 60, yh_size * xh_size).reshape(yh_size, xh_size)

    # 2-D corner (q-point) coordinates  — shape (yq, xq)
    geolat_c = ds.createVariable('geolat_c', 'f4', ('yq', 'xq'))
    geolat_c[:] = np.linspace(-90, 90, yq_size * xq_size).reshape(yq_size, xq_size)
    geolon_c = ds.createVariable('geolon_c', 'f4', ('yq', 'xq'))
    geolon_c[:] = np.linspace(0, 60, yq_size * xq_size).reshape(yq_size, xq_size)

    # 1-D axis coordinates
    yh_var = ds.createVariable('yh', 'f4', ('yh',))
    yh_var[:] = np.linspace(-80, 80, yh_size)
    xh_var = ds.createVariable('xh', 'f4', ('xh',))
    xh_var[:] = np.linspace(0, 60, xh_size)

    # q-point 1-D coordinates (one element longer each axis)
    yq_var = ds.createVariable('yq', 'f4', ('yq',))
    yq_var[:] = np.linspace(-90, 90, yq_size)
    xq_var = ds.createVariable('xq', 'f4', ('xq',))
    xq_var[:] = np.linspace(-10, 70, xq_size)

    ds.close()


def _make_mock_data_nc(path: Path, yh_size: int = 4, xh_size: int = 5) -> None:
    """
    Write a minimal data NetCDF file that has yh/xh dimensions but
    no lat/lon yet (simulating a tripolar ocean file before statics injection).
    """
    ds = netCDF4.Dataset(str(path), 'w')
    ds.createDimension('yh', yh_size)
    ds.createDimension('xh', xh_size)
    ds.createDimension('nv', 2)
    # deliberately do NOT add lat/lon — that's the job of load_tripolar_grid
    sos = ds.createVariable('sos', 'f4', ('yh', 'xh'))
    sos[:] = np.ones((yh_size, xh_size))
    yh_v = ds.createVariable('yh', 'f4', ('yh',))
    yh_v[:] = np.linspace(-80, 80, yh_size)
    xh_v = ds.createVariable('xh', 'f4', ('xh',))
    xh_v[:] = np.linspace(0, 60, xh_size)
    ds.close()


# ---------------------------------------------------------------------------
# tests
# ---------------------------------------------------------------------------

class TestLoadTripolarGrid:
    """Tests for load_tripolar_grid using mock statics and data files."""

    def test_return_keys(self, tmp_path):
        """
        The returned dict must contain exactly the eight expected coordinate keys.
        """
        statics = tmp_path / 'ocean_monthly.static.nc'
        data_nc = tmp_path / 'ocean_monthly.199301-199302.sos.nc'
        _make_mock_statics_nc(statics)
        _make_mock_data_nc(data_nc)

        import fremor.cmor_tripolar as _mod # pylint: disable=import-outside-toplevel
        import fremor.cmor_helpers as _helpers # pylint: disable=import-outside-toplevel
        import fremor.cmor_constants as _const # pylint: disable=import-outside-toplevel

        fake_archive = tmp_path / 'fake_archive'
        fake_archive_file = fake_archive / _const.CMIP7_GOLD_OCEAN_FILE_STUB
        fake_archive_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(statics), str(fake_archive_file))

        orig_archive = _const.ARCHIVE_GOLD_DATA_DIR
        orig_helpers = _helpers.ARCHIVE_GOLD_DATA_DIR
        try:
            _const.ARCHIVE_GOLD_DATA_DIR = str(fake_archive)
            _helpers.ARCHIVE_GOLD_DATA_DIR = str(fake_archive)
            _mod.ARCHIVE_GOLD_DATA_DIR = str(fake_archive)  # not imported directly, but guard

            ds = netCDF4.Dataset(str(data_nc), 'r+')
            result = load_tripolar_grid(ds=ds, netcdf_file=str(data_nc), prev_path=None)
            ds.close()
        finally:
            _const.ARCHIVE_GOLD_DATA_DIR = orig_archive
            _helpers.ARCHIVE_GOLD_DATA_DIR = orig_helpers

        expected_keys = {'lat', 'lon', 'lat_bnds', 'lon_bnds', 'yh', 'xh', 'yh_bnds', 'xh_bnds'}
        assert set(result.keys()) == expected_keys

    def test_coordinates_written_into_ds(self, tmp_path):
        """
        After calling load_tripolar_grid, ds should contain lat/lon and their bounds.
        """
        statics = tmp_path / 'ocean_monthly.static.nc'
        data_nc = tmp_path / 'ocean_monthly.199301-199302.sos.nc'
        yh_size, xh_size = 4, 5
        _make_mock_statics_nc(statics, yh_size=yh_size, xh_size=xh_size)
        _make_mock_data_nc(data_nc, yh_size=yh_size, xh_size=xh_size)

        import fremor.cmor_helpers as _helpers # pylint: disable=import-outside-toplevel
        import fremor.cmor_constants as _const # pylint: disable=import-outside-toplevel

        fake_archive = tmp_path / 'fake_archive2'
        fake_archive_file = fake_archive / _const.CMIP7_GOLD_OCEAN_FILE_STUB
        fake_archive_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(statics), str(fake_archive_file))

        orig_archive = _const.ARCHIVE_GOLD_DATA_DIR
        orig_helpers = _helpers.ARCHIVE_GOLD_DATA_DIR
        try:
            _const.ARCHIVE_GOLD_DATA_DIR = str(fake_archive)
            _helpers.ARCHIVE_GOLD_DATA_DIR = str(fake_archive)

            ds = netCDF4.Dataset(str(data_nc), 'r+')
            load_tripolar_grid(ds=ds, netcdf_file=str(data_nc), prev_path=None)

            assert 'lat' in ds.variables
            assert 'lon' in ds.variables
            assert 'lat_bnds' in ds.variables
            assert 'lon_bnds' in ds.variables
            assert 'vertex' in ds.dimensions
            assert ds.variables['lat'].shape == (yh_size, xh_size)
            assert ds.variables['lat_bnds'].shape == (yh_size, xh_size, 4)
            ds.close()
        finally:
            _const.ARCHIVE_GOLD_DATA_DIR = orig_archive
            _helpers.ARCHIVE_GOLD_DATA_DIR = orig_helpers

    def test_fallback_to_find_statics_file(self, tmp_path):
        """
        When the gold archive file is absent, load_tripolar_grid should fall back
        to find_statics_file via prev_path and still succeed.
        """
        # build a FRE-bronx-style directory layout so find_statics_file can locate the statics
        bronx_pp_dir = (tmp_path / 'USER' / 'CMIP7' / 'ESM4' / 'DEV' /
                        'ESM4.5v01_om5b04_piC' /
                        'gfdl.ncrc5-intel23-prod-openmp' / 'pp' / 'ocean_monthly')
        ts_dir = bronx_pp_dir / 'ts' / 'monthly' / '5yr'
        ts_dir.mkdir(parents=True, exist_ok=True)

        data_nc = ts_dir / 'ocean_monthly.000101-000102.sos.nc'
        statics = bronx_pp_dir / 'ocean_monthly.static.nc'

        _make_mock_statics_nc(statics)
        _make_mock_data_nc(data_nc)

        import fremor.cmor_helpers as _helpers # pylint: disable=import-outside-toplevel
        import fremor.cmor_constants as _const # pylint: disable=import-outside-toplevel

        # point ARCHIVE_GOLD_DATA_DIR at a non-existent path so gold statics is skipped
        orig_archive = _const.ARCHIVE_GOLD_DATA_DIR
        orig_helpers = _helpers.ARCHIVE_GOLD_DATA_DIR
        try:
            _const.ARCHIVE_GOLD_DATA_DIR = str(tmp_path / 'nonexistent')
            _helpers.ARCHIVE_GOLD_DATA_DIR = str(tmp_path / 'nonexistent')

            ds = netCDF4.Dataset(str(data_nc), 'r+')
            result = load_tripolar_grid(ds=ds, netcdf_file=str(data_nc), prev_path=str(data_nc))
            ds.close()
        finally:
            _const.ARCHIVE_GOLD_DATA_DIR = orig_archive
            _helpers.ARCHIVE_GOLD_DATA_DIR = orig_helpers

        assert 'lat' in result
        assert 'lon' in result

    def test_raises_file_not_found_when_no_statics(self, tmp_path):
        """
        When neither the gold archive nor the prev_path fallback can locate a
        statics file, load_tripolar_grid should raise FileNotFoundError.
        """
        data_nc = tmp_path / 'ocean_monthly.000101-000102.sos.nc'
        _make_mock_data_nc(data_nc)

        import fremor.cmor_helpers as _helpers # pylint: disable=import-outside-toplevel
        import fremor.cmor_constants as _const # pylint: disable=import-outside-toplevel

        orig_archive = _const.ARCHIVE_GOLD_DATA_DIR
        orig_helpers = _helpers.ARCHIVE_GOLD_DATA_DIR
        try:
            _const.ARCHIVE_GOLD_DATA_DIR = str(tmp_path / 'nonexistent')
            _helpers.ARCHIVE_GOLD_DATA_DIR = str(tmp_path / 'nonexistent')

            ds = netCDF4.Dataset(str(data_nc), 'r+')
            with pytest.raises(FileNotFoundError, match='statics file not found'):
                load_tripolar_grid(ds=ds, netcdf_file=str(data_nc), prev_path=None)
            ds.close()
        finally:
            _const.ARCHIVE_GOLD_DATA_DIR = orig_archive
            _helpers.ARCHIVE_GOLD_DATA_DIR = orig_helpers

    def test_raises_value_error_on_inconsistent_hq_dims(self, tmp_path):
        """
        If the statics file's q-point dimensions are not exactly hpoint+1,
        load_tripolar_grid should raise ValueError.
        """
        # data has yh=4, xh=5 but statics will have yq=3, xq=4 (wrong — should be 5, 6)
        statics = tmp_path / 'ocean_monthly.static.nc'
        data_nc = tmp_path / 'ocean_monthly.000101-000102.sos.nc'
        _make_mock_data_nc(data_nc, yh_size=4, xh_size=5)

        # deliberately mismatched q-point sizes (yq=3 instead of 5, xq=4 instead of 6)
        ds_statics = netCDF4.Dataset(str(statics), 'w')
        yh_size, xh_size = 4, 5
        bad_yq, bad_xq = 3, 4
        ds_statics.createDimension('yh', yh_size)
        ds_statics.createDimension('xh', xh_size)
        ds_statics.createDimension('yq', bad_yq)
        ds_statics.createDimension('xq', bad_xq)
        for name, dim in [('geolat', ('yh', 'xh')), ('geolon', ('yh', 'xh')),
                          ('geolat_c', ('yq', 'xq')), ('geolon_c', ('yq', 'xq'))]:
            shape = tuple(ds_statics.dimensions[d].size for d in dim)
            v = ds_statics.createVariable(name, 'f4', dim)
            v[:] = np.ones(shape)
        for name, dim in [('yh', 'yh'), ('xh', 'xh'), ('yq', 'yq'), ('xq', 'xq')]:
            v = ds_statics.createVariable(name, 'f4', (dim,))
            v[:] = np.arange(ds_statics.dimensions[dim].size, dtype='f4')
        ds_statics.close()

        import fremor.cmor_helpers as _helpers # pylint: disable=import-outside-toplevel
        import fremor.cmor_constants as _const # pylint: disable=import-outside-toplevel

        fake_archive = tmp_path / 'fake_archive3'
        fake_archive_file = fake_archive / _const.CMIP7_GOLD_OCEAN_FILE_STUB
        fake_archive_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(statics), str(fake_archive_file))

        orig_archive = _const.ARCHIVE_GOLD_DATA_DIR
        orig_helpers = _helpers.ARCHIVE_GOLD_DATA_DIR
        try:
            _const.ARCHIVE_GOLD_DATA_DIR = str(fake_archive)
            _helpers.ARCHIVE_GOLD_DATA_DIR = str(fake_archive)

            ds = netCDF4.Dataset(str(data_nc), 'r+')
            with pytest.raises(ValueError, match='hpoint_dim != qpoint_dim-1'):
                load_tripolar_grid(ds=ds, netcdf_file=str(data_nc), prev_path=None)
            ds.close()
        finally:
            _const.ARCHIVE_GOLD_DATA_DIR = orig_archive
            _helpers.ARCHIVE_GOLD_DATA_DIR = orig_helpers
