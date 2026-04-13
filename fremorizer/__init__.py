"""
module init file for fremorizer. sets the version attribute, and sets up a fre_logger
"""

import logging
import os
version = os.getenv("GIT_DESCRIBE_TAG", "2026.01.alpha1")
__version__ = version

fre_logger = logging.getLogger(__name__)

FORMAT = "[%(levelname)5s:%(filename)24s:%(funcName)24s] %(message)s"
logging.basicConfig(level = logging.WARNING,
                    format = FORMAT,
                    filename = None,
                    encoding = 'utf-8' )

from .cmor_mixer import cmor_run_subtool
from .cmor_finder import cmor_find_subtool, make_simple_varlist
from .cmor_yamler import cmor_yaml_subtool
from .cmor_config import cmor_config_subtool
