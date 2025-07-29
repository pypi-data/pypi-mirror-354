"""
Core functionality for font utilities in matplotlib.
"""

import logging
import os
import re
import warnings
from typing import Optional, Set

import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager


def load_fonts_from_directory(directory: str) -> int:
    """
    Load custom fonts from a specified directory.

    This function recursively searches the given directory for font files
    (.ttf and .otf) and adds them to matplotlib's font manager.

    Args:
        directory (str): Path to the directory containing font files

    Returns:
        int: Number of fonts loaded.

    Example:
        >>> load_fonts_from_directory("/path/to/fonts")
    """
    if not os.path.exists(directory):
        logging.warning(f"Font directory '{directory}' does not exist.")
        return 0

    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".otf", ".ttf")):
                fontManager.addfont(os.path.join(root, file))
                logging.debug(f"Loaded font: {file}")
                count += 1

    return count


glyph_missing_pattern = re.compile(r"Glyph (\d+) \(.*\) missing from font\(s\) (.+)\.")


def find_available_fonts(test_text: str, output_file: Optional[str] = None) -> Set[str]:
    """
    Find fonts that can display the given text.

    Args:
        test_text (str): Text to test font compatibility.
        output_file (str, optional): Path to save visualization.

    Returns:
        Set[str]: Fonts compatible with the text.
    """
    fonts = set(fontManager.get_font_names())

    # Create a figure to test font rendering
    fig, ax = plt.subplots()
    for font in fonts:
        ax.text(0, 0, test_text, fontname=font)

    # Render the figure to trigger warnings
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        fig.canvas.draw()
    plt.close(fig)

    fonts -= set(m.group(2) for m in (re.match(glyph_missing_pattern, str(w.message)) for w in caught_warnings) if m)

    # Create visualization if output_file is provided
    fs = 10  # Font size in points
    w = fs / 100  # Convert font size to width
    if output_file and fonts:
        fig, ax = plt.subplots(figsize=(w * (max(map(len, fonts)) + 4), 2 * w))
        for i, font in enumerate(fonts):
            ax.text(0, i, font, fontsize=fs)
            ax.text(1, i, test_text, fontname=font, fontsize=fs)
        ax.set_axis_off()
        fig.savefig(output_file, bbox_inches="tight", pad_inches=w, dpi=300)

    return fonts
