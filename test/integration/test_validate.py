# File: test/test_integration.py
import pytest
from dbrew.core.validate.schema import YamlValidator, DataProductSchema


@pytest.fixture
def valid_yaml_file_path(tmp_path):
    yaml_content = """
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
    yaml_file_path = tmp_path / "valid_product.yml"
    yaml_file_path.write_text(yaml_content)
    return yaml_file_path


def test_integration(valid_yaml_file_path):
    # Instantiate the YamlValidator with the path to the valid YAML file
    validator = YamlValidator(str(valid_yaml_file_path))

    # Load and validate the YAML file
    yaml_data = validator.load_yaml()
    validated_data = validator.validate_yaml(yaml_data)

    # Assert that the validated_data is of type DataProductSchema
    assert isinstance(validated_data, DataProductSchema)

    # Assert values in validated_data object
    product_data = validated_data.product
    assert product_data.id == "monthly_active_users"
    assert product_data.version == "1.0.0"
    assert product_data.name == "Monthly active users"
    assert product_data.description == "Data product to calculate and report monthly active users across business units."
    assert product_data.owner == "xx@yy.com"
    assert product_data.schedule == "0 7 * * *"
    assert product_data.engine['dbt']['models_package'] == "src/"

    # Check the constraints
    for constraint in product_data.constraints:
        fields = constraint.get('fields', {})
        if 'active_users' in fields:
            active_users_constraints = fields['active_users']
            assert 'is_not_null' in active_users_constraints
            assert 'is_positive_integer' in active_users_constraints
            break  # Exit loop once active_users constraints have been found and checked
