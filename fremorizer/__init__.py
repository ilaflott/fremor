"""
module init file for fremorizer. sets the version attribute, and sets up a fre_logger
"""

import logging

from ._version import __version__, version

fre_logger = logging.getLogger(__name__)

FORMAT = '[%(levelname)5s:%(filename)24s:%(funcName)24s] %(message)s'
logging.basicConfig( level = logging.WARNING,
                     format = FORMAT,
                     filename = None,
                     encoding = 'utf-8' )

# these need to be here for the base logger configuration, i think
from .cmor_mixer import cmor_run_subtool # pylint: disable=wrong-import-position
from .cmor_finder import cmor_find_subtool, make_simple_varlist # pylint: disable=wrong-import-position
from .cmor_yamler import cmor_yaml_subtool # pylint: disable=wrong-import-position
from .cmor_config import cmor_config_subtool # pylint: disable=wrong-import-position
from .cmor_init import cmor_init_subtool # pylint: disable=wrong-import-position
