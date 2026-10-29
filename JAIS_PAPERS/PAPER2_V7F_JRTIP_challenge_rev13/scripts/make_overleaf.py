"""
Build the Overleaf package of Paper2_V13 after pdflatex + bibtex of main.tex:
for_overleaf/main.tex with every \\input file inlined and the bibliography embedded, the
Springer Nature class and style, and the figure PDFs; then Paper2_V13_overleaf.zip.

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev13/scripts/make_overleaf.py
"""
import re
import shutil
import zipfile
from pathlib import Path

V = Path(__file__).resolve().parents[1]
OUT = V / "for_overleaf"
ZIP = V / "Paper2_V13_overleaf.zip"


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
