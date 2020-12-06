#!/usr/bin/env python3


def get_quasi_cpe(hub, **wfn_attrs) -> str:
    vendor = str(wfn_attrs["vendor"]) if "vendor" in wfn_attrs else None
    product = str(wfn_attrs["product"]) if "product" in wfn_attrs else None
    version = str(wfn_attrs["version"]) if "version" in wfn_attrs else None
    update = str(wfn_attrs["update"]) if "update" in wfn_attrs else None
    if product is None:
        raise TypeError("vendor param is required")
    parts = [vendor, product, version, update]
    return ":".join(list(filter(lambda x: x is not None, parts)))
