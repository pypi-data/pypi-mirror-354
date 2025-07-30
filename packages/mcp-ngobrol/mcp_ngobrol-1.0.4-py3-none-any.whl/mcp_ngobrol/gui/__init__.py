"""
Modul GUI Koleksi Umpan Balik Interaktif
=========================================

Modul antarmuka pengguna grafis berbasis PySide6, menyediakan fungsionalitas pengumpulan umpan balik yang intuitif.
Mendukung input teks, upload gambar, eksekusi perintah, dan fungsi lainnya.

Struktur Modul:
- main.py: Entry point antarmuka utama
- window/: Kelas jendela
- widgets/: Komponen kustom
- styles/: Definisi gaya
- utils/: Fungsi utilitas
- models/: Model data

Penulis: Fábio Ferreira
Sumber Inspirasi: dotcursorrules.com
Fitur Enhanced: Dukungan gambar dan desain antarmuka modern
Dukungan Multi-bahasa: MBPR
Refaktor: Desain modular
"""

from .main import feedback_ui, feedback_ui_with_timeout

__all__ = ['feedback_ui', 'feedback_ui_with_timeout'] 