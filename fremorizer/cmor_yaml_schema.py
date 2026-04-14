"""
YAML Schema Validation for CMOR Configuration
==============================================

This module provides schema validation for YAML configuration files used in CMORization workflows.
It defines the JSON schema for CMOR configuration and provides validation functions.

Functions
---------
- ``validate_cmor_yaml(...)`` - Validate a CMOR configuration dictionary against the schema
- ``get_cmor_schema()`` - Get the JSON schema for CMOR configuration

.. note:: Uses jsonschema for validation
"""

from typing import Dict, Any
import jsonschema


def get_cmor_schema() -> Dict[str, Any]:
    """
    Get the JSON schema for CMOR configuration.

    Returns the complete schema that defines the structure of a valid CMOR
    configuration dictionary, including all required and optional fields.

    :return: JSON schema dictionary
    :rtype: dict
    """
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["cmor"],
        "properties": {
            "cmor": {
                "type": "object",
                "required": ["mip_era", "directories", "exp_json", "table_targets"],
                "properties": {
                    "mip_era": {
                        "type": "string",
                        "enum": ["CMIP6", "CMIP7", "cmip6", "cmip7"],
                        "description": "MIP era (CMIP6 or CMIP7)"
                    },
                    "directories": {
                        "type": "object",
                        "required": ["pp_dir", "table_dir", "outdir"],
                        "properties": {
                            "pp_dir": {
                                "type": "string",
                                "description": "Path to postprocessed data directory"
                            },
                            "table_dir": {
                                "type": "string",
                                "description": "Path to CMOR table directory"
                            },
                            "outdir": {
                                "type": "string",
                                "description": "Path to output directory for CMORized files"
                            }
                        },
                        "additionalProperties": False
                    },
                    "exp_json": {
                        "type": "string",
                        "description": "Path to experiment configuration JSON file"
                    },
                    "start": {
                        "type": "string",
                        "pattern": "^\\d{4}$",
                        "description": "Start year (YYYY format)"
                    },
                    "stop": {
                        "type": "string",
                        "pattern": "^\\d{4}$",
                        "description": "Stop year (YYYY format)"
                    },
                    "calendar_type": {
                        "type": "string",
                        "description": "CF-compliant calendar type (e.g., 'julian', 'noleap')"
                    },
                    "table_targets": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["table_name", "target_components"],
                            "properties": {
                                "table_name": {
                                    "type": "string",
                                    "description": "Name of the MIP table (e.g., 'Omon', 'Amon')"
                                },
                                "freq": {
                                    "type": ["string", "null"],
                                    "description": "Frequency of data (e.g., 'monthly', 'daily')"
                                },
                                "gridding": {
                                    "type": ["object", "null"],
                                    "required": ["grid_label", "grid_desc", "nom_res"],
                                    "properties": {
                                        "grid_label": {
                                            "type": "string",
                                            "description": "Grid label (e.g., 'gr', 'gn')"
                                        },
                                        "grid_desc": {
                                            "type": "string",
                                            "description": "Grid description"
                                        },
                                        "nom_res": {
                                            "type": "string",
                                            "description": "Nominal resolution (e.g., '100 km')"
                                        }
                                    },
                                    "additionalProperties": False
                                },
                                "target_components": {
                                    "type": "array",
                                    "minItems": 1,
                                    "items": {
                                        "type": "object",
                                        "required": ["component_name", "chunk", "data_series_type", "variable_list"],
                                        "properties": {
                                            "component_name": {
                                                "type": "string",
                                                "description": "Name of the component (e.g., 'ocean_monthly_1x1deg')"
                                            },
                                            "chunk": {
                                                "type": "string",
                                                "description": "ISO 8601 duration for chunking (e.g., 'P5Y')"
                                            },
                                            "data_series_type": {
                                                "type": "string",
                                                "description": "Type of data series (e.g., 'ts')"
                                            },
                                            "variable_list": {
                                                "type": "string",
                                                "description": "Path to variable list JSON file"
                                            }
                                        },
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "additionalProperties": False
                        }
                    }
                },
                "additionalProperties": False
            }
        },
        "additionalProperties": False
    }


def validate_cmor_yaml(config_dict: Dict[str, Any]) -> None:
    """
    Validate a CMOR configuration dictionary against the schema.

    Validates the structure and content of a CMOR configuration dictionary
    to ensure it meets all requirements. Raises ValidationError if the
    configuration is invalid.

    :param config_dict: Configuration dictionary to validate
    :type config_dict: dict
    :raises jsonschema.ValidationError: If the configuration is invalid
    :raises jsonschema.SchemaError: If the schema itself is invalid
    :return: None
    :rtype: None

    Example:
        >>> config = {'cmor': {'mip_era': 'CMIP6', ...}}
        >>> validate_cmor_yaml(config)  # Raises if invalid
    """
    schema = get_cmor_schema()
    jsonschema.validate(instance=config_dict, schema=schema)
