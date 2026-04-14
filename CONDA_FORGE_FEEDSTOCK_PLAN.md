# conda-forge feedstock plan

This document captures the steps needed to publish `fremorizer` on conda-forge and keep the feedstock healthy.

## Preconditions
- Cut a tagged release (sdist/wheel) that matches `meta.yaml`'s version (e.g., `2026.01.alpha1`) and host it on GitHub releases or PyPI so staged-recipes can fetch an immutable tarball.
- Ensure `LICENSE.md` is included in the sdist; conda-forge recipes must declare `license_file`.
- Verify all runtime deps are present on conda-forge: `cmor`, `netcdf4`, `cftime`, `click`, `numpy`, `pyyaml`, and Python >=3.11. If any are missing/outdated, submit/refresh those first.
- Keep the recipe `noarch: python` while the code remains pure-Python; drop it only if compiled extensions are added later.

## Recipe expectations for conda-forge
- `build`: `noarch: python`, `number: 0`, `script: "{{ PYTHON }} -m pip install . -vv --no-deps"`.
- `requirements` (host/run): `python >=3.11`, `pip`, and the runtime deps above sourced from conda-forge (no extra channels).
- `test`: prefer fast checks such as `python -c "import fremorizer"` and `fremor --help`; avoid data-heavy integration runs.
- `about`: include `home`, `summary`, `license`, and `license_file: LICENSE.md`.
- `extra`: add `recipe-maintainers` (at minimum `ilaflott`; add others who will triage feedstock PRs).

## Execution plan (staged-recipes → feedstock)
1) Sync `meta.yaml` with the release version and recipe expectations above; compute the source tarball SHA256.
2) Open a PR to `conda-forge/staged-recipes` with the recipe, limiting channels to conda-forge and using strict channel priority.
3) Respond to review (lint from `conda-smithy`/`conda-forge-ci-setup`); adjust tests or pins as requested.
4) After merge, watch the new feedstock repo; rerender with `conda-smithy rerender` if needed and enable automerge for patch bumps.
5) Document the release cadence so maintainers know when to rerender or accept `regro-cf-autotick-bot` version bumps.

## Issues to open
- Track release packaging: ensure sdists/wheels include `LICENSE.md` and match the recipe version.
- Track staged-recipes submission: PR prep with SHA256, maintainer list, and minimal tests.
- Track feedstock bootstrap: rerendering, enabling automerge, and setting maintainer expectations.

## Tagging
Tag @ilaflott and @Codex (agent) on the staged-recipes PR and follow-up feedstock issues to keep reviewers and automation in the loop.
