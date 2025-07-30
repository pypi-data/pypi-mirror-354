# prepare_msi_build.py
import os
import shutil
import json
from pathlib import Path


def prepare_package_structure():
    """Prepare files for MSI packaging."""

    # Create directory structure
    msi_staging = Path("msi_staging")
    if msi_staging.exists():
        shutil.rmtree(msi_staging)

    # Create package directory
    package_dir = msi_staging / "sw_mcp"
    package_dir.mkdir(parents=True)

    # Copy Nuitka output files
    shutil.copy2("build/sw_mcp.cp310-win_amd64.pyd", package_dir / "sw_mcp.pyd")
    shutil.copy2("build/sw_mcp.pyi", package_dir)

    # Create __init__.py
    init_content = """# SW MCP Package
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
"""

    with open(package_dir / "__init__.py", "w") as f:
        f.write(init_content)

    # Create __main__.py for module execution
    main_content = """import sys
import os

# Import from compiled module
from .sw_mcp import main as _main

if __name__ == "__main__":
    sys.exit(_main() if callable(_main) else 0)
"""

    with open(package_dir / "__main__.py", "w") as f:
        f.write(main_content)

    # Create wrapper script for command line
    wrapper_content = """@echo off
python -m sw_mcp %*
"""

    with open(msi_staging / "sw_mcp.bat", "w") as f:
        f.write(wrapper_content)

    # Create metadata file
    metadata = {
        "name": "sw-mcp",
        "version": "0.1.0",
        "python_version": "3.10",
        "arch": "win_amd64",
        "requires": ["pywin32>=305"],
    }

    with open(package_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("Package structure prepared in msi_staging/")
    return msi_staging


if __name__ == "__main__":
    prepare_package_structure()
