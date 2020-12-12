#!/usr/bin/env python3


async def sig_query_cpe_match(hub, quasi_cpe: str, feed=None):
    pass


async def call_query_cpe_match(hub, ctx):
    quasi_cpe = ctx.args[1]
    if quasi_cpe is None:
        return []
    return await ctx.func(*ctx.args, **ctx.kwargs)
