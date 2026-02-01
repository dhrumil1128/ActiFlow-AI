"""
filesystem.py

This file contains low-level filesystem operations.
These functions are intentionally simple and predictable.
"""

import os

# It’s a Python module for file and folder operations like copy, move, delete.
import shutil


def create_folder(path: str) -> None:
    """
    Create a folder at the given path.

    If the folder already exists, nothing happens.
    """
    os.makedirs(path, exist_ok=True)


def move_file(source: str, destination: str) -> None:
    """
    Move a file from source to destination.
    """
    shutil.move(source, destination)


def rename_file(source: str, destination: str) -> None:
    """
    Rename a file from source to destination.
    """
    os.rename(source, destination)
