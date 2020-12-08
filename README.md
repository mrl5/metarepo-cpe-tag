# metarepo-cpe-tag
This is an implementation of [CPE tagger] from [Funtoo Linux Optimization Proposal]s.
Main objective is to tag [Funtoo meta-repo] catpkgs with corresponding
[CPE]s.


## CVEs, CPEs, WTFs
Check this example: https://nvd.nist.gov/products/cpe/search/results?namingFormat=2.3&keyword=openssh

Notice how easy is to list all [CVE]s for given [CPE]. Using [CPE]s allows you to
have reliable [CVE] tracker for each version of a package that is present in the
repo.


## Getting started
1. Create python3 virtualenv:
```
VENV_DIR="$HOME/.my_virtualenvs/metarepo_cpe_tag"
mkdir -p "${VENV_DIR}"
python3 -m venv "${VENV_DIR}"
```
2. Switch to new virtualenv:
```
source "${VENV_DIR}/bin/activate"
```
3. Install requirements:
```
python3 setup.py install
```
4. Download CPE feed:
```
mkdir -p ~/feeds/json && cd $_
  wget https://nvd.nist.gov/feeds/json/cpematch/1.0/nvdcpematch-1.0.json.gz &&
  cd -
```
5. See how it works:
```
input='{"name": "busybox", "versions": [{"version": "1.29.0"}, {"version": "1.29.3"}, {"version": "1.30.1"}, {"version": "1.31.0"}, {"version": "9999"}]}'

export PYTHONPATH=./
./bin/tag_package_with_cpes.py --package-json "$input"
```
6. Get metarepo2json plugin and export meta-repo to json:
```
make sync &&
  cd modules/metarepo-to-json/ &&
  python3 setup.py install &&
  cd -

export PYTHONPATH=./:./modules/metarepo-to-json
./bin/export_metarepo_to_json.py
```
7. install GNU parallel to make it faster:
```
emerge -av sys-process/parallel
```
8. generate tags for each package in kit
```
metarepodir=~/metarepo_dump
kit=core-kit
kitdir=$metarepodir/$kit
parallel_jobs=8

rm -f $kitdir/*.tagged \
    $kitdir/*.err
for catpkgs in `ls $kitdir`; do
    echo tagging [$kit] $catpkgs ...
    cat $kitdir/$catpkgs |
        parallel -j$parallel_jobs "xargs -0 -d '\n' ./bin/tag_package_with_cpes.py --package-json" \
            1>>$kitdir/$catpkgs.tagged \
            2>>$kitdir/$catpkgs.err
done
```
9. if you want do it for all kits
```
metarepodir=~/metarepo_dump
parallel_jobs=8

for kit in `ls $metarepodir`; do
    kitdir=$metarepodir/$kit
    rm -f $kitdir/*.tagged \
        $kitdir/*.err
    for catpkgs in `ls $kitdir`; do
        echo tagging [$kit] $catpkgs ...
        cat $kitdir/$catpkgs |
            parallel -j$parallel_jobs "xargs -0 -d '\n' ./bin/tag_package_with_cpes.py --package-json" \
                1>>$kitdir/$catpkgs.tagged \
                2>>$kitdir/$catpkgs.err
    done
done
```


## I want to contribute/learn more technical details
Check out [CONTRIBUTING](CONTRIBUTING.md)


[Funtoo meta-repo]: https://github.com/funtoo/meta-repo
[CVE]: https://nvd.nist.gov/vuln
[CPE]: https://nvd.nist.gov/products/cpe
[CPE tagger]: https://www.funtoo.org/FLOP:CPE_tagger
[Funtoo Linux Optimization Proposal]: https://www.funtoo.org/Category:FLOP
