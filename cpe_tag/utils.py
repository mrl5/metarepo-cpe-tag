# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from enum import Enum, unique
from pathlib import Path


@unique
class Schemas(str, Enum):
    package_json = "package.schema.json"
    tagged_package_json = "tagged_package.schema.json"


def get_schema(schema: str) -> dict:
    schemas_subpath = "schemas"
    schema_file = Schemas[schema].value
    file_path = Path(__file__).resolve()
    schema_path = file_path.parent.joinpath(schemas_subpath).joinpath(schema_file)
    with open(schema_path) as f:
        jschema = json.load(f)
    return jschema
