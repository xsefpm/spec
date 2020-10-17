import pytest
from pathlib import Path
import json
from jsonschema import validate
from jsonschema.validators import (
    Draft7Validator,
    validator_for,
)


@pytest.fixture
def xsefpm_spec_dir():
    return Path(__file__).parent.parent


@pytest.fixture
def schema(xsefpm_spec_dir):
    v3_schema_path = xsefpm_spec_dir / "spec" / "v3.spec.json"
    return json.loads(v3_schema_path.read_text())


@pytest.fixture
def validate_v3(schema):
    def _validate(*args, **kwargs):
        validate(args[0], schema, cls=validator_for(schema, Draft7Validator))

    return _validate
