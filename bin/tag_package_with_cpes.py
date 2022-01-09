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
    target = json.loads(hub.OPT.cpe_tag.package_json)
    throw_on_invalid_feed(hub.OPT.cpe_tag.cpe_match_feed)
    tagged = handle_multi(target) if isinstance(target, list) else handle_single(target)
    print(json.dumps(tagged))


def handle_single(package):
    serialized = hub.cpe_tag.serializers.serialize_package_json(package)
    tagged = hub.cpe_tag.generators.tag_package_with_cpes(
        serialized, query_function=hub.cpe_tag.searchers.query_cpe_match
    )
    return tagged


def handle_multi(packages):
    serialized = [
        hub.cpe_tag.serializers.serialize_package_json(package) for package in packages
    ]
    tagged = hub.cpe_tag.generators.tag_packages_with_cpes(
        serialized, query_function=hub.cpe_tag.searchers.query_multi_cpe_match
    )
    return tagged


if __name__ == "__main__":
    from sys import exit

    exit(run())
