"""
Figs. 1, 2 and 6 of Paper2_V28 as standalone PDF files (figures/Fig1.tex, Fig2.tex, Fig6.tex with
figures/fig_preamble.tex): Helvetica lettering at final size, compiled with pdflatex, fonts embedded.
Same content and numbers as the inline TikZ figures of Paper2_V27.

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev28/scripts/make_tikz_figs.py
"""
import shutil
import subprocess
from pathlib import Path

V = Path(__file__).resolve().parents[1]
F = V / "figures"
for n in ("Fig1", "Fig2", "Fig6"):
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{n}.tex"], cwd=F, capture_output=True, text=True)
    log = (F / f"{n}.log").read_text(errors="ignore")
    assert r.returncode == 0 and "\n! " not in log, f"{n} failed"
    shutil.copyfile(F / f"{n}.pdf", V / f"{n}.pdf")
    print("wrote", n + ".pdf")
