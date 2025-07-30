import sys
import os

# Import from compiled module
from .sw_mcp import main as _main

if __name__ == "__main__":
    sys.exit(_main() if callable(_main) else 0)
