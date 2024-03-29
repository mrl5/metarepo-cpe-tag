# metarepo-cpe-tag
[![master status](https://github.com/mrl5/metarepo-cpe-tag/actions/workflows/python-app.yml/badge.svg?event=push)](https://github.com/mrl5/metarepo-cpe-tag/actions/workflows/python-app.yml)

This is an implementation of [CPE tagger] from [Funtoo Linux Optimization Proposal]s.
Main objective is to tag [Funtoo meta-repo] catpkgs with corresponding
[CPE]s.


## CVEs, CPEs, WTFs
Check this example: https://nvd.nist.gov/products/cpe/search/results?namingFormat=2.3&keyword=openssh

Notice how easy is to list all [CVE]s for given [CPE]. Using [CPE]s allows you to
have reliable [CVE] tracker for each version of a package that is present in the
repo.


## Getting started

1. Clone this repo
```bash
git clone https://github.com/mrl5/metarepo-cpe-tag/
cd metarepo-cpe-tag/
```

2. Install dependencies:

On funtoo:
```bash
emerge dev-python/click dev-python/requests dev-python/jsonschema
```
or using `pip`
```bash
# optional but recommended - use poetry or at least run in venv
pip install .[cli]
```
or [install
poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer)
and:
```bash
poetry shell
poetry install --no-dev --extras cli
```

3. Download CPE feed:
Use existing script:
```bash
./bin/get_cpe_match_feed.py ~/feeds/json
```
or do it manually:
```bash
mkdir -p ~/feeds/json && cd $_
  wget https://nvd.nist.gov/feeds/json/cpematch/1.0/nvdcpematch-1.0.json.gz &&
  cd -
```

4. See how it works:
```bash
feed=~/feeds/json/nvdcpematch-1.0.json.gz
single_input='{"name": "busybox", "versions": [{"version": "1.29.0"}, {"version": "1.29.3"}, {"version": "1.30.1"}, {"version": "1.31.0"}, {"version": "9999"}]}'
batch_input='[{"name": "busybox", "versions": [{"version": "1.29.3"}, {"version": "1.31.0"}]}, {"name":"libxml2", "versions":[{"version":"2.9.10-r5"}]}]'

export PYTHONPATH=./
./bin/tag_package_with_cpes.py --cpe-match-feed "$feed" "$single_input"
./bin/tag_package_with_cpes.py --cpe-match-feed "$feed" "$batch_input"
```

5. Come back later and update CPE feed:
```bash
./bin/get_cpe_match_feed.py ~/feeds/json
```

## get CVEs on Funtoo system (ego plugin bash PoC)
```bash
emerge app-misc/jq

export PYTHONPATH=./
./bin/get_cves_on_system.sh

ls -l dump/

cat dump/*cves.json
```


## I want to contribute/learn more technical details
Check out [CONTRIBUTING](CONTRIBUTING.md)


[Funtoo meta-repo]: https://github.com/funtoo/meta-repo
[CVE]: https://nvd.nist.gov/vuln
[CPE]: https://nvd.nist.gov/products/cpe
[CPE tagger]: https://www.funtoo.org/FLOP:CPE_tagger
[Funtoo Linux Optimization Proposal]: https://www.funtoo.org/Category:FLOP
