# SW MCP Package
import sys
import os

# Ensure DLL directory is in PATH for COM dependencies
if sys.platform == 'win32':
    import pythoncom
    dll_dir = os.path.dirname(__file__)
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(dll_dir)
    else:
        os.environ['PATH'] = dll_dir + os.pathsep + os.environ['PATH']

# Import the compiled module
from .sw_mcp import *

__version__ = "0.1.0"
