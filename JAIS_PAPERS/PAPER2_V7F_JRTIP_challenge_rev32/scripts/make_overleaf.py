"""
Build the Overleaf package of Paper2_V32 after pdflatex + bibtex of main.tex:
for_overleaf/main.tex with every \\input file inlined and the bibliography embedded, the
Springer Nature class and style, and the figure PDFs; then Paper2_V32_overleaf.zip. The delivered
Paper2_V32.pdf is compiled from for_overleaf/main.tex itself, so the PDF and the zip are the same file.

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev32/scripts/make_overleaf.py
"""
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

V = Path(__file__).resolve().parents[1]
OUT = V / "for_overleaf"
ZIP = V / "Paper2_V32_overleaf.zip"


def inline(text: str) -> str:
    def rep(m):
        name = m.group(1)
        p = V / (name if name.endswith(".tex") else name + ".tex")
        return "% --- " + name + "\n" + inline(p.read_text(encoding="utf-8")).rstrip("\n")
    return re.sub(r"\\input\{([^}]+)\}", rep, text)


src = inline((V / "main.tex").read_text(encoding="utf-8"))
bbl = (V / "main.bbl").read_text(encoding="utf-8")
cmd = "\\bibliography{references}"
assert src.count(cmd) == 1
src = src.replace(cmd, "% Bibliography embedded so that this file compiles on its own.\n" + bbl.rstrip("\n"))
assert "\\input{" not in src
OUT.mkdir(exist_ok=True)
(OUT / "main.tex").write_text(src, encoding="utf-8")
figs = sorted(set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", src)))
files = {"main.tex": OUT / "main.tex"}
for name in ("sn-jnl.cls", "sn-mathphys-num.bst"):
    shutil.copyfile(V / name, OUT / name)
    files[name] = OUT / name
for f in figs:
    (OUT / f).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(V / f, OUT / f)
    files[f] = OUT / f
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for arc, p in files.items():
        z.write(p, arc)
print(f"wrote {OUT / 'main.tex'} and {ZIP.name}: {sorted(files)}")
for _ in range(3):
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], cwd=OUT, capture_output=True, check=False)
log = (OUT / "main.log").read_text(encoding="utf-8", errors="ignore")
assert "Overfull" not in log and "undefined" not in log.lower() and "\n! " not in log, "for_overleaf build is not clean"
shutil.copyfile(OUT / "main.pdf", V / "Paper2_V32.pdf")
print("wrote Paper2_V32.pdf from for_overleaf/main.tex")
