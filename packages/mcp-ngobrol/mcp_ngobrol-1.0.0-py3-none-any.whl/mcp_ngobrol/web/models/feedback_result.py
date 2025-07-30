#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Data Hasil Umpan Balik Web UI
====================================

Mendefinisikan struktur data pengumpulan umpan balik, konsisten dengan versi GUI.
"""

from typing import TypedDict, List


class FeedbackResult(TypedDict):
    """Definisi tipe hasil umpan balik"""
    command_logs: str
    interactive_feedback: str
    images: List[dict]