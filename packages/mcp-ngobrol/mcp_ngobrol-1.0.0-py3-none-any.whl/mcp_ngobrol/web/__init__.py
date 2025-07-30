#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modul Web UI
============

Menyediakan antarmuka pengguna Web berbasis FastAPI, dirancang khusus untuk lingkungan pengembangan SSH remote.
Mendukung input teks, upload gambar, eksekusi perintah, dan fungsi lainnya, serta mengacu pada pola desain GUI.
"""

from .main import WebUIManager, launch_web_feedback_ui, get_web_ui_manager, stop_web_ui

__all__ = [
    'WebUIManager',
    'launch_web_feedback_ui', 
    'get_web_ui_manager',
    'stop_web_ui'
] 