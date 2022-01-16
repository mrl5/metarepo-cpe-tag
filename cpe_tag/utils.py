# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from enum import Enum, unique
from pathlib import Path

from jsonschema import Draft7Validator, RefResolver, validate
from jsonschema.protocols import Validator


def validate_package(package: dict):
    schema = get_schema("package_json")
    validate(instance=package, schema=schema)


def validate_batch(batch):
    validator = get_batch_validator()
    validator.validate(batch)


@unique
class Schemas(str, Enum):
    package_json = "package.schema.json"
    batch_of_package_json = "batch.schema.json"
    tagged_package_json = "tagged_package.schema.json"


def get_schema(schema: str) -> dict:
    schemas_subpath = "schemas"
    schema_file = Schemas[schema].value
    file_path = Path(__file__).resolve()
    schema_path = file_path.parent.joinpath(schemas_subpath).joinpath(schema_file)
    with open(schema_path) as f:
        jschema = json.load(f)
    return jschema


def get_schema_store() -> dict:
    # Allows handling schema that reference another schema:
    #   https://python-jsonschema.readthedocs.io/en/stable/references/#resolving-json-references
    #   https://json-schema.org/understanding-json-schema/structuring.html#id
    #   https://json-schema.org/understanding-json-schema/structuring.html#ref
    store = {}
    for s in Schemas:
        schema = get_schema(s.name)
        id = schema["$id"]
        store[id] = schema
    return store


def get_batch_validator() -> Validator:
    batch_schema = get_schema("batch_of_package_json")
    nested_schema = get_schema("package_json")
    store = get_schema_store()
    resolver = RefResolver.from_schema(nested_schema, store=store)
    return Draft7Validator(batch_schema, resolver=resolver)
