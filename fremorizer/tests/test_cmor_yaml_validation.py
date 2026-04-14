"""
Tests for YAML schema validation and consolidation
==================================================

Tests the cmor_yaml_schema and cmor_yaml_consolidator modules.
"""

import json
import pytest
import tempfile
from pathlib import Path
import yaml
import sys

# Import only the modules we need to test directly
# This avoids importing the full fremorizer package which requires cmor
sys.path.insert(0, str(Path(__file__).parent.parent))

from cmor_yaml_schema import get_cmor_schema, validate_cmor_yaml
from cmor_yaml_consolidator import load_and_validate_yaml


# ---- Test data fixtures ----

def create_valid_cmor_config():
    """Create a valid CMOR configuration dictionary."""
    return {
        'cmor': {
            'mip_era': 'CMIP6',
            'directories': {
                'pp_dir': '/path/to/pp',
                'table_dir': '/path/to/tables',
                'outdir': '/path/to/output',
            },
            'exp_json': '/path/to/exp_config.json',
            'start': '1990',
            'stop': '2000',
            'calendar_type': 'noleap',
            'table_targets': [
                {
                    'table_name': 'Omon',
                    'freq': 'monthly',
                    'gridding': {
                        'grid_label': 'gr',
                        'grid_desc': 'regridded to 1x1 degree',
                        'nom_res': '100 km',
                    },
                    'target_components': [
                        {
                            'component_name': 'ocean_monthly',
                            'chunk': 'P5Y',
                            'data_series_type': 'ts',
                            'variable_list': '/path/to/varlist.json',
                        }
                    ],
                }
            ],
        }
    }


# ================================================================
# Tests for cmor_yaml_schema.py
# ================================================================

def test_get_cmor_schema():
    """Test that get_cmor_schema returns a valid JSON schema."""
    schema = get_cmor_schema()
    assert isinstance(schema, dict)
    assert '$schema' in schema
    assert 'properties' in schema
    assert 'cmor' in schema['properties']


def test_validate_valid_config():
    """Test that validate_cmor_yaml accepts a valid configuration."""
    config = create_valid_cmor_config()
    # Should not raise
    validate_cmor_yaml(config)


def test_validate_missing_required_field():
    """Test that validate_cmor_yaml rejects config missing required field."""
    config = create_valid_cmor_config()
    del config['cmor']['mip_era']

    with pytest.raises(Exception):  # jsonschema.ValidationError
        validate_cmor_yaml(config)


def test_validate_invalid_mip_era():
    """Test that validate_cmor_yaml rejects invalid mip_era value."""
    config = create_valid_cmor_config()
    config['cmor']['mip_era'] = 'CMIP5'  # Not in enum

    with pytest.raises(Exception):  # jsonschema.ValidationError
        validate_cmor_yaml(config)


def test_validate_missing_directories():
    """Test that validate_cmor_yaml rejects config missing directories."""
    config = create_valid_cmor_config()
    del config['cmor']['directories']['pp_dir']

    with pytest.raises(Exception):  # jsonschema.ValidationError
        validate_cmor_yaml(config)


def test_validate_empty_table_targets():
    """Test that validate_cmor_yaml rejects config with empty table_targets."""
    config = create_valid_cmor_config()
    config['cmor']['table_targets'] = []

    with pytest.raises(Exception):  # jsonschema.ValidationError
        validate_cmor_yaml(config)


def test_validate_invalid_year_format():
    """Test that validate_cmor_yaml rejects invalid year format."""
    config = create_valid_cmor_config()
    config['cmor']['start'] = '90'  # Not YYYY format

    with pytest.raises(Exception):  # jsonschema.ValidationError
        validate_cmor_yaml(config)


def test_validate_missing_gridding_fields():
    """Test that validate_cmor_yaml rejects incomplete gridding dict."""
    config = create_valid_cmor_config()
    del config['cmor']['table_targets'][0]['gridding']['grid_label']

    with pytest.raises(Exception):  # jsonschema.ValidationError
        validate_cmor_yaml(config)


def test_validate_null_gridding():
    """Test that validate_cmor_yaml accepts null gridding."""
    config = create_valid_cmor_config()
    config['cmor']['table_targets'][0]['gridding'] = None

    # Should not raise - null gridding is allowed
    validate_cmor_yaml(config)


def test_validate_null_freq():
    """Test that validate_cmor_yaml accepts null freq."""
    config = create_valid_cmor_config()
    config['cmor']['table_targets'][0]['freq'] = None

    # Should not raise - null freq is allowed
    validate_cmor_yaml(config)


