#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

import pop.hub

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="cpe_tag")
hub.cpe_tag.init.cli()


def throw_on_invalid_feed(feed_loc):
    try:
        assert Path(feed_loc).is_file() is True
    except AssertionError:
        raise OSError(f"{feed_loc}: no such file")


def run():
    package = json.loads(hub.OPT.cpe_tag.package_json)
    throw_on_invalid_feed(hub.OPT.cpe_tag.cpe_match_feed)
    serialized = hub.cpe_tag.serializers.serialize_package_json(package)
    tagged = hub.cpe_tag.generators.tag_package_with_cpes(
        serialized, query_function=hub.cpe_tag.searchers.query_cpe_match
    )
    print(json.dumps(tagged))


if __name__ == "__main__":
    from sys import exit

    exit(run())
