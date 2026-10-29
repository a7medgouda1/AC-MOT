#!/bin/sh
# Builds the Word thesis and its PDF from the LaTeX source of THESIS_V6.
#
#   sh THESIS_V6/word/build_all.sh <template.docx> <work_dir>
#
# <template.docx>: the previous Word edition of the thesis, THESIS_V3/word/Thesis_Ahmed_Gouda_Ismail.docx
# (its layout, front pages and styles are reused; the file itself is only read). Needs pdflatex, bibtex, pandoc (PANDOC=... to choose the binary),
# LibreOffice Writer and Math with the Python 'uno' module (/usr/bin/python3), and python-docx.
set -e
TEMPLATE="$1"
WORK="$2"
PANDOC="${PANDOC:-pandoc}"
PY="${PYTHON:-python3}"   # a Python with python-docx
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
"$PY" "$HERE/build_docx_v3.py" "$TEMPLATE" "$WORK" "$WORK/pass1.docx"
/usr/bin/python3 "$HERE/update_fields.py" "$WORK/pass1.docx" "$WORK/indexes1.json" "$WORK/pass1.pdf"
"$PY" "$HERE/build_docx_v3.py" "$TEMPLATE" "$WORK" "$WORK/thesis.docx" "$WORK/indexes1.json"
"$PY" "$HERE/build_toc_docx.py" "$WORK/indexes1.json" "$WORK/Thesis_Table_of_Contents.docx"

# 4. PDF of the final file as it is (its contents and lists already hold the page numbers)
(cd "$WORK" && soffice --headless --convert-to pdf thesis.docx >/dev/null 2>&1 && soffice --headless --convert-to pdf Thesis_Table_of_Contents.docx >/dev/null 2>&1)
# 5. Versioned deliverables (THESIS_V<n> -> Thesis_V<n>.*)
V="$(basename "$THESIS" | sed 's/^THESIS_//')"
cp "$WORK/thesis.docx" "$THESIS/word/Thesis_$V.docx"
cp "$WORK/thesis.pdf" "$THESIS/word/Thesis_$V.pdf"
cp "$WORK/Thesis_Table_of_Contents.docx" "$THESIS/word/Thesis_${V}_Table_of_Contents.docx"
cp "$THESIS/main.pdf" "$THESIS/Thesis_${V}_LaTeX.pdf"
echo "built $THESIS/word/Thesis_$V.docx, Thesis_$V.pdf, Thesis_${V}_Table_of_Contents.docx and Thesis_${V}_LaTeX.pdf"
