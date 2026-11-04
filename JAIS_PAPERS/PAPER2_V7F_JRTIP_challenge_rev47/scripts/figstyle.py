"""
Shared figure style of Paper2_V47, following the artwork rules of The Visual Computer (Springer):
sans-serif lettering (Liberation Sans, metric-compatible with Arial) at 8 pt final size with minimal
size variance, lines of at least 0.3 pt, RGB color with patterns or marker shapes so that every
series is also clear in black and white, lettering with high contrast, and figures drawn at their
final width (column 76 mm or text width 160 mm of the template), so nothing is rescaled.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

COL_IN = 216.24094 / 72.27   # \columnwidth of sn-jnl iicol (76.0 mm)
TEXT_IN = 455.24408 / 72.27  # \textwidth (160.0 mm)
FS = 8                       # lettering size, pt

# Okabe-Ito colorblind-safe colors (RGB); gray for the host alone
BLUE, ORANGE, VERMILION, GRAY, DARK = "#0072B2", "#E69F00", "#D55E00", "#9A9A9A", "#333333"

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.family": "sans-serif", "font.sans-serif": ["Liberation Sans", "Arial", "Helvetica"],
    "font.size": FS, "axes.labelsize": FS, "axes.titlesize": FS, "xtick.labelsize": FS,
    "ytick.labelsize": FS, "legend.fontsize": FS,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "lines.linewidth": 1.0, "hatch.linewidth": 0.6, "patch.linewidth": 0.6,
    "text.color": "black", "axes.labelcolor": "black", "xtick.color": "black", "ytick.color": "black",
    "axes.spines.top": False, "axes.spines.right": False,
    "savefig.bbox": "standard", "figure.dpi": 600, "savefig.dpi": 600,
})
