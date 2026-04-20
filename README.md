# `fremorizer`
`fremorizer` CMORizes FRE output with `CMOR`. It is a `conda` package and it's documentation can be found on
[`readthedocs`](https://fremorizer.readthedocs.io/en/latest/).

[![Anaconda-Server Badge](https://anaconda.org/ilaflott/fremorizer/badges/version.svg)](https://anaconda.org/ilaflott/fremorizer)
[![Anaconda-Server Badge](https://anaconda.org/ilaflott/fremorizer/badges/latest_release_date.svg)](https://anaconda.org/ilaflott/fremorizer)
[![Anaconda-Server Badge](https://anaconda.org/ilaflott/fremorizer/badges/latest_release_relative_date.svg)](https://anaconda.org/ilaflott/fremorizer)

[![publish_conda](https://github.com/ilaflott/fremorizer/actions/workflows/publish_conda.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/publish_conda.yml)
[![readthedocs](https://app.readthedocs.org/projects/fremorizer/badge/?version=latest&style=flat)](https://fremorizer.readthedocs.io/en/latest/)

[![pylint](https://github.com/ilaflott/fremorizer/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/ilaflott/fremorizer/actions/workflows/pylint.yml)
[![pylint](https://img.shields.io/badge/pylint-%E2%89%A59.7-brightgreen)](https://github.com/NOAA-GFDL/epmt/actions/workflows/build_and_test_epmt.yml)
[![codecov](https://codecov.io/gh/ilaflott/fremorizer/branch/main/graph/badge.svg)](https://codecov.io/gh/ilaflott/fremorizer)


## Background and Purpose
`fremorizer` is a model output rewriter (CMORizer) for FRE/FMS based models and output. It was originally the `fre.cmor`
submodule of [`NOAA-GFDL/fre-cli`](https://github.com/NOAA-GFDL/fre-cli). `fremorizer` (or `fremor` for short) is geared
for rewriting NOAA-GFDL datasets for further quality control checks, assessments and data publishing pipelines in the
context of CMIP7 using the [`CMOR`](https://cmor.llnl.gov/) library.



## Installation / Access


### Requirements

- `python>=3.11`
- `click>=8.2`
- `cmor>=3.14.2`
- `netCDF4>=1.7`
- `numpy>=2`
- `pyyaml`

For development and testing, `pylint`, `pytest`, and `pytest-cov` are all highly recommended as helpful additions.


### via PPAN / modules (COMING SOON/TODO)
If you're trying to gain access to `fremor` functionality as quickly as possible:
```bash
# the current post-release in main
module load fremorizer/test

# a tagged version of fremorizer, post-releases will never be named modules
module load fremorizer/X.Y.Z
```


### via `conda`
If you have a path to a `fremorizer` environment you can activate it like so:
```bash
conda activate some/path/to/fremorizer_env
```

If you want your own `fremorizer` environment:
```bash
# the environment will be named fremorizer_en
conda create -n fremorizer_env ilaflott::fremorizer

# see fremorizer_env in the list --> activate it by name
conda env list
conda activate fremorizer_env
```

or, if you've already activated a `conda` environment
```bash
conda create -n empty_env
conda activate empty_env
conda install -c ilaflott fremorizer

# equivalent syntax
conda install ilaflott::fremorizer
```


### `pip` install source/checkout into a virtual environment (`conda`/`venv`)
If you're trying to develop `fremorizer` capabilities, or edit the code to your liking in either a big or small way,
**this is for you**. This checks out the code, creates and activates an environment, installs into the environment,
and runs all unit-tests and `pylint` checks:
```bash
# omit --recursive if you don't want tables as submodules
git clone --recursive https://github.com/ilaflott/fremorizer.git
cd fremorizer

# create an environment and install the local checkout
conda env create -f environment.yaml
conda actiavte fremorizer
pip install -e . 

# Run tests
pytest fremorizer/tests/

# Run linter
pylint --rcfile pylintrc fremorizer/
```



## Usage


### as a command line interface (CLI)
The CLI entry point is `fremor`, currently a suite of (currently) six routines for facillitating data preparation for
CMIP7. 
```bash
# The full list of subcommands
fremor init      # Initialize CMOR configuration resources: generate template user config, fetch tables
fremor find      # Find and print variables in MIP tables according to your variable lists or other input
fremor varlist   # Create a simple variable list of netCDF files in a directory
fremor config    # Generate a basic CMOR YAML configuration from a pp directory tree
fremor yaml      # Bulk routine for processing data based on a CMOR YAML config, calls fremor run many times
fremor run       # Lowest-level routine, no CMOR YAML needed, rewrites output files in a directory with CMOR
```

The CLI offers full logging and verbosity control independent of the command chosen:
```bash
# verbosity and logging
fremor -v  ...          # INFO level logging
fremor -vv ...          # DEBUG level logging
fremor -q  ...          # ERROR level only (quiet)
fremor -l mylog.txt ... # Log to file (appends)
```

If you've used the previous `fre cmor` command, there is a direct mapping of syntax:
```bash
# past fre-cli command
fre -vv -l logfile.txt cmor <COMMAND> [OPTIONS]

# fremorizer equivalent
fremor -vv -l logfile.txt <COMMAND> [OPTIONS]
```


### as a `python` module
Each CLI subcommand (`run`, `yaml`, etc.) maps to an API under under `fremor`, so the CLI functionality
is equivalently available via `import` in scripts as a proper `python` module



## Getting started
For an overview of required inputs and sample commands, see the [CMOR Quickstart](docs/quickstart.rst).



## CI/CD Workflows and QA


### WCRP Compliance Checking (under development)

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


### `conda` environment tests

| Python 3.11 | Python 3.12 | Python 3.13 | Python 3.14 |
|-------------|-------------|-------------|-------------|
| [![3.11](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.11) | [![3.12](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.12) | [![3.13](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.13) | [![3.14](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/ilaflott/fremorizer/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.14) |



## License
Apache License 2.0 — see [LICENSE.md](LICENSE.md)



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
