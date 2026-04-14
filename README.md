<!-- [![Anaconda-Server Badge](https://anaconda.org/noaa-gfdl/fremorizer/badges/version.svg)](https://anaconda.org/noaa-gfdl/fremorizer)
[![Anaconda-Server Badge](https://anaconda.org/noaa-gfdl/fremorizer/badges/latest_release_date.svg)](https://anaconda.org/noaa-gfdl/fremorizer)
[![Anaconda-Server Badge](https://anaconda.org/noaa-gfdl/fremorizer/badges/latest_release_relative_date.svg)](https://anaconda.org/noaa-gfdl/fremorizer)
-->

# fremorizer

[![build_conda](https://github.com/ilaflott/fremorizer/actions/workflows/build_conda.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/build_conda.yml)
[![create_test_conda_env](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml)
[![publish_conda](https://github.com/ilaflott/fremorizer/actions/workflows/publish_conda.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/publish_conda.yml)

[![pylint](https://github.com/ilaflott/fremorizer/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/pylint.yml)
[![pylint](https://img.shields.io/badge/pylint-%E2%89%A59.4-brightgreen)](https://github.com/NOAA-GFDL/epmt/actions/workflows/build_and_test_epmt.yml)

[![codecov](https://codecov.io/gh/ilaflott/fremorizer/branch/main/graph/badge.svg)](https://codecov.io/gh/ilaflott/fremorizer)
[![readthedocs](https://app.readthedocs.org/projects/fremorizer/badge/?version=latest&style=flat)](https://fremorizer.readthedocs.io/en/latest/)

| Workflow | Python 3.9 | Python 3.10 | Python 3.11 |
|----------|------------|-------------|------------|
| **create_test_conda_env** | [![3.9](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.9) | [![3.10](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.10) | [![3.11](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.11) |

[![compliance_check](https://github.com/ilaflott/fremorizer/actions/workflows/compliance_check.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/compliance_check.yml)

Model output rewriter (CMORizer) for FRE/FMS based models.

`fremorizer` is an independent package extracted from the `fre.cmor` submodule of
[fre-cli](https://github.com/NOAA-GFDL/fre-cli). It rewrites climate model output
files with CMIP-compliant metadata for downstream publishing using the
[CMOR](https://cmor.llnl.gov/) library.

## Installation

### Via pip
```bash
pip install fremorizer
```

### Via conda
```bash
conda install -c noaa-gfdl -c conda-forge fremorizer
```

### From source
```bash
git clone https://github.com/ilaflott/fremorizer.git
cd fremorizer
pip install .
```

## Usage

The CLI entry point is `fremor`. It maps directly from the `fre cmor` subcommand:

```
# fre-cli equivalent:       fre -vv -l logfile.txt cmor run [OPTIONS]
# fremorizer equivalent:    fremor -vv -l logfile.txt run [OPTIONS]
```

### Subcommands

```bash
fremor run       # Rewrite climate model output files with CMIP-compliant metadata
fremor yaml      # Process a CMOR YAML configuration file
fremor find      # Find variables in MIP tables
fremor varlist   # Create a simple variable list from netCDF files
fremor config    # Generate a CMOR YAML configuration from a pp directory tree
```

For a concise overview of required inputs and sample commands, see the
[CMOR Quickstart](docs/quickstart.rst).

### Verbosity and Logging

```bash
fremor -v run ...        # INFO level logging
fremor -vv run ...       # DEBUG level logging
fremor -q run ...        # ERROR level only (quiet)
fremor -l log.txt run ...  # Log to file (appends)
```

### Example: CMORize ocean data

```bash
fremor run \
    -d /path/to/input/netcdf/dir \
    -l /path/to/varlist.json \
    -r /path/to/CMIP6_Omon.json \
    -p /path/to/exp_config.json \
    -o /path/to/output/dir
```

## Requirements

- Python >= 3.11
- cftime
- click
- cmor
- netCDF4
- numpy
- pyyaml

## Development

```bash
# Create conda environment
conda env create -f environment.yaml
conda activate fremorizer

# Install in editable mode
pip install -e .

# Run tests
pytest fremorizer/tests/ -v

# Run linter
pylint --rcfile pylintrc fremorizer/
```

## Relationship to fre-cli

`fremorizer` is a near-exact copy of the `fre.cmor` submodule from
[NOAA-GFDL/fre-cli](https://github.com/NOAA-GFDL/fre-cli), extracted as an
independent package. The `fremor yaml` subcommand optionally depends on
`fre-cli`'s `yamltools` module for YAML consolidation.

## License

Apache License 2.0 — see [LICENSE.md](LICENSE.md)

## Conda-forge feedstock

See `CONDA_FORGE_FEEDSTOCK_PLAN.md` for the steps and follow-up tasks to submit and maintain the conda-forge feedstock for `fremorizer`.
