#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Data Hasil Umpan Balik
=============================

Mendefinisikan struktur data pengumpulan umpan balik.
"""

from typing import TypedDict, List


class FeedbackResult(TypedDict):
    """Definisi tipe hasil umpan balik"""
    command_logs: str
    interactive_feedback: str
    images: List[dict]