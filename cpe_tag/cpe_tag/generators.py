#!/usr/bin/env python3

import asyncio


def get_quasi_cpe(hub, **wfn_attrs) -> str:
    vendor = (
        wfn_attrs["vendor"]
        if "vendor" in wfn_attrs and wfn_attrs["vendor"] is not None
        else ""
    )
    product = (
        wfn_attrs["product"]
        if "product" in wfn_attrs and wfn_attrs["product"] is not None
        else ""
    )
    version = (
        wfn_attrs["version"]
        if "version" in wfn_attrs and wfn_attrs["version"] is not None
        else ""
    )
    update = (
        wfn_attrs["update"]
        if "update" in wfn_attrs and wfn_attrs["update"] is not None
        else ""
    )

    if len(product) == 0 or len(version) == 0:
        raise hub.cpe_tag.errors.GeneratorError("missing required params")
    parts = [vendor, product, version, update]
    return ":".join(parts)


def convert_quasi_cpe_to_regex(hub, quasi_cpe: str) -> str:
    vendor, product, version, update = quasi_cpe.split(":")
    update = "[\\*\\-]" if len(update) == 0 else f"({update}|[\\*])"
    parts = [vendor, product, version, update]
    return ":".join(parts)


async def tag_version(hub, v: dict, **kwargs) -> dict:
    if "quasi_cpe" not in v:
        pass
    elif v["quasi_cpe"] is None:
        del v["quasi_cpe"]
    else:
        v["cpes"] = list(
            set(await hub.cpe_tag.searchers.query_cpe_match(v["quasi_cpe"], **kwargs))
        )
        v["cpes"].sort()
        del v["quasi_cpe"]
        v["cpes"].sort()
    return v


async def tag_versions(hub, versions: list, **kwargs) -> list:
    done_tasks, _ = await asyncio.wait([tag_version(hub, v, **kwargs) for v in versions])
    return list(map(lambda x: x.result(), done_tasks))


def tag_package_with_cpes(hub, package: dict, **kwargs) -> dict:
    versions = package["versions"]
    versions = asyncio.run(tag_versions(hub, versions, **kwargs))
    package["versions"] = versions
    return package
