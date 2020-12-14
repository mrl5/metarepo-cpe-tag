#!/bin/bash

regex='(.+)-([0-9]+.*)(\.ebuild)'
base=/var/db/pkg
parallel_jobs=8
dump_dir=dump

mkdir -p ${dump_dir}
for category in `ls ${base}`; do
    echo ""
    echo "collecting CPEs for $category ..."
    for package in `ls ${base}/${category}/`; do
        ebuild=`ls ${base}/${category}/$package | grep '.ebuild'`
        [[ $ebuild =~ $regex ]];

        echo -n .
        echo "{\"name\":\"${BASH_REMATCH[1]}\",\"versions\":[{\"version\":\"${BASH_REMATCH[2]}\"}]}" |
            xargs -0 -d '\n' ./bin/tag_package_with_cpes.py --cpe-match-feed ~/feeds/json/nvdcpematch-1.0.json.gz |
            jq -r .versions[].cpes[] > ${dump_dir}/${category}:${package}:cpes.json &&
            du ${dump_dir}/${category}:${package}:cpes.json | cut -f1 |
            grep 0 >/dev/null && rm ${dump_dir}/${category}:${package}:cpes.json &

        if [[ $(jobs -r -p | wc -l) -ge $parallel_jobs ]]; then
            wait -n
        fi
    done
    echo ""
done
echo ""
echo "got CPEs"

for file in `ls ${dump_dir}/`; do
    du ${dump_dir}/${file} | cut -f1 | grep 0 >/dev/null && rm ${dump_dir}/${file}
done

for cpes_file in `ls ${dump_dir}/ | grep cpes.json`; do
    echo ""
    echo "collecting CVEs for $cpes_file ..."
    for cpe in `cat ${dump_dir}/${cpes_file}`; do
        cves_file=`echo $cpes_file | sed 's/cpes/cves/'`
        rm -f ${dump_dir}/${cves_file}
        curl -s https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString="$cpe" |
            jq -c ".result.CVE_Items[] | {id: .cve.CVE_data_meta.ID, impact: .impact}" >> ${dump_dir}/${cves_file}
        du ${dump_dir}/${cves_file} | cut -f1 | grep 0 >/dev/null && rm ${dump_dir}/${cves_file}
    done
done
echo ""
echo "got CVEs"

for cves_file in `ls ${dump_dir}/ | grep cves.json`; do
     du ${dump_dir}/${cves_file} | cut -f1 | grep 0 >/dev/null && rm ${dump_dir}/${cves_file}
done
