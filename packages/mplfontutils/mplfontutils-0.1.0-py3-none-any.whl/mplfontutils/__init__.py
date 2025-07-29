"""
Font Utility Package for Matplotlib

This package provides utilities for testing and loading fonts in matplotlib.
"""

from .core import load_fonts_from_directory, find_available_fonts

__version__ = "0.1.0"

__all__ = ["load_fonts_from_directory", "find_available_fonts"]
