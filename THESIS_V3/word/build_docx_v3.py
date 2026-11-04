"""
Builds the Word thesis from the previous Word edition (used as the template)
and the converted LaTeX content (prep_latex.py + pandoc).

  python THESIS_V3/word/build_docx_v3.py <previous_thesis.docx> <conv_dir> <out.docx> [indexes.json]

The front pages, abstract, acknowledgments, abbreviations and Arabic summary of
the previous edition are kept; the contents and lists are rebuilt, and the
chapters, references and publications are replaced by the current source.
"""
from __future__ import annotations

import copy
import sys

from build_docx import Builder, qn, text_of


class BuilderV3(Builder):
    def __init__(self, template, conv, indexes=None):
        super().__init__(template, conv, indexes)
        kids = list(self.body)

        def style(k):
            ppr = k.find(qn("w:pPr")) if k.tag == qn("w:p") else None
            st = ppr.find(qn("w:pStyle")) if ppr is not None else None
            return st.get(qn("w:val")) if st is not None else None
        h1 = next(k for k in kids if style(k) == "Heading1")
        self.proto = {"h1": copy.deepcopy(h1)}

    def caption(self, kind, num, runs):
        cap, desc = super().caption(kind, num, runs)
        st = cap.find(qn("w:pPr")).find(qn("w:pStyle"))
        st.set(qn("w:val"), "thesisfigures" if kind == "fig" else "thesistables")
        return cap, desc

    def front(self):
        pass

    def abstract_and_ack(self):
        pass

    def abbreviations(self):
        pass

    def arabic_summary(self):
        pass

    def front_layout(self):
        pass

    def toc_fields(self):
        body = self.body
        sdt = body.find(qn("w:sdt"))
        content = sdt.find(qn("w:sdtContent"))
        ps = content.findall(qn("w:p"))
        instr = next(it.text for p in ps for it in p.iter(qn("w:instrText")) if it.text and "TOC" in it.text)
        for p in ps[1:]:
            content.remove(p)
        f1, f2 = self.field_paragraphs(instr, "TOC1")
        content.append(f1)
        content.append(f2)
        for key in ("thesis figures", "thesis tables"):
            kids = list(body)
            start = next(i for i, k in enumerate(kids)
                         if any(key in (it.text or "") for it in k.iter(qn("w:instrText"))))
            depth, end = 0, None
            for j in range(start, len(kids)):
                for fc in kids[j].iter(qn("w:fldChar")):
                    typ = fc.get(qn("w:fldCharType"))
                    depth += 1 if typ == "begin" else (-1 if typ == "end" else 0)
                    if depth == 0 and typ == "end":
                        end = j
                        break
                if end is not None:
                    break
            instr = next(it.text for it in kids[start].iter(qn("w:instrText")) if key in (it.text or ""))
            self.replace_block(kids[start], kids[end], self.field_paragraphs(instr, "TableofFigures"))


if __name__ == "__main__":
    BuilderV3(sys.argv[1], sys.argv[2], sys.argv[4] if len(sys.argv) > 4 else None).build(sys.argv[3])
