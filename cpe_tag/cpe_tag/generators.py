#!/usr/bin/env python3

import asyncio
from re import sub, escape


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
    edition = (
        wfn_attrs["edition"]
        if "edition" in wfn_attrs and wfn_attrs["edition"] is not None
        else ""
    )
    language = (
        wfn_attrs["language"]
        if "language" in wfn_attrs and wfn_attrs["language"] is not None
        else ""
    )
    swedition = (
        wfn_attrs["swedition"]
        if "swedition" in wfn_attrs and wfn_attrs["swedition"] is not None
        else ""
    )
    targetsw = (
        wfn_attrs["targetsw"]
        if "targetsw" in wfn_attrs and wfn_attrs["targetsw"] is not None
        else "linux"
    )
    targethw = (
        wfn_attrs["targethw"]
        if "targethw" in wfn_attrs and wfn_attrs["targethw"] is not None
        else ""
    )
    other = (
        wfn_attrs["other"]
        if "other" in wfn_attrs and wfn_attrs["other"] is not None
        else ""
    )

    parts = [
        vendor,
        product,
        version,
        update,
        edition,
        language,
        swedition,
        targetsw,
        targethw,
        other,
    ]
    return ":".join(parts)


def convert_quasi_cpe_to_regex(quasi_cpe: str) -> str:
    escaped = escape(quasi_cpe)
    (
        vendor,
        product,
        version,
        update,
        edition,
        language,
        swedition,
        targetsw,
        targethw,
        other,
    ) = escaped.split(":")
    update = "[\\*\\-]" if len(update) == 0 else f"({update}|\\*)"
    edition = "[^:]+" if len(edition) == 0 else f"({edition}|\\*)"
    language = "[^:]+" if len(language) == 0 else f"({language}|\\*)"
    swedition = "[^:]+" if len(swedition) == 0 else f"({swedition}|\\*)"
    targetsw = "[^:]+" if len(targetsw) == 0 else f"({targetsw}|\\*)"
    targethw = "[^:]+" if len(targethw) == 0 else f"({targethw}|\\*)"
    other = "[^:]" if len(other) == 0 else f"({other}|\\*)"
    parts = [
        vendor,
        product,
        version,
        update,
        edition,
        language,
        swedition,
        targetsw,
        targethw,
        other,
    ]
    return ":".join(parts)


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


async def tag_versions(versions: list, **kwargs) -> list:
    done_tasks, _ = await asyncio.wait([tag_version(v, **kwargs) for v in versions])
    return list(map(lambda x: x.result(), done_tasks))


def tag_package_with_cpes(hub, package: dict, query_function=None, **kwargs) -> dict:
    if query_function is None:
        query_function = hub.cpe_tag.searchers.query_cpe_match

    versions = package["versions"]
    versions = asyncio.run(
        tag_versions(versions, query_function=query_function, **kwargs)
    )
    package["versions"] = versions
    return package
