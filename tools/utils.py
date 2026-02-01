"""
utils.py

General helper utilities for ActiFlow AI.

This file contains small, reusable helper functions
that do not belong to any core module.
"""

import os


def normalize_path(path: str) -> str:
    """
    Normalize and clean a filesystem path.

    - Expands user paths (~)
    - Converts to absolute path
    - Removes redundant separators

    This helps keep paths consistent across the project.
    """
    if not path:
        return ""

    return os.path.abspath(os.path.expanduser(path))
