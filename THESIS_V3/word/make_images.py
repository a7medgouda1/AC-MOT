"""
Renders the figures (PDF -> PNG, 300 dpi) and the algorithms (algorithmic
blocks with resolved references -> standalone PDF -> PNG) listed in
<out>/prep/side.json into <out>/fig/.

  python THESIS_V3/word/make_images.py <out_dir>
"""
import json
import subprocess
import sys
from pathlib import Path

THESIS = Path(__file__).resolve().parents[1]

ALG_TEMPLATE = r"""\documentclass[12pt,varwidth=15.5cm,border=6pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{algpseudocode}
\algrenewcommand\algorithmicrequire{\textbf{Input:}}
\algrenewcommand\algorithmicensure{\textbf{Output:}}
\begin{document}
%s
\end{document}
"""


def main(out_dir):
    out = Path(out_dir)
    side = json.loads((out / "prep/side.json").read_text())
    fig = out / "fig"
    alg = out / "algsrc"
    fig.mkdir(parents=True, exist_ok=True)
    alg.mkdir(parents=True, exist_ok=True)
    for key, f in side["figures"].items():
        src = THESIS / f["src"]["pdf"]
        subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", str(src),
                        str(fig / ("fig" + key.replace(".", "_")))], check=True)
    for key, a in side["algos"].items():
        name = f"alg{key}"
        (alg / f"{name}.tex").write_text(ALG_TEMPLATE % a["latex"])
        subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{name}.tex"], cwd=alg, capture_output=True)
        log = (alg / f"{name}.log").read_text(errors="ignore")
        assert "\n! " not in log and "Overfull" not in log, f"{name} did not build cleanly"
        subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", str(alg / f"{name}.pdf"), str(fig / name)],
                       check=True)
    print("figures", len(side["figures"]), "algorithms", len(side["algos"]))


if __name__ == "__main__":
    main(sys.argv[1])
