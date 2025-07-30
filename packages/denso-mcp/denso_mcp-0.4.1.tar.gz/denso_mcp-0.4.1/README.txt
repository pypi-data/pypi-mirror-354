SW MCP - Python COM Integration Tool
====================================

Version: 0.1.0
Python: 3.10 (64-bit) Required

INSTALLATION
------------
This installer will:
1. Install SW MCP Python package to your Python 3.10 site-packages
2. Add command-line wrapper to Python Scripts directory
3. Install required dependencies (pywin32)

USAGE
-----
After installation, you can use SW MCP in two ways:

1. Command line:
   sw_mcp --sse

2. Python import:
   import sw_mcp
   
REQUIREMENTS
------------
- Windows 10 or later (64-bit)
- Python 3.10 (64-bit)
- .NET Framework 4.7.2 or later
- Administrator privileges for COM registration

TROUBLESHOOTING
---------------
If you encounter COM errors:
1. Run as administrator: python -m win32com.server.register
2. Ensure your C# DLLs are properly registered with regasm

Support: support@yourcompany.com