def test_validate_optional_fields_missing():
    """Test that validate_cmor_yaml accepts config without optional fields."""
    config = {
        'cmor': {
            'mip_era': 'CMIP7',
            'directories': {
                'pp_dir': '/path/to/pp',
                'table_dir': '/path/to/tables',
                'outdir': '/path/to/output',
            },
            'exp_json': '/path/to/exp_config.json',
            'table_targets': [
                {
                    'table_name': 'ocean',
                    'target_components': [
                        {
                            'component_name': 'ocean_monthly',
                            'chunk': 'P5Y',
                            'data_series_type': 'ts',
                            'variable_list': '/path/to/varlist.json',
                        }
                    ],
                }
            ],
        }
    }

    # Should not raise - start, stop, calendar_type, freq, gridding are optional
    validate_cmor_yaml(config)


# ================================================================
# Tests for cmor_yaml_consolidator.py
# ================================================================

def test_load_and_validate_yaml_valid(tmp_path):
    """Test that load_and_validate_yaml loads a valid YAML file."""
    config = create_valid_cmor_config()
    yaml_file = tmp_path / 'test.yaml'

    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)

    result = load_and_validate_yaml(str(yaml_file))
    assert result == config


def test_load_and_validate_yaml_file_not_found():
    """Test that load_and_validate_yaml raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_and_validate_yaml('/nonexistent/file.yaml')


def test_load_and_validate_yaml_invalid_syntax(tmp_path):
    """Test that load_and_validate_yaml raises error on invalid YAML syntax."""
    yaml_file = tmp_path / 'invalid.yaml'

    with open(yaml_file, 'w', encoding='utf-8') as f:
        f.write('invalid: yaml: syntax:\n  - unclosed [bracket')

    with pytest.raises(yaml.YAMLError):
        load_and_validate_yaml(str(yaml_file))


def test_load_and_validate_yaml_empty_file(tmp_path):
    """Test that load_and_validate_yaml raises error on empty file."""
    yaml_file = tmp_path / 'empty.yaml'
    yaml_file.write_text('')

    with pytest.raises(ValueError, match='empty'):
        load_and_validate_yaml(str(yaml_file))


def test_load_and_validate_yaml_not_dict(tmp_path):
    """Test that load_and_validate_yaml raises error if top level is not dict."""
    yaml_file = tmp_path / 'notdict.yaml'

    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(['not', 'a', 'dict'], f)

    with pytest.raises(ValueError, match='dictionary'):
        load_and_validate_yaml(str(yaml_file))


def test_load_and_validate_yaml_invalid_schema(tmp_path):
    """Test that load_and_validate_yaml raises error on schema validation failure."""
    config = create_valid_cmor_config()
    del config['cmor']['mip_era']  # Make it invalid

    yaml_file = tmp_path / 'invalid_schema.yaml'
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)

    with pytest.raises(ValueError, match='schema validation'):
        load_and_validate_yaml(str(yaml_file))


def test_load_and_validate_yaml_with_output(tmp_path):
    """Test that load_and_validate_yaml writes output when specified."""
    config = create_valid_cmor_config()
    input_file = tmp_path / 'input.yaml'
    output_file = tmp_path / 'output.yaml'

    with open(input_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)

    result = load_and_validate_yaml(str(input_file), output=str(output_file))

    assert result == config
    assert output_file.exists()

    with open(output_file, 'r', encoding='utf-8') as f:
        output_config = yaml.safe_load(f)

    assert output_config == config


def test_load_and_validate_yaml_expands_env_vars(tmp_path, monkeypatch):
    """Test that load_and_validate_yaml expands environment variables."""
    # Set an environment variable
    monkeypatch.setenv('TEST_PP_DIR', '/actual/pp/dir')

    config = create_valid_cmor_config()
    config['cmor']['directories']['pp_dir'] = '$TEST_PP_DIR'

    yaml_file = tmp_path / 'test_env.yaml'
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)

    result = load_and_validate_yaml(str(yaml_file))

    # Environment variable should be expanded
    assert result['cmor']['directories']['pp_dir'] == '/actual/pp/dir'


def test_load_and_validate_yaml_expands_nested_env_vars(tmp_path, monkeypatch):
    """Test that environment variables are expanded in nested structures."""
    monkeypatch.setenv('VARLIST_PATH', '/actual/varlist.json')

    config = create_valid_cmor_config()
    config['cmor']['table_targets'][0]['target_components'][0]['variable_list'] = '$VARLIST_PATH'

    yaml_file = tmp_path / 'test_nested_env.yaml'
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)

    result = load_and_validate_yaml(str(yaml_file))

    assert result['cmor']['table_targets'][0]['target_components'][0]['variable_list'] == '/actual/varlist.json'


def test_load_and_validate_yaml_compatibility_params(tmp_path):
    """Test that load_and_validate_yaml accepts compatibility parameters."""
    config = create_valid_cmor_config()
    yaml_file = tmp_path / 'test.yaml'

    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)

    # Should accept these parameters without error (even if unused)
    result = load_and_validate_yaml(
        str(yaml_file),
        experiment='test_exp',
        platform='test_platform',
        target='test_target',
        use='cmor'
    )

    assert result == config
