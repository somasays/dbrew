import pytest
from click.testing import CliRunner
from dbrew.client.cli import cli
import contextlib
import os


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def valid_yaml(tmp_path):
    yaml_data = """\
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
    file_path = tmp_path / 'valid.yaml'
    file_path.write_text(yaml_data)
    return str(file_path)


@pytest.fixture
def invalid_yaml(tmp_path):
    yaml_data = """\
schema_version: 0.1
invalid:
    id: monthly_active_users
"""
    file_path = tmp_path / 'invalid.yaml'
    file_path.write_text(yaml_data)
    return str(file_path)


class change_directory:
    """Context manager for changing the current working directory."""
    def __init__(self, path):
        self.path = path
        self.saved_path = None

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.saved_path)

@pytest.fixture
def temp_cwd(tmp_path):
    """Fixture to provide a context manager for temporarily changing the working directory."""
    return change_directory(tmp_path)



def test_brew_with_valid_file(runner, valid_yaml):
    result = runner.invoke(cli, ['brew', '--path', valid_yaml])
    assert result.exit_code == 0

def test_brew_with_invalid_file(runner, invalid_yaml):
    result = runner.invoke(cli, ['brew', '--path', invalid_yaml])
    assert 'Error:' in result.output

def test_brew_with_missing_file(runner):
    result = runner.invoke(cli, ['brew', '--path', 'tests/missing.yaml'])
    assert 'Error:' in result.output

def test_brew_with_default_file(runner):
    result = runner.invoke(cli, ['brew'])
    assert result.exit_code == 0


def test_brew_with_default_file_in_temp_dir(runner, valid_yaml, temp_cwd):
    with temp_cwd:
        # Copy the valid_yaml file to the current working directory with the name 'dataproduct.yaml'
        os.rename(valid_yaml, os.path.join(temp_cwd.path, 'dataproduct.yaml'))

        # Now invoke the brew command without specifying the --path option.
        # It should look for 'dataproduct.yaml' in the current working directory.
        result = runner.invoke(cli, ['brew'])

    # Verify the result
    assert result.exit_code == 0


def test_help(runner):
    # Invoke the cli with the --help option
    result = runner.invoke(cli, ['--help'])

    # Check the exit code to ensure there were no errors
    assert result.exit_code == 0

    # Check the output to ensure it contains the expected help text.
    # This is just a basic check. You may want to add more detailed checks
    # to ensure all the expected information is present in the help text.
    assert 'Usage:' in result.output
    assert 'Options:' in result.output
    assert '--help  Show this message and exit.' in result.output
    assert 'brew' in result.output