#!/usr/bin/env python3

from jsonschema import validate


def sig_serialize_package_json(hub, package: dict):
    pass


def pre_serialize_package_json(hub, ctx):
    package = ctx.args[1]
    package_json_schema = hub.cpe_tag.utils.get_schema("package_json")
    validate(instance=package, schema=package_json_schema)
