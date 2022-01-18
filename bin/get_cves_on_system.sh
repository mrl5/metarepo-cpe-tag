#!/bin/bash

regex='(.+)-([0-9]+.*)(\.ebuild)'
base=/var/db/pkg
parallel_jobs=8

IFS='T' read -a timestamp <<< "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
dump_dir=dump/${timestamp[0]}/${timestamp[1]}

mkdir -p ${dump_dir}
for category in `ls ${base}`; do
    echo ""
    echo "collecting CPEs for $category ..."
    packages=$(ls ${base}/${category}/*/*.ebuild)

    for package in $packages; do
        [[ $package =~ $regex ]];
        name=${BASH_REMATCH[1]}
        echo "{\"name\":\"$(basename $name)\",\"versions\":[{\"version\":\"${BASH_REMATCH[2]}\"}]}"
    done |
        jq -s -c '.' |
        xargs -0 -d '\n' ./bin/tag_package_with_cpes.py --cpe-match-feed ~/feeds/json/nvdcpematch-1.0.json.gz |
        jq -r '.[]' > ${dump_dir}/${category}:cpes.json

done
echo ""
echo "got CPEs"
echo ""

for file in $(ls ${dump_dir}/); do
    du ${dump_dir}/${file} | cut -f1 | grep 0 >/dev/null && rm ${dump_dir}/${file}
done

for cpe in `cat ${dump_dir}/*cpes*`; do
    pkg=`echo $cpe | cut -d':' -f4-8 | sed 's/\*//g' | sed 's/:-:/::/g' | sed 's/::$//g' | sed 's/:$//g'`
    cves_file="${pkg}.cves.json"
    echo "collecting CVEs for $pkg ..."
    curl -s https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString="$cpe" |
        jq -c ".result.CVE_Items[] | {id: .cve.CVE_data_meta.ID, impact: .impact}" >> ${dump_dir}/${cves_file}
done
echo ""
echo "got CVEs"

for cves_file in `ls ${dump_dir}/ | grep cves.json`; do
     du ${dump_dir}/${cves_file} | cut -f1 | grep 0 >/dev/null && rm ${dump_dir}/${cves_file}
done
