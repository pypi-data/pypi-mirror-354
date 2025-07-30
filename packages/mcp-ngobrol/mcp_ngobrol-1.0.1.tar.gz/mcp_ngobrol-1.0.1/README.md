# MCP Ngobrol

**🗣️ MCP server untuk ngobrol interaktif dengan AI - Enhanced feedback system dengan dual UI support**

**🌐 Language / 語言切換:** **English** | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md) | [Bahasa Indonesia](README.id.md)

**Original Author:** [Fábio Ferreira](https://x.com/fabiomlferreira) | [Original Project](https://github.com/noopstudios/interactive-feedback-mcp) ⭐
**Enhanced Fork:** [MBPR](https://github.com/mbprcc) | **Version:** 1.0.0
**UI Design Reference:** [sanshao85/mcp-feedback-collector](https://github.com/sanshao85/mcp-feedback-collector)

## 🚀 MBPRCC Enhanced Features

### 🎯 What Makes This Fork Special?

**MCP Ngobrol** adalah versi yang telah di-tuning dan di-enhance oleh **MBPRCC** dengan fokus pada:

1. **🇮🇩 Indonesian-First Experience**
   - Default bahasa Indonesia untuk semua interface
   - Pesan error dan debug dalam bahasa Indonesia
   - Dokumentasi lengkap dalam bahasa Indonesia

2. **🛠️ Production-Ready Stability**
   - Enhanced error handling dan recovery
   - Memory management yang lebih baik
   - Auto-cleanup untuk session dan temporary files
   - Connection stability improvements

3. **🎨 Improved User Experience**
   - Auto-focus pada input field
   - Better responsive design
   - Consistent spacing dan padding
   - Professional UI/UX improvements

4. **⚡ Performance Optimizations**
   - Faster startup time
   - Reduced memory footprint
   - Optimized WebSocket connections
   - Better resource management

5. **🔧 Developer-Friendly**
   - Comprehensive testing suite
   - Better debugging tools
   - Detailed logging system
   - Easy configuration management

## 🎯 Core Concept

**MCP Ngobrol** adalah [MCP server](https://modelcontextprotocol.io/) yang memungkinkan **ngobrol interaktif dengan AI** melalui feedback-oriented development workflows. Sempurna untuk lingkungan lokal, **SSH Remote** (Cursor SSH Remote, VS Code Remote SSH), dan **WSL (Windows Subsystem for Linux)**. Dengan memandu AI untuk konfirmasi dengan user daripada operasi spekulatif, sistem ini menggabungkan multiple tool calls menjadi single feedback request, secara dramatis mengurangi biaya platform dan meningkatkan efisiensi development.

**Supported Platforms:** [Cursor](https://www.cursor.com) | [Cline](https://cline.bot) | [Windsurf](https://windsurf.com) | [Augment](https://www.augmentcode.com) | [Trae](https://www.trae.ai)

### 🔄 Perbedaan Detail dengan Original Project

| Fitur | Original Project | MBPRCC Enhanced | Benefit |
|-------|------------------|-----------------|---------|
| **Default Language** | English | 🇮🇩 **Bahasa Indonesia** | Better UX untuk developer Indonesia |
| **Error Messages** | English only | Indonesian + English | Easier debugging |
| **Debug Output** | Mixed languages | Konsisten Indonesian | Cleaner development experience |
| **UI Polish** | Basic | **Professional design** | Better user experience |
| **Memory Management** | Standard | **Enhanced monitoring** | Prevents memory leaks |
| **Auto-cleanup** | Manual | **Automatic** | Maintenance-free operation |
| **Connection Stability** | Basic | **Production-grade** | Reliable for production use |
| **Testing Suite** | Limited | **Comprehensive** | Better code quality |
| **Documentation** | English only | **Bilingual (ID/EN)** | Accessible untuk semua developer |
| **Configuration** | Complex | **Simplified setup** | Faster deployment |
| **Checkpoint System** | ❌ None | ✅ **Auto + Manual** | Progress tracking & recovery |
| **Memory Bank** | ❌ None | ✅ **Automatic** | Project state persistence |
| **Auto-focus** | ❌ None | ✅ **Enhanced** | Better input experience |
| **Responsive Design** | Basic | ✅ **Professional** | Works on all screen sizes |
| **Error Recovery** | Basic | ✅ **Advanced** | Graceful error handling |

### 🔄 Workflow Ngobrol
1. **AI Call** → `mcp-ngobrol`
2. **Environment Detection** → Auto-select appropriate interface
3. **User Ngobrol** → Command execution, text feedback, image upload
4. **Feedback Delivery** → Information returns to AI
5. **Process Continuation** → Adjust or end based on ngobrol

## 🌟 Key Features

### 🖥️ Dual Interface System
- **Qt GUI**: Native experience for local environments, modular refactored design
- **Web UI**: Modern interface for remote SSH and WSL environments, brand new architecture
- **Smart Switching**: Auto-detect environment (local/remote/WSL) and choose optimal interface

### 🎨 Brand New Interface Design (v2.1.0)
- **Modular Architecture**: Both GUI and Web UI adopt modular design
- **Centralized Management**: Reorganized folder structure for easier maintenance
- **Modern Themes**: Improved visual design and user experience
- **Responsive Layout**: Adapts to different screen sizes and window dimensions

### 🖼️ Image Support
- **Format Support**: PNG, JPG, JPEG, GIF, BMP, WebP
- **Upload Methods**: Drag & drop files + clipboard paste (Ctrl+V)
- **Auto Processing**: Smart compression to ensure 1MB limit compliance

### 🌏 Multi-language
- **Four Languages**: Indonesian, English, Traditional Chinese, Simplified Chinese
- **Smart Detection**: Auto-select based on system language
- **Live Switching**: Change language directly within interface

### ✨ WSL Environment Support (v2.2.5)
- **Auto Detection**: Intelligently identifies WSL (Windows Subsystem for Linux) environments
- **Browser Integration**: Automatically launches Windows browser in WSL environments
- **Multiple Launch Methods**: Supports `cmd.exe`, `powershell.exe`, `wslview` and other browser launch methods
- **Seamless Experience**: WSL users can directly use Web UI without additional configuration

### 🌐 SSH Remote Environment Support (v2.3.0 New Feature)
- **Smart Detection**: Automatically identifies SSH Remote environments (Cursor SSH Remote, VS Code Remote SSH, etc.)
- **Browser Launch Guidance**: Provides clear solutions when browser cannot launch automatically
- **Port Forwarding Support**: Complete port forwarding setup guidance and troubleshooting
- **MCP Integration Optimization**: Improved integration with MCP system for more stable connection experience
- **Detailed Documentation**: [SSH Remote Environment Usage Guide](docs/en/ssh-remote/browser-launch-issues.md)
- 🎯 **Auto-focus Input Box**: Automatically focus on feedback input box when window opens, improving user experience (Thanks @penn201500)
  
## 🖥️ Interface Preview

### Qt GUI Interface (Refactored Version)
<div align="center">
  <img src="docs/en/images/gui1.png" width="400" alt="Qt GUI Main Interface" />
  <img src="docs/en/images/gui2.png" width="400" alt="Qt GUI Settings Interface" />
</div>

*Qt GUI Interface - Modular refactoring, supporting local environments*

### Web UI Interface (Refactored Version)
<div align="center">
  <img src="docs/en/images/web1.png" width="400" alt="Web UI Main Interface" />
  <img src="docs/en/images/web2.png" width="400" alt="Web UI Settings Interface" />
</div>

*Web UI Interface - Brand new architecture, suitable for SSH Remote environments*

**Keyboard Shortcuts**
- `Ctrl+Enter` (Windows/Linux) / `Cmd+Enter` (macOS): Submit feedback (supports both main keyboard and numpad)
- `Ctrl+V` (Windows/Linux) / `Cmd+V` (macOS): Directly paste clipboard images

## 🚀 Quick Start

### 1. Installation & Testing
```bash
# Install uv (jika belum terinstall)
pip install uv

# Quick test dengan MBPRCC enhanced version
uvx mcp-ngobrol@latest test
```

### 2. MCP Configuration

#### 🎯 **Recommended MBPRCC Configuration**
**Untuk Augment Code IDE** (Production-ready):
```json
{
  "mcpServers": {
    "mcp-ngobrol-dev": {
      "command": "python",
      "args": ["c:/project/mcp-feedback-enhanced-2.3.0/run_mcp_simple.py"],
      "timeout": 600,
      "env": {
        "MCP_LANGUAGE": "id",
        "MCP_DEBUG": "false",
        "PYTHONIOENCODING": "utf-8"
      },
      "autoApprove": ["interactive_feedback_mcp-ngobrol-dev"]
    }
  }
}
```

#### 📦 **Package Installation Configuration**
**Basic Configuration** (untuk most users):
```json
{
  "mcpServers": {
    "mcp-ngobrol": {
      "command": "uvx",
      "args": ["mcp-ngobrol@latest"],
      "timeout": 600,
      "env": {
        "MCP_LANGUAGE": "id",
        "MCP_DEBUG": "false"
      },
      "autoApprove": ["interactive_feedback"]
    }
  }
}
```

#### ⚙️ **Advanced Configuration**
**Untuk custom environment dan debugging**:
```json
{
  "mcpServers": {
    "mcp-ngobrol": {
      "command": "uvx",
      "args": ["mcp-ngobrol@latest"],
      "timeout": 600,
      "env": {
        "FORCE_WEB": "true",
        "MCP_DEBUG": "true",
        "MCP_LANGUAGE": "id",
        "PYTHONIOENCODING": "utf-8"
      },
      "autoApprove": ["interactive_feedback"]
    }
  }
}
```

### 3. Prompt Engineering Setup

#### 🎯 **MBPRCC Recommended Prompt Rules**
Untuk hasil terbaik, tambahkan rules ini ke AI assistant Anda:

```
# MCP Ngobrol Interactive Feedback Rules - MBPRCC Enhanced

RULES PALING UTAMA! SELALU GUNAKAN MCP FEEDBACK SEBELUM MENUTUP CONVERSATIONS ATAU MENYELESAIKAN TASK!

1. Selama proses apapun, task, atau conversation, baik bertanya, merespons, atau menyelesaikan stage tasks, HARUS call MCP mcp-ngobrol.
2. Ketika menerima user feedback, jika feedback content tidak kosong, HARUS call MCP mcp-ngobrol lagi dan adjust behavior berdasarkan feedback.
3. Hanya ketika user secara eksplisit menunjukkan "end" atau "tidak perlu interaksi lagi" baru boleh berhenti call MCP mcp-ngobrol.
4. Kecuali menerima end command, semua steps harus berulang kali call MCP mcp-ngobrol.
5. Sebelum menyelesaikan task, gunakan MCP mcp-ngobrol untuk meminta feedback user.
6. Gunakan bahasa Indonesia sebagai default untuk komunikasi dengan user.
```

#### 📋 **Additional MBPRCC Rules**
```
# MBPRCC Enhanced Workflow Rules

1. MEMORY BANK: Pada awal SETIAP tugas, periksa keberadaan Memory Bank. Jika tidak ada, buat otomatis.
2. CHECKPOINT: Gunakan checkpoint system untuk tracking progress dan recovery.
3. ERROR HANDLING: Gunakan enhanced error handling dengan pesan dalam bahasa Indonesia.
4. TESTING: Selalu suggest testing setelah implementasi code changes.
5. DOCUMENTATION: Update dokumentasi setelah perubahan signifikan.
```

## ⚙️ Advanced Settings

### 🔧 MBPRCC Enhanced Environment Variables
| Variable | Purpose | Values | Default | MBPRCC Enhancement |
|----------|---------|--------|---------|-------------------|
| `MCP_LANGUAGE` | **Interface language** | `id`/`en`/`zh-CN`/`zh-TW` | `id` | **🇮🇩 Indonesian default** |
| `FORCE_WEB` | Force use Web UI | `true`/`false` | `false` | Auto-detection improved |
| `MCP_DEBUG` | Debug mode | `true`/`false` | `false` | **Indonesian debug messages** |
| `MCP_WEB_PORT` | Web UI port | `1024-65535` | `8765` | Better port management |
| `PYTHONIOENCODING` | **Character encoding** | `utf-8` | `utf-8` | **🆕 Prevents garbled text** |

### 🎯 MBPRCC Specific Features
| Feature | Description | Usage |
|---------|-------------|-------|
| **Memory Bank** | Automatic project state tracking | Auto-created on first run |
| **Checkpoint System** | Progress tracking and recovery | Manual and auto checkpoints |
| **Enhanced Error Handling** | Indonesian error messages | Better user experience |
| **Auto-cleanup** | Automatic session cleanup | Prevents memory leaks |
| **Connection Monitoring** | WebSocket stability tracking | Auto-reconnection |

### 🧪 MBPRCC Enhanced Testing Options
```bash
# Version check
uvx mcp-ngobrol@latest version       # Check MBPRCC version

# Interface-specific testing dengan Indonesian output
uvx mcp-ngobrol@latest test --gui    # Quick test Qt GUI
uvx mcp-ngobrol@latest test --web    # Test Web UI (auto continuous running)

# Debug mode dengan Indonesian messages
MCP_DEBUG=true MCP_LANGUAGE=id uvx mcp-ngobrol@latest test
```

### 🛠️ Developer Installation (MBPRCC Enhanced)
```bash
# Clone MBPRCC enhanced version
git clone https://github.com/mbprcc/mcp-ngobrol.git
cd mcp-ngobrol
uv sync

# Setup development environment
uv run python -m mcp_ngobrol test
```

### 🔬 **MBPRCC Local Testing Methods**
```bash
# Method 1: Standard test (recommended untuk daily development)
uv run python -m mcp_ngobrol test

# Method 2: Complete test suite dengan MBPRCC enhancements
uvx --with-editable . mcp-ngobrol test

# Method 3: Interface-specific testing
uvx --with-editable . mcp-ngobrol test --gui    # Quick test Qt GUI
uvx --with-editable . mcp-ngobrol test --web    # Test Web UI (auto continuous running)

# Method 4: MBPRCC specific testing
MCP_LANGUAGE=id uvx --with-editable . mcp-ngobrol test    # Indonesian interface test
```

### 📊 **MBPRCC Testing Descriptions**
- **Standard Test**: Complete functionality check dengan Indonesian output
- **Complete Test**: Deep testing semua components dengan MBPRCC enhancements
- **Qt GUI Test**: Quick launch dan test local graphical interface
- **Web UI Test**: Start Web server dan keep running untuk complete Web functionality testing
- **Indonesian Test**: Test dengan interface bahasa Indonesia dan enhanced error handling

## 🆕 Version History

📋 **Complete Version History:** [RELEASE_NOTES/CHANGELOG.en.md](RELEASE_NOTES/CHANGELOG.en.md) | [CHANGELOG.id.md](RELEASE_NOTES/CHANGELOG.id.md)

### 🚀 MBPRCC Enhanced Version (v1.0.0)
**🎯 Major MBPRCC Enhancements:**
- 🇮🇩 **Indonesian-First Experience**: Default bahasa Indonesia untuk semua interface dan error messages
- 🛡️ **Production-Ready Stability**: Enhanced error handling, memory management, dan auto-cleanup
- 🎨 **Professional UI/UX**: Improved spacing, padding, responsive design, dan auto-focus features
- ⚡ **Performance Optimizations**: Faster startup, reduced memory footprint, optimized connections
- 🔧 **Developer-Friendly**: Comprehensive testing suite, better debugging, detailed logging
- 📊 **Memory Bank System**: Automatic project state tracking dan checkpoint management
- 🌐 **Enhanced Connection Stability**: Improved WebSocket handling dan auto-reconnection
- 📝 **Bilingual Documentation**: Comprehensive documentation dalam Indonesian dan English

### Original Version Highlights (v2.3.0)
- 🌐 **SSH Remote Environment Support**: Solved Cursor SSH Remote browser launch issues with clear usage guidance
- 🛡️ **Error Message Improvements**: Provides more user-friendly error messages and solution suggestions when errors occur
- 🧹 **Auto-cleanup Features**: Automatically cleans temporary files and expired sessions to keep the system tidy
- 📊 **Memory Monitoring**: Monitors memory usage to prevent system resource shortage
- 🔧 **Connection Stability**: Improved Web UI connection stability and error handling

## 🐛 Common Issues

### 🌐 SSH Remote Environment Issues
**Q: Browser cannot launch in SSH Remote environment**
A: This is normal behavior. SSH Remote environments have no graphical interface, requiring manual opening in local browser. For detailed solutions, see: [SSH Remote Environment Usage Guide](docs/en/ssh-remote/browser-launch-issues.md)

**Q: Why am I not receiving new MCP feedback?**
A: There might be a WebSocket connection issue. **Solution**: Simply refresh the browser page.

**Q: Why isn't MCP being called?**
A: Please confirm the MCP tool status shows green light. **Solution**: Toggle the MCP tool on/off repeatedly, wait a few seconds for system reconnection.

**Q: Augment cannot start MCP**
A: **Solution**: Completely close and restart VS Code or Cursor, then reopen the project.

### 🔧 General Issues
**Q: Getting "Unexpected token 'D'" error**
A: Debug output interference. Set `MCP_DEBUG=false` or remove the environment variable.

**Q: Chinese character garbled text**
A: Fixed in v2.0.3. Update to latest version: `uvx mcp-feedback-enhanced@latest`

**Q: Multi-screen window disappearing or positioning errors**
A: Fixed in v2.1.1. Go to "⚙️ Settings" tab, check "Always show window at primary screen center" to resolve. Especially useful for T-shaped screen arrangements and other complex multi-monitor configurations.

**Q: Image upload fails**
A: Check file size (≤1MB) and format (PNG/JPG/GIF/BMP/WebP).

**Q: Web UI won't start**
A: Set `FORCE_WEB=true` or check firewall settings.

**Q: UV Cache taking up too much disk space**
A: Due to frequent use of `uvx` commands, cache may accumulate to tens of GB. Regular cleanup is recommended:
```bash
# Check cache size and detailed information
python scripts/cleanup_cache.py --size

# Preview cleanup content (without actually cleaning)
python scripts/cleanup_cache.py --dry-run

# Execute standard cleanup
python scripts/cleanup_cache.py --clean

# Force cleanup (attempts to close related processes, solves Windows file lock issues)
python scripts/cleanup_cache.py --force

# Or use uv command directly
uv cache clean
```
For detailed instructions, see: [Cache Management Guide](docs/en/cache-management.md)

**Q: AI models cannot parse images**
A: Various AI models (including Gemini Pro 2.5, Claude, etc.) may have instability in image parsing, sometimes correctly identifying and sometimes unable to parse uploaded image content. This is a known limitation of AI visual understanding technology. Recommendations:
1. Ensure good image quality (high contrast, clear text)
2. Try uploading multiple times, retries usually succeed
3. If parsing continues to fail, try adjusting image size or format

## 🙏 Acknowledgments

### 🌟 Support Original Author
**Fábio Ferreira** - [X @fabiomlferreira](https://x.com/fabiomlferreira)
**Original Project:** [noopstudios/interactive-feedback-mcp](https://github.com/noopstudios/interactive-feedback-mcp)

If you find this useful, please:
- ⭐ [Star the original project](https://github.com/noopstudios/interactive-feedback-mcp)
- 📱 [Follow the original author](https://x.com/fabiomlferreira)

### Design Inspiration
**sanshao85** - [mcp-feedback-collector](https://github.com/sanshao85/mcp-feedback-collector)

### Contributors
**penn201500** - [GitHub @penn201500](https://github.com/penn201500)
- 🎯 Auto-focus input box feature (Original contribution)

### 🌟 MBPRCC Community Support
- **Discord:** [https://social.mbpr.cc/mbprdiscord](https://social.mbpr.cc/mbprdiscord)
- **Issues:** [GitHub Issues](https://github.com/mbprcc/mcp-ngobrol/issues)
- **Documentation:** [MBPRCC Docs](https://github.com/mbprcc/mcp-ngobrol/docs)
- **Website:** [https://mbpr.cc](https://mbpr.cc)

## 🎯 Cara Menggunakan MBPRCC Enhanced Version

### 1. **Quick Setup untuk Augment Code IDE**
```bash
# Clone repository
git clone https://github.com/mbprcc/mcp-ngobrol.git
cd mcp-ngobrol

# Install dependencies
uv sync

# Test installation dengan Indonesian interface
MCP_LANGUAGE=id uv run python -m mcp_ngobrol test
```

### 2. **Konfigurasi MCP di Augment**
Tambahkan ke `mcp.json`:
```json
{
  "mcpServers": {
    "mcp-ngobrol-dev": {
      "command": "python",
      "args": ["c:/project/mcp-feedback-enhanced-2.3.0/run_mcp_simple.py"],
      "env": {
        "MCP_LANGUAGE": "id",
        "MCP_DEBUG": "false",
        "PYTHONIOENCODING": "utf-8"
      },
      "autoApprove": ["interactive_feedback_mcp-ngobrol-dev"]
    }
  }
}
```

### 3. **Menggunakan MBPRCC Enhanced Features**

#### 🏦 **Memory Bank System**
```python
# Otomatis dibuat saat pertama kali digunakan
# Menyimpan project state, teknologi, dan progress
# File: memory_bank/project_state.md
```

#### 📍 **Checkpoint System**
```python
# Manual checkpoint
create_checkpoint_mcp-ngobrol-dev(
    name="Feature Implementation Complete",
    description="Selesai implementasi fitur login",
    tags="feature,login,complete"
)

# Auto checkpoint (otomatis saat task start/end)
```

#### 🇮🇩 **Indonesian Interface**
```python
# Set bahasa Indonesia (default)
MCP_LANGUAGE=id

# Error messages dalam bahasa Indonesia
# Debug output dalam bahasa Indonesia
# GUI text dalam bahasa Indonesia
```

#### 🔧 **Enhanced Error Handling**
```python
# Error messages yang lebih jelas
# Suggestion untuk solution
# Recovery options
# Graceful degradation
```

#### 🧹 **Auto-cleanup Features**
```python
# Automatic session cleanup
# Memory monitoring
# Temporary file cleanup
# Resource management
```

### 4. **MBPRCC Specific Tools**

#### 📊 **Memory & Session Management**
```python
# Check memory statistics
get_session_memory_stats_mcp-ngobrol-dev()

# Analyze conversation context
analyze_conversation_context_mcp-ngobrol-dev()

# Enhanced response with memory
enhance_response_with_memory_mcp-ngobrol-dev()
```

#### 🎯 **Auto-completion System**
```python
# Enable auto-completion
enable_auto_completion_mcp-ngobrol-dev()

# Check completion triggers
check_completion_trigger_mcp-ngobrol-dev()

# Get auto-completion status
get_auto_completion_status_mcp-ngobrol-dev()
```

#### 📋 **Checkpoint Management**
```python
# List all checkpoints
list_checkpoints_mcp-ngobrol-dev()

# Restore from checkpoint
restore_checkpoint_mcp-ngobrol-dev(checkpoint_id="...")

# Create manual checkpoint
create_checkpoint_mcp-ngobrol-dev()
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---
**🌟 MBPRCC Enhanced - Welcome to Star and share with more developers!**