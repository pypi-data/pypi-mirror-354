#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Ngobrol v1.0.4
==================

Server MCP untuk ngobrol interaktif dengan AI - Fork dan pengembangan lanjutan dengan identitas Indonesia.

Development by: MBPR
Fork dari: mcp-feedback-enhanced (Minidoracat) → interactive-feedback-mcp (Fábio Ferreira)

Fitur v1.0.4:
- Rebranding ke "MCP Ngobrol" dengan identitas Indonesia
- Default Bahasa Indonesia untuk pengalaman yang natural
- Qt GUI interface yang powerful dan user-friendly
- Enhanced performance dan memory management
- Fungsionalitas eksekusi perintah
- Dukungan upload gambar
- Professional Qt design
- Arsitektur modular yang dioptimasi
- Package name: mcp-ngobrol
"""

__version__ = "1.0.4"
__author__ = "MBPR"
__email__ = "mbpr.dev@gmail.com"

import os

from .server import main as run_server

# Import modul GUI
feedback_ui = None
try:
    from .gui import feedback_ui
except ImportError:
    # Jika dependensi GUI tidak tersedia, set ke None
    feedback_ui = None

# Antarmuka export utama
__all__ = [
    "run_server",
    "feedback_ui",
    "__version__",
    "__author__",
]

def main():
    """Entry point utama untuk eksekusi uvx"""
    from .__main__ import main as cli_main
    return cli_main()