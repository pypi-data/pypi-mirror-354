#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk publish MCP Ngobrol ke PyPI
========================================

Script otomatis untuk build dan publish package ke PyPI.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, check=True, capture_output=False):
    """Run command dengan error handling"""
    print(f"🔄 Running: {cmd}")
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=check)
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {cmd}")
        print(f"Error: {e}")
        if capture_output and e.stdout:
            print(f"Stdout: {e.stdout}")
        if capture_output and e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def clean_build_artifacts():
    """Clean build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    artifacts = [
        "dist",
        "build", 
        "*.egg-info",
        "src/*.egg-info"
    ]
    
    for artifact in artifacts:
        if "*" in artifact:
            # Use glob for wildcard patterns
            import glob
            for path in glob.glob(artifact):
                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                        print(f"  Removed directory: {path}")
                    else:
                        os.remove(path)
                        print(f"  Removed file: {path}")
        else:
            if os.path.exists(artifact):
                if os.path.isdir(artifact):
                    shutil.rmtree(artifact)
                    print(f"  Removed directory: {artifact}")
                else:
                    os.remove(artifact)
                    print(f"  Removed file: {artifact}")

def check_version():
    """Check current version"""
    print("📋 Checking current version...")
    
    # Read version from pyproject.toml
    with open("pyproject.toml", "r") as f:
        content = f.read()
        
    import re
    version_match = re.search(r'version = "([^"]+)"', content)
    if version_match:
        version = version_match.group(1)
        print(f"  Current version: {version}")
        return version
    else:
        print("❌ Could not find version in pyproject.toml")
        return None

def build_package():
    """Build package"""
    print("🔨 Building package...")
    
    # Use uv to build
    success = run_command("uv build")
    if success:
        print("✅ Package built successfully")
        return True
    else:
        print("❌ Package build failed")
        return False

def check_package():
    """Check package with twine"""
    print("🔍 Checking package...")
    
    success = run_command("uv run twine check dist/*")
    if success:
        print("✅ Package check passed")
        return True
    else:
        print("❌ Package check failed")
        return False

def upload_to_testpypi():
    """Upload to TestPyPI first"""
    print("🧪 Uploading to TestPyPI...")
    
    success = run_command("uv run twine upload --repository testpypi dist/*")
    if success:
        print("✅ Uploaded to TestPyPI successfully")
        return True
    else:
        print("❌ Upload to TestPyPI failed")
        return False

def upload_to_pypi():
    """Upload to PyPI"""
    print("🚀 Uploading to PyPI...")
    
    success = run_command("uv run twine upload dist/*")
    if success:
        print("✅ Uploaded to PyPI successfully")
        return True
    else:
        print("❌ Upload to PyPI failed")
        return False

def test_installation():
    """Test installation from PyPI"""
    print("🧪 Testing installation...")
    
    version = check_version()
    if not version:
        return False
        
    # Test with uvx
    success = run_command(f"uvx mcp-ngobrol@{version} version")
    if success:
        print("✅ Installation test passed")
        return True
    else:
        print("❌ Installation test failed")
        return False

def main():
    """Main function"""
    print("🚀 MCP Ngobrol - PyPI Publishing Script")
    print("=" * 50)
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    if not os.path.exists("pyproject.toml"):
        print("❌ pyproject.toml not found. Are you in the project root?")
        sys.exit(1)
    
    # Step 1: Clean build artifacts
    clean_build_artifacts()
    
    # Step 2: Check version
    version = check_version()
    if not version:
        sys.exit(1)
    
    # Step 3: Build package
    if not build_package():
        sys.exit(1)
    
    # Step 4: Check package
    if not check_package():
        sys.exit(1)
    
    # Step 5: Ask for confirmation
    print(f"\n📦 Ready to publish version {version}")
    print("🎯 This will upload to PyPI and make it available via:")
    print(f"   uvx mcp-ngobrol@{version}")
    print(f"   uvx mcp-ngobrol@latest")
    
    response = input("\n❓ Continue with publishing? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Publishing cancelled")
        sys.exit(0)
    
    # Step 6: Upload to PyPI
    if not upload_to_pypi():
        print("\n💡 Tip: Make sure you have PyPI credentials configured:")
        print("   uv run twine configure")
        sys.exit(1)
    
    # Step 7: Test installation (optional)
    print(f"\n🎉 Successfully published version {version}!")
    print("\n📋 Next steps:")
    print(f"1. Test installation: uvx mcp-ngobrol@{version} test")
    print("2. Update MCP configuration to use new version")
    print("3. Test with AI assistants (Cursor, Windsurf, etc.)")
    
    print(f"\n✅ Package is now available at: https://pypi.org/project/mcp-ngobrol/{version}/")

if __name__ == "__main__":
    main()
