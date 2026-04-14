"""
version info for fremorizer, isolated to avoid importing heavy dependencies at build time
"""

import os
version = os.getenv("GIT_DESCRIBE_TAG", "2026.01.alpha1")
__version__ = version
