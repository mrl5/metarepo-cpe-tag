# metarepo-cpe-tag
This is an implementation of [CPE tagger] from [Funtoo Linux Optimization Proposal]s.
Main objective is to tag [Funtoo meta-repo] catpkgs with corresponding
[CPE]s.


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
[CPE]: https://nvd.nist.gov/products/cpe
[CPE tagger]: https://www.funtoo.org/FLOP:CPE_tagger
[Funtoo Linux Optimization Proposal]: https://www.funtoo.org/Category:FLOP
