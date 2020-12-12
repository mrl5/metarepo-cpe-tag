# For contributors
This project uses **P**lugin **O**riented **P**rogramming paradigm by
incorporating [SaltStack pop library]

I decided to use classic `forking flow` model which is nicely described here:
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


## HUBs, POPs, WTF?
0. [my pop framework fairytale](https://github.com/mrl5/private-wiki/blob/master/pop-framework-fairy-tale.md)
1. `pop` book: https://pop-book.readthedocs.io/en/latest/
2. `pop` tutorial: https://pop.readthedocs.io/en/latest/tutorial/quickstart.html
3. `pop-config`: https://pop-config.readthedocs.io/en/latest/topics/quickstart.html#the-config-dictionary
4. `pop` patterns: https://pop.readthedocs.io/en/latest/topics/sub_patterns.html


[SaltStack pop library]: https://gitlab.com/saltstack/pop/pop
