#!/bin/sh
# Builds the Word thesis and its PDF from the LaTeX source of THESIS_V2.
#
#   sh THESIS_V2/word/build_all.sh <template.docx> <work_dir>
#
# <template.docx>: the faculty thesis template (Word file whose layout, front pages and
# styles are reused). Needs pdflatex, bibtex, pandoc (PANDOC=... to choose the binary),
# LibreOffice with its Python 'uno' module (/usr/bin/python3), and python-docx.
set -e
TEMPLATE="$1"
WORK="$2"
PANDOC="${PANDOC:-pandoc}"
HERE="$(cd "$(dirname "$0")" && pwd)"
THESIS="$(dirname "$HERE")"
mkdir -p "$WORK"

# 1. LaTeX build: numbers of sections, figures, tables, equations, citations; bibliography
(cd "$THESIS/figures" && for f in tbd_pipeline outline score_stages acmot_pipeline acmot_visdrone_bars acmot_uavdt_bars; do
   pdflatex -interaction=nonstopmode "$f.tex" >/dev/null; done)
(cd "$THESIS" && pdflatex -interaction=nonstopmode main.tex >/dev/null && bibtex main >/dev/null \
   && pdflatex -interaction=nonstopmode main.tex >/dev/null && pdflatex -interaction=nonstopmode main.tex >/dev/null)
! grep -q "^! " "$THESIS/main.log"
! grep -qi "undefined" "$THESIS/main.log"

# 2. Marked LaTeX + side data, pandoc conversion, images
python3 "$HERE/prep_latex.py" "$WORK/prep"
for f in body abstract acknowledgments snippets refs; do
  "$PANDOC" -f latex -t docx "$WORK/prep/$f.tex" -o "$WORK/prep/$f.docx"
done
python3 "$HERE/make_images.py" "$WORK"

# 3. Two passes: the first gives the page numbers of the contents and the lists
python3 "$HERE/build_docx.py" "$TEMPLATE" "$WORK" "$WORK/pass1.docx"
/usr/bin/python3 "$HERE/update_fields.py" "$WORK/pass1.docx" "$WORK/indexes1.json" "$WORK/pass1.pdf"
python3 "$HERE/build_docx.py" "$TEMPLATE" "$WORK" "$WORK/thesis.docx" "$WORK/indexes1.json"

# 4. PDF of the final file as it is (its contents and lists already hold the page numbers)
(cd "$WORK" && soffice --headless --convert-to pdf thesis.docx >/dev/null 2>&1)
echo "built $WORK/thesis.docx and $WORK/thesis.pdf"
