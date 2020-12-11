#!/usr/bin/env python3

from jsonschema import validate

from .schemas import package_json_schema


def sig_serialize_package_json(hub, package: dict):
    pass


def pre_serialize_package_json(hub, ctx):
    package = ctx.args[1]
    validate(instance=package, schema=package_json_schema)
