#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modul Model Data Web UI
=======================

Mendefinisikan struktur data dan tipe yang terkait dengan Web UI.
"""

from .feedback_session import WebFeedbackSession, SessionStatus, CleanupReason
from .feedback_result import FeedbackResult

__all__ = [
    'WebFeedbackSession',
    'SessionStatus',
    'CleanupReason',
    'FeedbackResult'
]