import json
from pathlib import Path


def get_schema(hub, schema: str) -> dict:
    schemas_subpath = "schemas"
    schemas = {
        "package_json": "package.schema.json",
    }
    schema_file = schemas[schema]
    file_path = Path(__file__).resolve()
    schema_path = file_path.parent.joinpath(schemas_subpath).joinpath(schema_file)
    with open(schema_path) as f:
        schema = json.load(f)
    return schema
