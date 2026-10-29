"""
Builds the Word thesis from the previous Word edition (used as the template)
and the converted LaTeX content (prep_latex.py + pandoc).

  python THESIS_V4/word/build_docx_v3.py <previous_thesis.docx> <conv_dir> <out.docx> [indexes.json]

The front pages, abstract, acknowledgments, abbreviations and Arabic summary of
the previous edition are kept; the contents and lists are rebuilt, and the
chapters, references and publications are replaced by the current source.
"""
from __future__ import annotations

import copy
import sys

from build_docx import AR_TITLE, TITLE, Builder, qn, run, set_size, tab_run, text_of


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

    def publications(self):
        out = super().publications()
        note = ("The first publication forms the basis of Chapter 2, the second of Chapter 3, "
                "and the third of Chapter 4.")
        out.append(self.para([run(note)], style="Normal", jc="both", after=160, first_line=0, line=276))
        return out

    def front(self):
        """Replace the thesis title of the previous edition on the English and Arabic title pages."""
        old = {"Training-Free Adaptive Control of Detector and Tracker Operating Points for Multi-Object Tracking": TITLE,
               "التحكم التكيفي دون تدريب في نقاط تشغيل الكاشف والمتتبع لتتبع الأجسام المتعددة": AR_TITLE}
        n = 0
        for p in self.body.iter(qn("w:p")):
            t = text_of(p).strip()
            if t in old:
                self.replace_paragraph_text(p, old[t])
                n += 1
        assert n == 3, n
        # the shorter title frees space on the cover: start the inner title page on a new page
        mtc = [p for p in self.body.iter(qn("w:p")) if text_of(p).strip() == "Military Technical College"
               and p.getnext() is not None
               and text_of(p.getnext()).strip() == "Chair of Computing Engineering and Artificial Intelligence"]
        assert len(mtc) == 2, len(mtc)
        ppr = mtc[1].find(qn("w:pPr"))
        if ppr is None:
            ppr = mtc[1].makeelement(qn("w:pPr"), {})
            mtc[1].insert(0, ppr)
        if ppr.find(qn("w:pageBreakBefore")) is None:
            ppr.append(ppr.makeelement(qn("w:pageBreakBefore"), {}))

    def abstract_and_ack(self):
        pass

    def abbreviations(self):
        kids = list(self.body)
        start = next(i for i, k in enumerate(kids) if i > 0 and text_of(k).strip() == "Abbreviations"
                     and text_of(kids[i - 1]).strip() == "List of Abbreviations")
        end = next(i for i in range(start + 1, len(kids)) if kids[i].tag == qn("w:p")
                   and kids[i].find(qn("w:pPr")) is not None
                   and kids[i].find(qn("w:pPr")).find(qn("w:sectPr")) is not None)
        new = []
        for block in self.side["abbreviations"]:
            for a, b in block["rows"]:
                runs = set_size(self.snippet(a), 24) + [tab_run()] + set_size(self.snippet(b), 24)
                new.append(self.para(runs, style="Normal", after=40, tabs=[("left", 1900)], left=1900,
                                     hanging=1900, line=264))
        self.replace_block(kids[start + 1], kids[end - 1], new)

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
