#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk setup PyPI credentials
==================================

Script untuk membantu setup credentials PyPI untuk publishing.
"""

import os
import sys
from pathlib import Path

def create_pypirc():
    """Create .pypirc file"""
    print("🔐 Setting up PyPI credentials...")
    
    home_dir = Path.home()
    pypirc_path = home_dir / ".pypirc"
    
    print(f"📁 Creating .pypirc at: {pypirc_path}")
    
    # Get credentials
    print("\n📋 You need PyPI API token:")
    print("1. Go to https://pypi.org/manage/account/token/")
    print("2. Create new API token")
    print("3. Copy the token (starts with 'pypi-')")
    
    token = input("\n🔑 Enter your PyPI API token: ").strip()
    
    if not token.startswith("pypi-"):
        print("❌ Invalid token format. Token should start with 'pypi-'")
        return False
    
    # Create .pypirc content
    pypirc_content = f"""[distutils]
index-servers = 
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = {token}

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = {token}
"""
    
    # Write .pypirc file
    try:
        with open(pypirc_path, "w") as f:
            f.write(pypirc_content)
        
        # Set proper permissions (readable only by owner)
        os.chmod(pypirc_path, 0o600)
        
        print(f"✅ .pypirc created successfully at {pypirc_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .pypirc: {e}")
        return False

def test_credentials():
    """Test PyPI credentials"""
    print("\n🧪 Testing PyPI credentials...")
    
    import subprocess
    
    try:
        # Test with twine
        result = subprocess.run(
            ["uv", "run", "twine", "check", "--help"], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Twine is available")
            return True
        else:
            print("❌ Twine not available")
            return False
            
    except Exception as e:
        print(f"❌ Error testing credentials: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions"""
    print("\n📋 Usage Instructions:")
    print("=" * 50)
    
    print("\n🚀 To publish to PyPI:")
    print("1. Run: python scripts/publish_to_pypi.py")
    print("2. Or manually:")
    print("   uv build")
    print("   uv run twine upload dist/*")
    
    print("\n🧪 To test with TestPyPI first:")
    print("   uv run twine upload --repository testpypi dist/*")
    
    print("\n📦 After publishing, users can install with:")
    print("   uvx mcp-ngobrol@latest")
    print("   uvx mcp-ngobrol@1.0.0")
    
    print("\n⚙️ MCP Configuration:")
    print("""   {
     "mcpServers": {
       "mcp-ngobrol": {
         "command": "uvx",
         "args": ["mcp-ngobrol@latest"]
       }
     }
   }""")

def main():
    """Main function"""
    print("🔐 MCP Ngobrol - PyPI Credentials Setup")
    print("=" * 50)
    
    # Check if .pypirc already exists
    home_dir = Path.home()
    pypirc_path = home_dir / ".pypirc"
    
    if pypirc_path.exists():
        print(f"📁 .pypirc already exists at: {pypirc_path}")
        response = input("❓ Overwrite existing .pypirc? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Setup cancelled")
            show_usage_instructions()
            return
    
    # Create .pypirc
    if create_pypirc():
        print("\n✅ PyPI credentials setup completed!")
        
        # Test credentials
        if test_credentials():
            print("\n🎉 Ready to publish!")
            show_usage_instructions()
        else:
            print("\n⚠️ Credentials setup completed but testing failed")
            print("You may need to install twine: uv add twine")
    else:
        print("\n❌ Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
