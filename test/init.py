"""
Import this file to add the parent directory to the path and setup debug stuff.
"""
import sys
sys.path.insert(0,'..')
from CliRenderer.utils import Flags
Flags.DEBUG=True
