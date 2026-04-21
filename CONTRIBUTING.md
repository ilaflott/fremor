## **For Developers**

* Developers are free to use this repository's `README.md` to familiarize with the CLI and save time from having to install any dependencies, but development within a Conda environment is heavily recommended regardless
* Gain access to the repository with `git clone --recursive git@github.com:ilaflott/fremorizer.git` or your fork's link (recommended) and an SSH RSA key
    - Once inside the repository, developers can test local changes by running a `pip install .` inside of the root directory after activating a virtual environment, installing the fremorizer package locally with the newest local changes on top of the installed Conda fremorizer dependencies. the `-e` flag can be used for an editable installation
    - Test as a normal user would use the CLI
* Create a GitHub issue to reflect your contribution's background and reference it with Git commits

### **Opening Pull Requests and Issues**
Please use one of the templates present in this repository to open a PR or an issue, and fill out the template to the best of your ability.
With few exceptions, pull requests always require an issue.

### **Adding Tools From Other Repositories**

* Currently, the solution to this task is to approach it using Conda packages. The tool that is being added must reside within a repository that contains a meta.yaml that includes Conda dependencies like the one in this repository and ideally a setup.py (may be subject to change due to deprecation) that may include any potentially needed pip dependencies
    - Once published as a Conda package, ideally on the [NOAA-GFDL channel](https://anaconda.org/NOAA-GFDL), an addition can be made to the "run" section under the "requirements" category in the meta.yaml of the fremorizer following the syntax `channel::package`
    - On pushes to the main branch, the [package](https://anaconda.org/ilaflott/fremorizer) will automatically be updated using the workflow file
 
### **MANIFEST.in**

* In the case where non-python files like templates, examples, and outputs are to be included in the fremorizer package, MANIFEST.in can provide the solution. Ensure that the file exists within the correct folder, and add a line to the MANIFEST.in following [this syntax](https://setuptools.pypa.io/en/latest/userguide/miscellaneous.html)

