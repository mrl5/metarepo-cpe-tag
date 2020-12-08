# metarepo-cpe-tag
This is an implementation of [CPE tagger] from [Funtoo Linux Optimization Proposal]s.
Main objective is to tag [Funtoo meta-repo] catpkgs with corresponding
[CPE]s.


## CVEs, CPEs, WTFs

Check this example: https://nvd.nist.gov/products/cpe/search/results?namingFormat=2.3&keyword=openssh

Notice how easy is to list all [CVE]s for given [CPE]. Using [CPE]s allows you to
have reliable [CVE] tracker for each version of a package that is present in the
repo use [CPE].


## Getting started
1. init repo
```
make sync
```
2. Create python3 virtualenv:
```
VENV_DIR="$HOME/.my_virtualenvs/metarepo_cpe_tag"
mkdir -p "${VENV_DIR}"
python3 -m venv "${VENV_DIR}"
```
3. Switch to new virtualenv:
```
source "${VENV_DIR}/bin/activate"
```
4. Install requirements:
```
python3 setup.py install
```
5. **Export PYTHONPATH**:
```
export PYTHONPATH=./:./modules/metarepo-to-json
```


## I want to contribute/learn more technical details
Check out [CONTRIBUTING](CONTRIBUTING.md)


[Funtoo meta-repo]: https://github.com/funtoo/meta-repo
[CVE]: https://nvd.nist.gov/vuln
[CPE]: https://nvd.nist.gov/products/cpe
[CPE tagger]: https://www.funtoo.org/FLOP:CPE_tagger
[Funtoo Linux Optimization Proposal]: https://www.funtoo.org/Category:FLOP
