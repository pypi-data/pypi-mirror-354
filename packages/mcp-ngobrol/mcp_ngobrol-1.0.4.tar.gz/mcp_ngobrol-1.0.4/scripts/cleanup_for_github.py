#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk membersihkan project sebelum upload ke GitHub
=========================================================

Script ini akan menghapus file-file temporary, cache, dan development
yang tidak perlu di-upload ke GitHub repository.
"""

import os
import shutil
import glob
from pathlib import Path

def remove_file_or_dir(path):
    """Remove file atau directory dengan error handling"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"  ✅ Removed file: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"  ✅ Removed directory: {path}")
        else:
            print(f"  ⚠️  Not found: {path}")
    except Exception as e:
        print(f"  ❌ Error removing {path}: {e}")

def cleanup_build_artifacts():
    """Clean build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    artifacts = [
        "dist/",
        "build/",
        "*.egg-info",
        "src/*.egg-info",
        "__pycache__/",
        "**/__pycache__/",
        "*.pyc",
        "**/*.pyc",
        "*.pyo",
        "**/*.pyo",
        ".pytest_cache/",
        "**/.pytest_cache/"
    ]
    
    for pattern in artifacts:
        if "*" in pattern:
            for path in glob.glob(pattern, recursive=True):
                remove_file_or_dir(path)
        else:
            remove_file_or_dir(pattern)

def cleanup_development_files():
    """Clean development files"""
    print("\n🔧 Cleaning development files...")
    
    dev_files = [
        # Test files
        "test_mcp_local.py",
        "use_mcp_direct.py",
        "setup_mcp_connection.py",
        "debug_websocket.html",
        
        # Development configs
        "ui_settings.json",
        "dev-config.json",
        "webui-config.json",
        
        # Test reports
        "test_reports/",
        
        # Temporary files
        "*.tmp",
        "*.temp",
        "*.log",
        ".DS_Store",
        "Thumbs.db"
    ]
    
    for pattern in dev_files:
        if "*" in pattern:
            for path in glob.glob(pattern, recursive=True):
                remove_file_or_dir(path)
        else:
            remove_file_or_dir(pattern)

def cleanup_config_duplicates():
    """Clean duplicate config files"""
    print("\n📋 Cleaning duplicate config files...")
    
    # Keep only the correct/final versions
    duplicate_configs = [
        "augment-mcp-config.json",
        "augment-dev-config.json", 
        "augment-webui-config.json",
        "augment-setup-guide.json",
        "augment-config-templates.json",
        "augment-quick-setup.json",
        "config-templates.json",
        "cursor-mcp-config.json",
        "installation-guide.json",
        "mcp-ngobrol-config.json",
        "quick-setup.json",
        "augment_mcp_config.json"
    ]
    
    for config_file in duplicate_configs:
        remove_file_or_dir(config_file)

def cleanup_cache_and_temp():
    """Clean cache and temporary directories"""
    print("\n💾 Cleaning cache and temporary files...")
    
    cache_dirs = [
        ".uv/",
        ".mypy_cache/",
        ".coverage",
        "htmlcov/",
        ".tox/",
        ".venv/",
        "venv/",
        "env/",
        ".env"
    ]
    
    for cache_dir in cache_dirs:
        remove_file_or_dir(cache_dir)

def cleanup_editor_files():
    """Clean editor and IDE files"""
    print("\n📝 Cleaning editor files...")
    
    editor_files = [
        ".vscode/",
        ".idea/",
        "*.swp",
        "*.swo",
        "*~",
        ".vim/",
        "*.sublime-*"
    ]
    
    for pattern in editor_files:
        if "*" in pattern:
            for path in glob.glob(pattern, recursive=True):
                remove_file_or_dir(path)
        else:
            remove_file_or_dir(pattern)

def keep_essential_files():
    """List essential files that should be kept"""
    print("\n✅ Essential files to keep:")
    
    essential_files = [
        "README.md",
        "README.zh-CN.md", 
        "README.zh-TW.md",
        "LICENSE",
        "pyproject.toml",
        "uv.lock",
        "src/",
        "scripts/",
        "docs/",
        "tests/",
        "RELEASE_NOTES/",
        "run_mcp_simple.py",
        "PUBLISHING_GUIDE.md",
        "augment-production-config.json",
        "augment-development-config.json",
        "augment-webui-correct-config.json",
        "augment-correct-templates.json",
        "augment-correct-setup.json"
    ]
    
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ⚠️  Missing: {file_path}")

def create_gitignore():
    """Create or update .gitignore"""
    print("\n📄 Creating/updating .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
ui_settings.json
test_reports/
debug_websocket.html
*.tmp
*.temp

# Development configs (keep only production ones)
dev-config.json
webui-config.json
augment-mcp-config.json
augment-dev-config.json
augment-webui-config.json
augment-setup-guide.json
augment-config-templates.json
augment-quick-setup.json
config-templates.json
cursor-mcp-config.json
installation-guide.json
mcp-ngobrol-config.json
quick-setup.json
augment_mcp_config.json

# Test files
test_mcp_local.py
use_mcp_direct.py
setup_mcp_connection.py
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print("  ✅ .gitignore created/updated")

def main():
    """Main cleanup function"""
    print("🧹 MCP Ngobrol - GitHub Cleanup Script")
    print("=" * 50)
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Run cleanup steps
    cleanup_build_artifacts()
    cleanup_development_files()
    cleanup_config_duplicates()
    cleanup_cache_and_temp()
    cleanup_editor_files()
    
    # Create .gitignore
    create_gitignore()
    
    # Show essential files
    keep_essential_files()
    
    print("\n🎉 Cleanup completed!")
    print("\n📋 Next steps:")
    print("1. Review remaining files")
    print("2. Test: python run_mcp_simple.py")
    print("3. Commit to git: git add . && git commit -m 'Clean project for GitHub'")
    print("4. Push to GitHub: git push origin main")

if __name__ == "__main__":
    main()
