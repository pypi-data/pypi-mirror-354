# 🚀 MCP Ngobrol - Publishing Guide

## � GitHub Repository Setup

### 🔧 Step 1: Initialize Git Repository

#### Option A: Fresh Repository
```bash
# Initialize git in project directory
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit - MCP Ngobrol v1.0.0"

# Add GitHub remote
git remote add origin https://github.com/mbprcc/mcp-ngobrol.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### Option B: Clone dari GitHub (Jika repo sudah ada)
```bash
# Clone repository
git clone https://github.com/mbprcc/mcp-ngobrol.git
cd mcp-ngobrol

# Copy project files ke dalam repo
# (copy semua files dari project ke dalam folder ini)

# Add dan commit
git add .
git commit -m "Add MCP Ngobrol v1.0.0 project files"
git push origin main
```

### 🌐 Step 2: Create GitHub Repository

#### Via GitHub Web:
1. **Login** ke GitHub (https://github.com/mbprcc)
2. **Click** "New repository" atau "+"
3. **Repository name**: `mcp-ngobrol`
4. **Description**: "MCP Ngobrol v1.0.0 - Indonesian-first Interactive Feedback System for AI Assistants"
5. **Visibility**: Public
6. **Initialize**: Jangan centang README, .gitignore, license (sudah ada)
7. **Click** "Create repository"

#### Via GitHub CLI (Optional):
```bash
# Install GitHub CLI jika belum ada
# https://cli.github.com/

# Login
gh auth login

# Create repository
gh repo create mbprcc/mcp-ngobrol --public --description "MCP Ngobrol v1.0.0 - Indonesian-first Interactive Feedback System"

# Push code
git remote add origin https://github.com/mbprcc/mcp-ngobrol.git
git branch -M main
git push -u origin main
```

### 📋 Step 3: Verify Repository

#### Check Repository Contents:
- ✅ **README.md** (3 languages)
- ✅ **LICENSE** (dengan MBPRCC attribution)
- ✅ **pyproject.toml** (correct URLs)
- ✅ **src/mcp_ngobrol/** (source code)
- ✅ **scripts/** (publishing tools)
- ✅ **docs/** (documentation)
- ✅ **Augment configs** (5 configuration files)

#### Repository Settings:
1. **About section**: Add description dan topics
2. **Topics**: `mcp`, `ai-assistant`, `feedback`, `indonesian`, `interactive`
3. **Website**: Link ke PyPI page (setelah publish)
4. **Releases**: Siap untuk v1.0.0 release

### 🔄 Step 4: Development Workflow

#### Daily Development:
```bash
# Pull latest changes
git pull origin main

# Make changes...

# Stage changes
git add .

# Commit dengan descriptive message
git commit -m "feat: add new feature XYZ"

# Push to GitHub
git push origin main
```

#### Feature Development:
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes dan commit
git add .
git commit -m "feat: implement new feature"

# Push feature branch
git push origin feature/new-feature

# Create Pull Request di GitHub
# Merge setelah review
```

## �📋 Pre-Publishing Checklist

### ✅ Package Ready Status:
- [x] **Package Built**: `dist/mcp_ngobrol-1.0.0-py3-none-any.whl`
- [x] **Source Distribution**: `dist/mcp_ngobrol-1.0.0.tar.gz`
- [x] **pyproject.toml**: Configured with correct metadata
- [x] **README.md**: Complete documentation
- [x] **LICENSE**: MIT License included
- [x] **Scripts**: Publishing automation ready

### 🔧 Required Tools:
- [x] **UV**: Package manager (already installed)
- [x] **Twine**: PyPI upload tool (in dev dependencies)
- [x] **Build System**: Hatchling (configured)

## 🔐 Step 1: Setup PyPI Credentials

### Option A: Automatic Setup
```bash
python scripts/setup_pypi_credentials.py
```

### Option B: Manual Setup
1. **Get PyPI API Token**:
   - Go to https://pypi.org/manage/account/token/
   - Create new API token for "mcp-ngobrol"
   - Copy token (starts with `pypi-`)

2. **Create .pypirc**:
```ini
[distutils]
index-servers = 
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

3. **Set Permissions**:
```bash
chmod 600 ~/.pypirc
```

## 🚀 Step 2: Publishing Options

### Option A: Automated Publishing (Recommended)
```bash
python scripts/publish_to_pypi.py
```

This script will:
1. Clean build artifacts
2. Check current version (1.0.0)
3. Build fresh package
4. Validate package with twine
5. Ask for confirmation
6. Upload to PyPI
7. Provide next steps

### Option B: Manual Publishing

#### 1. Clean and Build:
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info src/*.egg-info

# Build package
uv build
```

#### 2. Check Package:
```bash
uv run twine check dist/*
```

#### 3. Test Upload (Optional):
```bash
uv run twine upload --repository testpypi dist/*
```

#### 4. Production Upload:
```bash
uv run twine upload dist/*
```

## 📦 Step 3: Verify Publication

### Check PyPI Page:
- **URL**: https://pypi.org/project/mcp-ngobrol/
- **Version**: 1.0.0
- **Files**: Wheel + Source distribution

### Test Installation:
```bash
# Test with uvx (recommended)
uvx mcp-ngobrol@1.0.0 --version

# Test with pip
pip install mcp-ngobrol==1.0.0
```

## ⚙️ Step 4: Update Configurations

### Augment Code Configuration:
```json
{
  "mcpServers": {
    "mcp-ngobrol": {
      "command": "uvx",
      "args": ["mcp-ngobrol@latest"],
      "env": {
        "FORCE_WEB": "false",
        "MCP_LANGUAGE": "id",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

### Cursor IDE Configuration:
```json
{
  "mcp": {
    "servers": {
      "mcp-ngobrol": {
        "command": "uvx",
        "args": ["mcp-ngobrol@latest"]
      }
    }
  }
}
```

## 🎯 Step 5: Post-Publishing Tasks

### 1. Update Documentation:
- [ ] Update installation instructions
- [ ] Update version references
- [ ] Create release notes

### 2. Test Integration:
- [ ] Test with Augment Code
- [ ] Test with Cursor IDE
- [ ] Test GUI and Web UI modes
- [ ] Verify Indonesian language support

### 3. Community Outreach:
- [ ] Announce on GitHub
- [ ] Update README badges
- [ ] Share with community

## 🔍 Troubleshooting

### Common Issues:

#### 1. **Authentication Failed**
```bash
# Check credentials
cat ~/.pypirc

# Regenerate token if needed
python scripts/setup_pypi_credentials.py
```

#### 2. **Package Already Exists**
```bash
# Bump version in pyproject.toml
version = "1.0.1"

# Rebuild and republish
uv build
uv run twine upload dist/*
```

#### 3. **Build Errors**
```bash
# Check dependencies
uv sync

# Clean and rebuild
rm -rf dist/
uv build
```

## 📊 Success Metrics

### After Publishing:
- ✅ Package available on PyPI
- ✅ Installation works with `uvx mcp-ngobrol@latest`
- ✅ MCP server starts correctly
- ✅ GUI and Web UI both functional
- ✅ Indonesian language support working
- ✅ Integration with AI assistants successful

## 🎉 Ready to Publish!

**Current Status**: All prerequisites met, package built and ready.

**Next Command**: 
```bash
python scripts/publish_to_pypi.py
```

This will make MCP Ngobrol available to the world! 🌍
