#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

import click

from cpe_tag import conf
from cpe_tag.generators import tag_package_with_cpes, tag_packages_with_cpes
from cpe_tag.searchers import query_cpe_match, query_multi_cpe_match
from cpe_tag.serializers import serialize_package_json
from cpe_tag.utils import validate_batch, validate_package


def throw_on_invalid_feed(feed_loc):
    try:
        assert Path(feed_loc).is_file() is True
    except AssertionError:
        raise OSError(f"{feed_loc}: no such file")


@click.command()
@click.option(
    "--cpe-match-feed",
    default=conf.DEFAULT_FEED_PATH,
    help="Path to NVD CPE Match Feed archive (json.gz)",
)
@click.argument("package_json")
def run(cpe_match_feed, package_json):
    target = json.loads(package_json)
    throw_on_invalid_feed(cpe_match_feed)
    tagged = handle_batch(target) if isinstance(target, list) else handle_single(target)
    print(json.dumps(tagged))


def handle_single(package):
    validate_package(package)
    serialized = serialize_package_json(package)
    tagged = tag_package_with_cpes(serialized, query_function=query_cpe_match)
    return tagged


def handle_batch(packages):
    validate_batch(packages)
    serialized = [serialize_package_json(package) for package in packages]
    tagged = tag_packages_with_cpes(serialized, query_function=query_multi_cpe_match)
    return tagged


if __name__ == "__main__":
    from sys import exit

    exit(run())
