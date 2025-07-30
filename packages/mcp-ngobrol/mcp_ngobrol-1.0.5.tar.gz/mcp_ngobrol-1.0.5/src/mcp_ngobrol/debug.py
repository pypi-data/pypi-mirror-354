#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modul Log Debug Terpadu
=======================

Menyediakan fungsionalitas log debug terpadu, memastikan output debug tidak mengganggu komunikasi MCP.
Semua output debug akan dikirim ke stderr, dan hanya output saat mode debug diaktifkan.

Cara Penggunaan:
```python
from .debug import debug_log

debug_log("Ini adalah informasi debug")
```

Kontrol Variabel Lingkungan:
- MCP_DEBUG=true/1/yes/on: Aktifkan mode debug
- MCP_DEBUG=false/0/no/off: Nonaktifkan mode debug (default)

Penulis: MBPR
"""

import os
import sys
from typing import Any


def debug_log(message: Any, prefix: str = "DEBUG") -> None:
    """
    Output pesan debug ke standard error, menghindari polusi standard output

    Args:
        message: Informasi debug yang akan dioutput
        prefix: Identifikasi prefix informasi debug, default "DEBUG"
    """
    # Hanya output saat mode debug diaktifkan, menghindari gangguan komunikasi MCP
    if not os.getenv("MCP_DEBUG", "").lower() in ("true", "1", "yes", "on"):
        return

    try:
        # Pastikan pesan adalah tipe string
        if not isinstance(message, str):
            message = str(message)

        # Output aman ke stderr, menangani masalah encoding
        try:
            print(f"[{prefix}] {message}", file=sys.stderr, flush=True)
        except UnicodeEncodeError:
            # Jika mengalami masalah encoding, gunakan mode aman ASCII
            safe_message = message.encode('ascii', errors='replace').decode('ascii')
            print(f"[{prefix}] {safe_message}", file=sys.stderr, flush=True)
    except Exception:
        # Rencana cadangan terakhir: gagal diam, tidak mempengaruhi program utama
        pass


def gui_debug_log(message: Any) -> None:
    """Log debug khusus modul GUI"""
    debug_log(message, "GUI")


def i18n_debug_log(message: Any) -> None:
    """Log debug khusus modul internasionalisasi"""
    debug_log(message, "I18N")


def server_debug_log(message: Any) -> None:
    """Log debug khusus modul server"""
    debug_log(message, "SERVER")


def web_debug_log(message: Any) -> None:
    """Log debug khusus modul Web UI"""
    debug_log(message, "WEB")


def is_debug_enabled() -> bool:
    """Periksa apakah mode debug diaktifkan"""
    return os.getenv("MCP_DEBUG", "").lower() in ("true", "1", "yes", "on")


def set_debug_mode(enabled: bool) -> None:
    """Set mode debug (untuk testing)"""
    os.environ["MCP_DEBUG"] = "true" if enabled else "false"