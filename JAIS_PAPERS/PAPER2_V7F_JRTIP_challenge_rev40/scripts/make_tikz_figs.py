"""
Figs. 1 (architecture), 3 (running time) and 4 (AOB comparison) of Paper2_V40 as standalone PDF files
(sources figures/Fig1.tex, Fig6.tex, Fig2.tex with
figures/fig_preamble.tex): Helvetica lettering at final size, compiled with pdflatex, fonts embedded.
Same content and numbers as the inline TikZ figures of Paper2_V27.

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev40/scripts/make_tikz_figs.py
"""
import shutil
import subprocess
from pathlib import Path

V = Path(__file__).resolve().parents[1]
F = V / "figures"
# source figures/<name>.tex -> published file (numbered by order of appearance in Paper2_V40)
for n, out in (("Fig1", "Fig1.pdf"),):
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{n}.tex"], cwd=F, capture_output=True, text=True)
    log = (F / f"{n}.log").read_text(errors="ignore")
    assert r.returncode == 0 and "\n! " not in log, f"{n} failed"
    shutil.copyfile(F / f"{n}.pdf", V / out)
    print("wrote", out, "from", n + ".tex")
