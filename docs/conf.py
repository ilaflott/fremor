# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
import datetime as dt
from pathlib import Path

sys.path.insert(0, str(Path('..').resolve()))

from fremorizer import __version__ as pkg_version

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'fremorizer'
copyright = f'{dt.datetime.now().year}, NOAA-GFDL MSD Workflow Team'
author = 'NOAA-GFDL MSD Workflow Team'
release = pkg_version   # type: ignore

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = ['sphinx.ext.autodoc']
exclude_patterns = []

# Mock imports for dependencies not needed during doc build
# This allows Sphinx to build docs without installing heavy dependencies
autodoc_mock_imports = [
    'cftime',
    'cmor',
    'netCDF4',
    'numpy',
    'xarray',
    'pandas',
    'pytest',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'renku'
