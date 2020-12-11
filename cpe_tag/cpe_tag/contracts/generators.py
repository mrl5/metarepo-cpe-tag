#!/usr/bin/env python3


def sig_tag_package_with_cpes(hub, package: dict, **kwargs):
    pass


def pre_get_quasi_cpe(hub, ctx):
    try:
        assert ("product" in ctx.kwargs) is True
        assert ("version" in ctx.kwargs) is True
        assert len(ctx.kwargs["product"]) > 0
        assert len(ctx.kwargs["version"]) > 0
    except AssertionError:
        raise hub.cpe_tag.errors.GeneratorError("missing required params")
