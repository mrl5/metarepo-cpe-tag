#!/usr/bin/env python3


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
