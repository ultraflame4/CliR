"""
Import this file to add the parent directory to the path and setup debug stuff.
"""
import sys
from CliRenderer.core import Flags

sys.path.append('..')
Flags.DEBUG=True