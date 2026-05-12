# `fremor`
`fremor` CMORizes FRE output with `CMOR`. It is a `conda` package and it's documentation can be found on
[`readthedocs`](https://fremor.readthedocs.io/en/latest/).

[![Build conda package](https://github.com/conda-forge/fremor-feedstock/actions/workflows/conda-build.yml/badge.svg?branch=main)](https://github.com/conda-forge/fremor-feedstock/actions/workflows/conda-build.yml)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/fremor/badges/version.svg)](https://anaconda.org/conda-forge/fremor)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/fremor/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/fremor)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/fremor/badges/latest_release_relative_date.svg)](https://anaconda.org/conda-forge/fremor)

[![pylint](https://img.shields.io/badge/pylint-%E2%89%A59.7-brightgreen)](https://github.com/NOAA-GFDL/fremor/actions/workflows/pylint.yml)
[![codecov](https://codecov.io/gh/NOAA-GFDL/fremor/branch/main/graph/badge.svg)](https://codecov.io/gh/NOAA-GFDL/fremor)

[![publish_pip](https://github.com/NOAA-GFDL/fremor/actions/workflows/publish_pip.yml/badge.svg)](https://github.com/NOAA-GFDL/fremor/actions/workflows/publish_pip.yml)
[![readthedocs](https://app.readthedocs.org/projects/fremor/badge/?version=latest&style=flat)](https://fremor.readthedocs.io/en/latest/)
[![pylint](https://github.com/NOAA-GFDL/fremor/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/NOAA-GFDL/fremor/actions/workflows/pylint.yml)

`python3.11`:[![3.11](https://github.com/NOAA-GFDL/fremor/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/NOAA-GFDL/fremor/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.11)

`python3.12`:[![3.12](https://github.com/NOAA-GFDL/fremor/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/NOAA-GFDL/fremor/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.12)

`python3.13`:[![3.13](https://github.com/NOAA-GFDL/fremor/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/NOAA-GFDL/fremor/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.13)

`python3.14`:[![3.14](https://github.com/NOAA-GFDL/fremor/actions/workflows/create_test_conda_env.yml/badge.svg)](https://github.com/NOAA-GFDL/fremor/actions/workflows/create_test_conda_env.yml?query=branch%3Amain+python-version%3A3.14)

#### License
Apache License 2.0 — see [LICENSE.md](LICENSE.md)


## Background and Purpose
`fremor` is a model output rewriter (CMORizer) for FRE/FMS based models and output. It is specifically geared for standardizing 
NOAA-GFDL datasets for further quality control checks, assessments and data publishing pipelines in the context of CMIP7 
using the [`CMOR`](https://cmor.llnl.gov/) library.


### Relationship to `fre-cli`
`fremor` was originally the `fre.cmor` submodule of [`NOAA-GFDL/fre-cli`](https://github.com/NOAA-GFDL/fre-cli) and so stands
on the shoulders of it's contributors, retaining it's general structure and lessons learned from it. Future re-integrations 
back into `fre-cli`, as a formal package dependency, are being assessed.





### Contributors
[![Contributors](https://contrib.rocks/image?repo=NOAA-GFDL/fremor)](https://github.com/NOAA-GFDL/fremor/graphs/contributors)

#### AI Disclaimer
AI was heavily used in the creation of this repository, primarily `github`'s `copilot` with `Claude` (`opus4.6`, `sonnet4.6`, 
and `haiku`), and `Gemini` and `Chat-GPT` models to a lesser extent, in agent mode. `Claude` and `Codex` agents have also 
contributed.




## Quickstart
For an overview of required inputs and sample commands, see the [CMOR Quickstart](docs/quickstart.rst).



## Installation / Access

### Requirements

- `python>=3.11`
- `click>=8.2`
- `cmor>=3.15.0`
- `netCDF4>=1.7`
- `numpy>=2`
- `pyyaml`

For development and testing, `pylint`, `pytest`, and `pytest-cov` are all highly recommended as helpful additions.



### via PPAN / modules (COMING SOON/TODO)
If you're trying to gain access to `fremor` functionality as quickly as possible:
```bash
# the current post-release in main
module load fremor/test

# a tagged version of fremor, post-releases will never be named modules
module load fremor/X.Y.Z
```


### via `conda` and/or `conda-forge`
If you have a path to a `fremor` environment you can activate it like so:
```bash
conda activate some/path/to/fremor_env
```

If you want your own `fremor` environment:
```bash
# the environment will be named fremor_en
conda create -n fremor_env conda-forge::fremor

# see fremor_env in the list --> activate it by name
conda env list
conda activate fremor_env
```

or, if you've already activated a `conda` environment
```bash
conda create -n empty_env
conda activate empty_env
conda install -c conda-forge fremor

# equivalent syntax
conda install conda-forge::fremor
```


### `pip` install source/checkout into a virtual environment (`conda`/`venv`)
If you're trying to develop `fremor` capabilities, or edit the code to your liking in either a big or small way,
**this is for you**. This checks out the code, creates and activates an environment, installs into the environment,
and runs all unit-tests and `pylint` checks:
```bash
# omit --recursive if you don't want tables as submodules
git clone --recursive https://github.com/NOAA-GFDL/fremor.git
cd fremor

# create an environment and install the local checkout
conda env create -f environment.yaml
conda activate fremor
pip install -e . 

# Run tests
pytest fremor/tests/

# Run linter
pylint --rcfile pylintrc fremor/
```



## Usage


### as a command line interface (CLI)
The CLI entry point is `fremor`, currently a suite of (currently) six routines for facilitating data preparation for
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

# fremor equivalent
fremor -vv -l logfile.txt <COMMAND> [OPTIONS]
```


### as a `python` module
Each CLI subcommand (`run`, `yaml`, etc.) maps to an API under under `fremor`, so the CLI functionality
is equivalently available via `import` in scripts as a proper `python` module




## CI/CD Workflows and QA


### WCRP Compliance Checking (under development)

[![wcrp_compliance_check](https://github.com/NOAA-GFDL/fremor/actions/workflows/wcrp_compliance_check.yml/badge.svg?branch=main)](https://github.com/NOAA-GFDL/fremor/actions/workflows/wcrp_compliance_check.yml)

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





## Versioning and tags
`fremor` uses a post-release scheme to identify development beyond the latest tagged version. To avoid confusion 
with `fre-workflows` and `fre-cli`, which often demand that the version tags match, `fremor`'s version format is 
`X.Y.Z[.post]`. 




## New Release Procedure 
This procedure is being actively tested and checked now, and may change in the future. Document any deviations 
taken from this guide!

To publish new release, cease merging new PRs to `main`, and carefully follow the below procedure:


### first, create a new tag for release
1. create a new branch off of `main`, which should be the previous tagged version + `.post`, *give it a name
   different than the exact tag you are creating*
3. edit the version number in `fremor/_version.py` from the current one, to the desired version tag, remove
   `.post`, then open a PR to `main` in this repository.
5. confirm the branch is functional by letting workflows finish, if you see green checks only, proceed. otherwise,
   stop and debug.
7. at this point, light clean up style edits are OK, but functional edits are not. Do so until happy and keep the
   checks passing.
9. now create the tag from the branch at this point locally in your terminal with `git tag X.Y.Z;`


### second, publish release to PyPI, then github, in that order
WARNING: *any problems or mistakes after the next step are irreversible due to package immutability so make sure 
things are working before continuing*

6. now push your tag you created locally with `git checkout X.Y.Z; git push origin HEAD:refs/tags/X.Y.Z`
7. workflow checks are triggered by the new push to the new tag `X.Y.Z`, and one of the workflows will to publish
   the built package to `PyPI`, check the actions tab
9. on github, create a new release from the new tag, generate release notes automatically comparing to the previous
   tag, and upload the built `X.Y.Z` package downloaded from `PyPI` *you cannot do this later due to immutability
   of releases*


### third, publish release to `conda-forge` via `fremor-feedstock` fork
10. use (create if needed) a fork (e.g. https://github.com/ilaflott/fremor-feedstock) to create a new branch called
    `fremorX.Y.Z`, e.g. https://github.com/ilaflott/fremor-feedstock/tree/fremor0.9.3
11. adjust the version to `X.Y.Z` and update the `sha256` to what it says on PyPI in `recipe.yaml`
12. open a PR to the `conda-forge/fremor-feedstock` e.g. https://github.com/conda-forge/fremor-feedstock/pull/3
13. once checks pass, a reviewer with access to `conda-forge/fremor-feedstock` can approve and merge, kicking off the
    rest of the publishing pipeline to `conda-forge`


### wrap-up
14. back to the `fremor` PR we opened intially.
15. edit the version number in `fremor/_version.py` to `X.Y.Z.post`, let the checks pass
16. merge the PR branch you used for creating the release to `main`

what a published release on PyPI looks like: https://pypi.org/project/fremor/0.9.3/#fremor-0.9.3.tar.gz

what a published PyPI package on github looks like: https://github.com/NOAA-GFDL/fremor/releases/tag/0.9.3

what a published PyPI package on `conda-forge` looks like: https://anaconda.org/channels/conda-forge/packages/fremor/files
