import pytest
from dbrew.core.validate.schema import YamlValidator, DataProductSchema, ValidationError
from unittest import mock
from io import StringIO
import yaml

# Sample valid YAML data
valid_yaml_data = """
schema_version: 0.1
product:
  id: monthly_active_users
  version: "1.0.0"
  name: Monthly active users
  description: Data product to calculate and report monthly active users across business units.
  owner: xx@yy.com
  schedule: "0 7 * * *"
  engine:
    dbt:
      models_package: src/
  constraints:
    - fields:
        - active_users:
            - is_not_null
            - is_positive_integer
"""

# Sample invalid YAML data (missing required fields)
invalid_yaml_data = """
schema_version: 0.1
product:
  id: monthly_active_users
"""


def test_load_yaml(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data=valid_yaml_data))
    validator = YamlValidator('fake_path')
    assert validator.load_yaml() == yaml.safe_load(StringIO(valid_yaml_data))


def test_validate_yaml():
    validator = YamlValidator('fake_path')
    validated_data = validator.validate_yaml(yaml.safe_load(StringIO(valid_yaml_data)))
    assert isinstance(validated_data, DataProductSchema)


def test_validate_yaml_invalid():
    validator = YamlValidator('fake_path')
    with pytest.raises(ValidationError):
        validator.validate_yaml(yaml.safe_load(StringIO(invalid_yaml_data)))


def test_validate_file(mocker):
    mocker.patch.object(YamlValidator, 'load_yaml', return_value=yaml.safe_load(StringIO(valid_yaml_data)))
    validator = YamlValidator('fake_path')
    validated_data = validator.validate_file()
    assert isinstance(validated_data, DataProductSchema)



def test_load_yaml_file_not_found(capfd):
    # This test checks the case where the file does not exist
    validator = YamlValidator('nonexistent_path')
    with pytest.raises(FileNotFoundError):
        validator.load_yaml()
    captured = capfd.readouterr()  # captures stdout and stderr
    assert captured.out == ''

def test_validate_file_invalid_yaml(capfd):
    # This test checks the case where the YAML data is invalid
    invalid_yaml_data = """
    schema_version: 0.1
    product:
      id: monthly_active_users
    """
    mock_open = mock.mock_open(read_data=invalid_yaml_data)
    with mock.patch('builtins.open', mock_open):
        validator = YamlValidator('fake_path')
        with pytest.raises(ValidationError):
            validated_data = validator.validate_file()
        # assert validated_data is None
            captured = capfd.readouterr()  # captures stdout and stderr
            assert "Validation error:" in captured.out