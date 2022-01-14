# For contributors

Please use classic `forking flow` model which is nicely described here:
https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow


## TL;DR:
0. create an issue (with nice description *por favor*)
1. fork the repo and `git clone` your fork
2. install dev dependencies
```
pip install -e .[dev]
```
3. then create your own branch (e.g. `issue-X` or `bugfix/issue-X`):
```
git checkout -b issue-X
```
4. after changes do the PR into the `master` branch


## Codestyle
1. [black](https://pypi.org/project/black/)
2. [isort](https://pypi.org/project/isort/)
