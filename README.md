# `fremorizer`
[![Anaconda-Server Badge](https://anaconda.org/ilaflott/fremorizer/badges/version.svg)](https://anaconda.org/ilaflott/fremorizer)
[![Anaconda-Server Badge](https://anaconda.org/ilaflott/fremorizer/badges/latest_release_date.svg)](https://anaconda.org/ilaflott/fremorizer)
[![Anaconda-Server Badge](https://anaconda.org/ilaflott/fremorizer/badges/latest_release_relative_date.svg)](https://anaconda.org/ilaflott/fremorizer)

[![publish_conda](https://github.com/ilaflott/fremorizer/actions/workflows/publish_conda.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/publish_conda.yml)
[![readthedocs](https://app.readthedocs.org/projects/fremorizer/badge/?version=latest&style=flat)](https://fremorizer.readthedocs.io/en/latest/)

[![pylint](https://github.com/ilaflott/fremorizer/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/pylint.yml)
[![pylint](https://img.shields.io/badge/pylint-%E2%89%A59.6-brightgreen)](https://github.com/NOAA-GFDL/epmt/actions/workflows/build_and_test_epmt.yml)
[![codecov](https://codecov.io/gh/ilaflott/fremorizer/branch/main/graph/badge.svg)](https://codecov.io/gh/ilaflott/fremorizer)

[![esgf_qa_check](https://github.com/ilaflott/fremorizer/actions/workflows/esgf_qa_check.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/esgf_qa_check.yml)

Simply put, `fremorizer` CMORizes FRE output with `CMOR`. 

`fremorizer` is a `conda` package, it's documentation can be found on [`readthedocs`](https://fremorizer.readthedocs.io/en/latest/).



## Background and Purpose
`fremorizer` is a model output rewriter (CMORizer) for FRE/FMS based models and output. It was originally the `fre.cmor` submodule of 
[`NOAA-GFDL/fre-cli`](https://github.com/NOAA-GFDL/fre-cli). `fremorizer` (or `fremor` for short) is geared for rewriting NOAA-GFDL 
datasets for further quality control checks, assessments and data publishing pipelines in the context of CMIP7 using the 
[`CMOR`](https://cmor.llnl.gov/) library.




## Installation / Access

### via PPAN / modules (COMING SOON/TODO)
```bash
# this will be whatever is in main of this repository (COMING SOON/TODO)
module load fremorizer/test

# this will be a tagged version of the package in this repository
module load fremorizer/YYYY.XX.[ZZ]{-alpha,-beta}
```

### From source/checkout into a virtual environment (`conda` or `venv`) with `pip`
If you're trying to develop the package, or edit the code for contributing in either a big or small way, this is for you. If you're just
trying to use `fremorizer` and you want to deal with as few technical details as possible, *this is not for you*. 

Add `-e` to the `pip` step for an editable install. `--recursive` pulls in required configuration in the form of CMIP CMOR tables, and
can be omitted if desired at the cost of local testing functionality out-of-box
```bash
# this does work, right now
git clone --recursive https://github.com/ilaflott/fremorizer.git
cd fremorizer
conda env create -f environment.yaml
pip install . 
```

### Via `conda` (COMING SOON)
If you just want an environment named `fremorizer` with the package:
```bash
# does not work yet, TODO
conda create -n fremorizer noaa-gfdl::fremorizer
conda activate fremorizer
```

or, if you've already activated a `conda` environment
```bash
# does not work yet, TODO
conda install -c noaa-gfdl fremorizer

# does not work yet, TODO
# equivalent syntax
conda install noaa-gfdl::fremorizer
```

## Usage

### as a command line interface (CLI)
The CLI entry point is `fremor`. It maps directly from the `fre cmor` subcommand:
```bash
# past fre-cli command
fre -vv -l logfile.txt cmor <COMMAND> [OPTIONS]

# fremorizer equivalent
fremor -vv -l logfile.txt <COMMAND> [OPTIONS]
```

### as a `python` module
Each CLI subcommand (`run`, `yaml`, etc.) maps to an API under under `fremor`, so the CLI functionality
is equivalently available via `import` in scripts as a proper `python` module

### Subcommands

```bash
fremor init      # Initialize CMOR configuration resources: generate template user config, fetch tables
fremor find      # Find and print variables in MIP tables according to your variable lists or other input
fremor varlist   # Create a simple variable list of netCDF files in a directory
fremor config    # Generate a basic CMOR YAML configuration from a pp directory tree
fremor yaml      # Bulk routine for processing data based on a CMOR YAML config, calls fremor run many times
fremor run       # Lowest-level routine, no CMOR YAML needed, rewrites output files in a directory with CMOR
```

For a concise overview of required inputs and sample commands, see the
[CMOR Quickstart](docs/quickstart.rst).

### Getting Started: Initialize CMOR Resources

Before CMORizing data, you need an experiment configuration template and MIP tables.
The `fremor init` command helps set up these resources:

```bash
# Generate a CMIP6 experiment config template and fetch CMIP6 tables
fremor init -m cmip6 -e exp_config.json -t cmip6-tables

# Generate a CMIP7 experiment config template and fetch CMIP7 tables (fast mode)
fremor init -m cmip7 -e exp_config.json -t cmip7-tables --fast

# Fetch tables for a specific release tag
fremor init -m cmip6 -t cmip6-tables --tag 6.9.33
```

This command:
- Generates an experiment configuration JSON template with required CMIP metadata fields
- Fetches official MIP tables from trusted GitHub repositories (CMIP6: `pcmdi/cmip6-cmor-tables`, CMIP7: `WCRP-CMIP/cmip7-cmor-tables`)
- Supports both `git clone` (default) and `curl` (`--fast`) methods for downloading official configurations

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

- `python>=3.11`
- `click>=8.2`
- `cmor>=3.14.2`
- `netCDF4>=1.7`
- `numpy>=2`
- `pyyaml`

For development and testing, `pylint`, `pytest`, and `pytest-cov` are all highly recommended as helpful additions.

## Development

```bash
# Checkout code
git clone --recursive https://github.com/ilaflott/fremorizer.git
cd fremorizer

# Create a conda environment
conda env create -f environment.yaml
conda activate fremorizer

# Install in editable mode
pip install -e .

# Run tests
pytest fremorizer/tests/

# Run linter
pylint --rcfile pylintrc fremorizer/
```

## Quality Assurance

The repository includes automated quality assurance (QA) checks to validate that CMORized outputs meet CMIP6 standards:

### ESGF-QA Validation

The `esgf_qa_check` workflow runs [ESGF-QA](https://github.com/ESGF/esgf-qa) on test outputs to verify CF compliance and CMIP6 metadata standards. This separate pipeline:

- Runs automatically on pushes and pull requests
- Executes unit tests to generate CMORized output files
- Validates outputs using ESGF-QA with CF compliance checks
- Uploads QA results as workflow artifacts (retained for 30 days)

To view QA results from a workflow run:
1. Navigate to the Actions tab in GitHub
2. Select the `esgf_qa_check` workflow run
3. Download the `esgf-qa-results` artifact
4. View results using the ESGF-QA viewer or web interface

## Relationship to fre-cli
### WCRP Compliance Checking

[![wcrp_compliance_check](https://github.com/ilaflott/fremorizer/actions/workflows/wcrp_compliance_check.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/wcrp_compliance_check.yml)

The `wcrp_compliance_check` workflow validates CMORized NetCDF outputs against WCRP project
specifications using [cc-plugin-wcrp](https://github.com/ESGF/cc-plugin-wcrp), a plugin for
the [IOOS compliance-checker](https://github.com/ioos/compliance-checker). This pipeline:

- Runs automatically on pull requests and via manual dispatch
- Executes unit tests to generate CMORized output files
- Gathers and categorizes outputs by CMIP version (CMIP6, CMIP7)
- Validates outputs using the `wcrp_cmip6` compliance checker
- Uploads compliance reports as workflow artifacts (retained for 30 days)

To view compliance results from a workflow/CI run:
1. Navigate to the Actions tab in GitHub
2. Select the `wcrp_compliance_check` workflow run
3. Download the `wcrp-compliance-reports` artifact

### pipeline badges

| Python 3.11 | Python 3.12 | Python 3.13 | Python 3.14 |
|-------------|-------------|-------------|-------------|
| [![3.11](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.11) | [![3.12](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.12) | [![3.13](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.13) | [![3.14](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.14) |

## License

Apache License 2.0 — see [LICENSE.md](LICENSE.md)

## Conda-forge feedstock

See `CONDA_FORGE_FEEDSTOCK_PLAN.md` for the steps and follow-up tasks to submit and maintain the conda-forge feedstock for `fremorizer`.

## Releases and Versioning

`fremorizer` uses a post-release scheme to identify development beyond the latest tagged version and tie the current `main` branch to a
`conda` package versioned as `develop`. To avoid confusion with `fre-workflows` and `fre-cli`, which often demand that the version tags 
match, `fremorizer`'s version format is `X.Y.Z[.post]`. 

### new published release procedure 

To publish new release carefully follow the below procedure:
1. create a new branch off of `main`, which is already published to `conda` under `develop`/the previous tagged version + `.post`
2. edit the version number in `fremorizer/_version.py` from the current one, to the desired version tag, remove `.post`, then open a PR. edit nothing else (usually).
3. confirm the branch is functional by letting workflows finish, if you see green checks only, proceed. otherwise, stop and debug.
4. draft a new release pointing to the PR branch, click release. the publishing workflow should trigger and finish, and you should see the `X.Y.Z` version in the conda channel.
5. *releases in this repository are immutable*, **so even if the release workflow fails, breathe and move on to the next step.**
6. edit the version number in `fremorizer/_version.py` to `X.Y.Z.post`, and merge the PR to main workflow steps passed. **`publish_conda`** will trigger again and upload what is in `main` under the `conda` version `develop` and `pip` version `X.Y.Z.post`
