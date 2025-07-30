# build_msi.py
import os
import subprocess
import shutil
from pathlib import Path


def check_wix_installed():
    """Check if WiX Toolset is installed."""
    try:
        subprocess.run(["candle", "-?"], capture_output=True, check=True)
        return True
    except:
        print("ERROR: WiX Toolset not found!")
        print("Please install from: https://wixtoolset.org/")
        return False


def build_msi():
    """Build the MSI installer."""

    if not check_wix_installed():
        return False

    print("Preparing package structure...")
    subprocess.run(["python", "prepare_msi_build.py"], check=True)

    print("Compiling WiX sources...")
    # Compile .wxs to .wixobj
    subprocess.run(
        [
            "candle",
            "-arch",
            "x64",
            "-ext",
            "WixUIExtension",
            "-ext",
            "WixUtilExtension",
            "sw_mcp.wxs",
        ],
        check=True,
    )

    print("Linking MSI...")
    # Link to create MSI
    subprocess.run(
        [
            "light",
            "-ext",
            "WixUIExtension",
            "-ext",
            "WixUtilExtension",
            "-cultures:en-us",
            "-out",
            "sw_mcp_installer.msi",
            "sw_mcp.wixobj",
        ],
        check=True,
    )

    print("\nMSI installer created: sw_mcp_installer.msi")

    # Create distribution folder
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)

    # Move MSI to dist
    shutil.move("sw_mcp_installer.msi", dist_dir / "sw_mcp_v0.1.0_installer.msi")

    # Clean up
    for file in Path(".").glob("*.wixobj"):
        file.unlink()
    for file in Path(".").glob("*.wixpdb"):
        file.unlink()

    print(f"\nInstaller ready: {dist_dir}/sw_mcp_v0.1.0_installer.msi")

    return True


def sign_msi(msi_path, cert_path=None):
    """Sign the MSI with a certificate."""
    if cert_path:
        subprocess.run(
            [
                "signtool",
                "sign",
                "/f",
                cert_path,
                "/t",
                "http://timestamp.digicert.com",
                "/d",
                "SW MCP Installer",
                msi_path,
            ]
        )


if __name__ == "__main__":
    if build_msi():
        print("\nNext steps:")
        print("1. Test the installer on a clean system")
        print("2. Sign the MSI if you have a code signing certificate")
        print("3. Distribute to users")
