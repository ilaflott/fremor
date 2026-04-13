## Release Versioning Procedure

## Checklist
### fremorizer changes
* [ ] 1. Verify that git submodules in fremorizer reflect the latest state (or certain commit/tag) of the upstream repositories.

    - If not, consult the manager of the upstream repository and determine whether the update should be included in this release.
    - If so, ask the sub-project maintainer to tag the upstream repository

    Open a PR to commit the submodule updates in `fremorizer`, solicit a review, and merge the PR.

    - **Submodules**:
        - `fremorizer/tests/test_files/cmip6-cmor-tables`
        - `fremorizer/tests/test_files/cmip7-cmor-tables`

    **Note**: The release schedules of these submodules may vary from that of fremorizer

* [ ] 2. Create a tag in the fremorizer repository (testing tag or release tag)

    Locally this can be done with:

    ```
    git tag -a <release>
    git push origin <tag name>
    ```

    - For the *testing tags*, follow the structure: `[year].[major].[minor].[testing tag]`

        - `[year].[major].[minor].alpha[iteration]`: alpha tags include major code breaking changes
        - `[year].[major].[minor].beta[iteration]`: beta tags include releases candidates for testing

    - For the *full release tag*, follow the structure: `[year].[major].[minor]`

    After the tag is pushed, CI will trigger the creation of a PR changing any reference to the previous tag with the new tag.
    Verify the tagged release is present [here](https://github.com/ilaflott/fremorizer/releases>)

* [ ] 3. For a full release (only), create the github release associated with the correct tag and generate the release notes.

    - In the release notes, be sure to link any alpha and beta tags that were tested for the release

* [ ] 4. Navigate to [noaa-gfdl conda channel](https://anaconda.org/NOAA-GFDL/fremorizer) and verify that the last upload date corresponds to the date of this release and that the release number is correct.
