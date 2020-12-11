#!/usr/bin/env python3

from pathlib import Path
from re import search
from shlex import quote


async def sig_query_cpe_match(hub, quasi_cpe: str, feed=None):
    pass


async def call_query_cpe_match(hub, ctx):
    quasi_cpe = ctx.args[1]
    if quasi_cpe is None:
        return []
    return await ctx.func(*ctx.args, **ctx.kwargs)


async def sig_get_feed(hub, feed_loc: str, quasi_cpe: str):
    pass


async def pre_get_feed(hub, ctx):
    try:
        feed_loc = ctx.args[1]
        assert Path(feed_loc).exists() is True
    except AssertionError:
        raise hub.cpe_tag.errors.SearcherError(f"{feed_loc}: No such file or directory")

    try:
        quasi_cpe = ctx.args[2]
        assert search(r"^[^:].*:[^:].+:[^:].+:[^:].*$", quasi_cpe) is not None
    except AssertionError:
        raise hub.cpe_tag.errors.SearcherError("invalid format of quasi_cpe")


async def call_get_feed(hub, ctx):
    ctx.args[1] = quote(ctx.args[1])
    ctx.args[2] = quote(ctx.args[2])
    return await ctx.func(*ctx.args, **ctx.kwargs)
