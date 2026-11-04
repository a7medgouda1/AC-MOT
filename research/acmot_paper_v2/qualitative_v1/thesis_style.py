"""
Common look of the thesis figures drawn from video frames: Times New Roman (the font of the thesis text)
and STIX mathematics, and a display gamma for night frames. The gamma acts on every pixel of every panel
of a figure in the same way, so the two pipelines are always shown on identical frames.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

FONT_DIRS = [Path("/usr/share/fonts/truetype/msttcorefonts")]


def apply():
    import matplotlib
    from matplotlib import font_manager
    for d in FONT_DIRS:
        for f in sorted(d.glob("*.[tT][tT][fF]")):
            font_manager.fontManager.addfont(str(f))
    matplotlib.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
                                "mathtext.fontset": "stix", "pdf.fonttype": 42})


def brighten(img: np.ndarray, gamma: float) -> np.ndarray:
    """img: uint8 RGB. gamma > 1 lifts the dark tones; gamma = 1 returns the frame unchanged."""
    if gamma == 1.0:
        return img
    lut = np.clip(255.0 * (np.arange(256) / 255.0) ** (1.0 / gamma) + 0.5, 0, 255).astype(np.uint8)
    return lut[img]
