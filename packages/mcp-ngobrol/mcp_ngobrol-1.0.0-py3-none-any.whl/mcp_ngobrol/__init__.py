#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Ngobrol v1.0.0
==================

Server MCP untuk ngobrol interaktif dengan AI - Fork dan pengembangan lanjutan dengan identitas Indonesia.

Development by: MBPR
Fork dari: mcp-feedback-enhanced (Minidoracat) → interactive-feedback-mcp (Fábio Ferreira)

Fitur v1.0.0:
- Rebranding ke "MCP Ngobrol" dengan identitas Indonesia
- Default Bahasa Indonesia untuk pengalaman yang natural
- Dukungan antarmuka ganda (Qt GUI dan Web UI)
- Deteksi lingkungan cerdas
- Fungsionalitas eksekusi perintah
- Dukungan upload gambar
- Tema gelap modern yang diperbaiki
- Arsitektur modular yang dioptimasi
- Package name: mcp-ngobrol
"""

__version__ = "1.0.0"
__author__ = "MBPR"
__email__ = "mbpr.dev@gmail.com"

import os

from .server import main as run_server

# Import modul Web UI baru
from .web import WebUIManager, launch_web_feedback_ui, get_web_ui_manager, stop_web_ui

# Import kondisional modul GUI (hanya import jika tidak dipaksa menggunakan Web)
feedback_ui = None
if not os.getenv('FORCE_WEB', '').lower() in ('true', '1', 'yes'):
    try:
        from .gui import feedback_ui
    except ImportError:
        # Jika dependensi GUI tidak tersedia, set ke None
        feedback_ui = None

# Antarmuka export utama
__all__ = [
    "run_server",
    "feedback_ui",
    "WebUIManager",
    "launch_web_feedback_ui",
    "get_web_ui_manager",
    "stop_web_ui",
    "__version__",
    "__author__",
]

def main():
    """Entry point utama untuk eksekusi uvx"""
    from .__main__ import main as cli_main
    return cli_main()