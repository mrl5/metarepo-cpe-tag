# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import asyncio

from cpe_tag.cpe import convert_quasi_cpe_to_regex
from cpe_tag.searchers import query_cpe_match, query_multi_cpe_match


def tag_packages_with_cpes(packages: list, query_function=None, **kwargs) -> list:
    if query_function is None:
        query_function = query_multi_cpe_match

    quasi_cpes = []
    for package in packages:
        for version in package["versions"]:
            q = version.get("quasi_cpe")
            if q is not None:
                quasi_cpes.append(q)
    patterns = list(map(lambda x: convert_quasi_cpe_to_regex(x), quasi_cpes))
    pattern = "|".join(patterns)
    cpes = asyncio.run(query_function(pattern, **kwargs))
    return cpes


def tag_package_with_cpes(package: dict, query_function=None, **kwargs) -> dict:
    if query_function is None:
        query_function = query_cpe_match

    versions = package["versions"]
    versions = asyncio.run(
        tag_versions(versions, query_function=query_function, **kwargs)
    )
    package["versions"] = versions
    return package


async def tag_versions(versions: list, **kwargs) -> list:
    done_tasks, _ = await asyncio.wait([tag_version(v, **kwargs) for v in versions])
    return list(map(lambda x: x.result(), done_tasks))


async def tag_version(v: dict, query_function=None, **kwargs) -> dict:
    if "quasi_cpe" not in v:
        pass
    elif v["quasi_cpe"] is None:
        del v["quasi_cpe"]
    else:
        cpes = await query_function(v["quasi_cpe"], **kwargs)
        v["cpes"] = list(set(cpes))
        v["cpes"].sort()
        del v["quasi_cpe"]
    return v
