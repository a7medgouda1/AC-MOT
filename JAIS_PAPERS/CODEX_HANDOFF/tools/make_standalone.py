"""Embed the compiled bibliography into main.tex so it compiles on its own.

Usage: python make_standalone.py main.tex main.bbl out/main.tex
Run after pdflatex + bibtex on the multi-file version.
"""
import sys

src, bbl, out = sys.argv[1:4]
s = open(src, encoding="utf-8").read()
b = open(bbl, encoding="utf-8").read()
cmd = "\\bibliography{references}"
assert s.count(cmd) == 1, "expected exactly one \\bibliography{references}"
s = s.replace(cmd, "% Bibliography is embedded so that this file compiles on its own.\n" + b.rstrip("\n"))
open(out, "w", encoding="utf-8").write(s)
print("written", out)
