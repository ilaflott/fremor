"""
Native YAML Consolidation for CMOR Configuration
================================================

This module provides native YAML consolidation functionality to replace
the dependency on fre-cli's yamltools.consolidate_yamls function.

Functions
---------
- ``load_and_validate_yaml(...)`` - Load and validate a CMOR YAML configuration file

.. note:: This module eliminates the dependency on fre-cli for YAML processing
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from .cmor_yaml_schema import validate_cmor_yaml
except ImportError:
    from cmor_yaml_schema import validate_cmor_yaml

fre_logger = logging.getLogger(__name__)


def load_and_validate_yaml(
    yamlfile: str,
    experiment: Optional[str] = None,
    platform: Optional[str] = None,
    target: Optional[str] = None,
    use: str = "cmor",
    output: Optional[str] = None
) -> Dict[str, Any]:
    """
    Load and validate a CMOR YAML configuration file.

    This function loads a YAML file, validates its structure against the CMOR schema,
    and returns the configuration dictionary. This is a simplified replacement for
    fre-cli's consolidate_yamls function that doesn't require external dependencies.

    :param yamlfile: Path to the YAML configuration file
    :type yamlfile: str
    :param experiment: Experiment name (for compatibility, currently unused)
    :type experiment: str, optional
    :param platform: Platform target (for compatibility, currently unused)
    :type platform: str, optional
    :param target: Compilation target (for compatibility, currently unused)
    :type target: str, optional
    :param use: Configuration section to use (default: 'cmor')
    :type use: str
    :param output: Optional output filename (for compatibility, currently unused)
    :type output: str, optional
    :raises FileNotFoundError: If the YAML file does not exist
    :raises ValueError: If the YAML structure is invalid
    :raises yaml.YAMLError: If the YAML syntax is invalid
    :return: Dictionary containing the YAML configuration
    :rtype: dict

    Example:
        >>> config = load_and_validate_yaml('model.yaml')
        >>> print(config['cmor']['mip_era'])
        CMIP6

    .. note:: This function provides a simplified version of YAML consolidation.
              It does not support:
              - Multi-file YAML consolidation
              - Platform/target/experiment-specific overrides
              - Variable substitution
              For these features, install fre-cli and use its consolidate_yamls function.
    """
    # Expand environment variables in path
    yamlfile = os.path.expandvars(yamlfile)
    yaml_path = Path(yamlfile)

    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML file not found: {yamlfile}")

    fre_logger.info(f"Loading YAML configuration from: {yamlfile}")

    # Load the YAML file
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise yaml.YAMLError(
            f"Failed to parse YAML file {yamlfile}: {exc}"
        ) from exc

    if config is None:
        raise ValueError(f"YAML file {yamlfile} is empty or contains only comments")

    # Ensure the expected structure exists
    if not isinstance(config, dict):
        raise ValueError(
            f"YAML file {yamlfile} must contain a dictionary at the top level, "
            f"got {type(config).__name__}"
        )

    # Validate the configuration against the schema
    try:
        validate_cmor_yaml(config)
        fre_logger.info("YAML configuration passed schema validation")
    except Exception as exc:
        raise ValueError(
            f"YAML configuration in {yamlfile} failed schema validation: {exc}"
        ) from exc

    # Expand environment variables in paths within the configuration
    config = _expand_variables_in_config(config)

    # If output is specified, write the validated config
    if output:
        output_path = Path(output)
        fre_logger.info(f"Writing validated configuration to: {output}")
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    return config


def _expand_variables_in_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively expand environment variables in string values.

    :param config: Configuration dictionary
    :type config: dict
    :return: Configuration with expanded variables
    :rtype: dict
    """
    if isinstance(config, dict):
        return {k: _expand_variables_in_config(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [_expand_variables_in_config(item) for item in config]
    elif isinstance(config, str):
        return os.path.expandvars(config)
    else:
        return config
