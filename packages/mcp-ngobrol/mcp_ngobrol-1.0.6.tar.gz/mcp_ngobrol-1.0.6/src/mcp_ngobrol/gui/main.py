#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry Point Utama GUI
======================

Menyediakan fungsi entry point utama untuk antarmuka umpan balik GUI.
"""

import threading
import time
from typing import Optional
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFont
from PySide6.QtCore import QTimer
import sys

from .models import FeedbackResult
from .window import FeedbackWindow


def feedback_ui(project_directory: str, summary: str) -> Optional[FeedbackResult]:
    """
    Meluncurkan antarmuka GUI pengumpulan umpan balik

    Args:
        project_directory: Jalur direktori proyek
        summary: Ringkasan pekerjaan AI

    Returns:
        Optional[FeedbackResult]: Hasil umpan balik, mengembalikan None jika pengguna membatalkan
    """
    # Periksa apakah sudah ada instance QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Set font global Microsoft JhengHei
    font = QFont("Microsoft JhengHei", 11)  # Microsoft JhengHei, 11pt
    app.setFont(font)

    # Set urutan fallback font, memastikan font Indonesia ditampilkan dengan benar
    app.setStyleSheet("""
        * {
            font-family: "Segoe UI", "Microsoft JhengHei", "微軟正黑體", "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", sans-serif;
        }
    """)

    # Buat jendela utama
    window = FeedbackWindow(project_directory, summary)
    window.show()

    # Jalankan event loop sampai jendela ditutup
    app.exec()

    # Kembalikan hasil
    return window.result


def feedback_ui_with_timeout(project_directory: str, summary: str, timeout: int) -> Optional[FeedbackResult]:
    """
    Meluncurkan antarmuka GUI pengumpulan umpan balik dengan timeout

    Args:
        project_directory: Jalur direktori proyek
        summary: Ringkasan pekerjaan AI
        timeout: Waktu timeout (detik) - waktu timeout yang diteruskan MCP, sebagai batas maksimum

    Returns:
        Optional[FeedbackResult]: Hasil umpan balik, mengembalikan None jika pengguna membatalkan atau timeout

    Raises:
        TimeoutError: Dilempar saat timeout
    """
    # Periksa apakah sudah ada instance QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Set font global Microsoft JhengHei
    font = QFont("Microsoft JhengHei", 11)  # Microsoft JhengHei, 11pt
    app.setFont(font)

    # Set urutan fallback font, memastikan font Indonesia ditampilkan dengan benar
    app.setStyleSheet("""
        * {
            font-family: "Segoe UI", "Microsoft JhengHei", "微軟正黑體", "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", sans-serif;
        }
    """)

    # Buat jendela utama, teruskan waktu timeout MCP
    window = FeedbackWindow(project_directory, summary, timeout)

    # Hubungkan sinyal timeout
    timeout_occurred = False
    def on_timeout():
        nonlocal timeout_occurred
        timeout_occurred = True

    window.timeout_occurred.connect(on_timeout)

    window.show()

    # Mulai countdown timeout pengaturan pengguna (jika diaktifkan)
    window.start_timeout_if_enabled()

    # Buat timer timeout MCP sebagai backup
    mcp_timeout_timer = QTimer()
    mcp_timeout_timer.setSingleShot(True)
    mcp_timeout_timer.timeout.connect(lambda: _handle_mcp_timeout(window, app))
    mcp_timeout_timer.start(timeout * 1000)  # Konversi ke milidetik

    # Jalankan event loop sampai jendela ditutup
    app.exec()

    # Hentikan timer (jika masih berjalan)
    mcp_timeout_timer.stop()
    window.stop_timeout()

    # Periksa apakah timeout
    if timeout_occurred:
        raise TimeoutError(f"Pengumpulan umpan balik timeout, antarmuka GUI telah ditutup otomatis")
    elif hasattr(window, '_timeout_occurred'):
        raise TimeoutError(f"Pengumpulan umpan balik timeout ({timeout} detik), antarmuka GUI telah ditutup otomatis")

    # Kembalikan hasil
    return window.result


def _handle_timeout(window: FeedbackWindow, app: QApplication) -> None:
    """Menangani event timeout (versi lama, dipertahankan untuk kompatibilitas mundur)"""
    # Tandai timeout terjadi
    window._timeout_occurred = True
    # Paksa tutup jendela
    window.force_close()
    # Keluar dari aplikasi
    app.quit()


def _handle_mcp_timeout(window: FeedbackWindow, app: QApplication) -> None:
    """Menangani event timeout MCP (mekanisme backup)"""
    # Tandai timeout terjadi
    window._timeout_occurred = True
    # Paksa tutup jendela
    window.force_close()
    # Keluar dari aplikasi
    app.quit()