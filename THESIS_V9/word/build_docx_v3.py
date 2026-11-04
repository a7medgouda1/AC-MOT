"""
Builds the Word thesis from the previous Word edition (used as the template)
and the converted LaTeX content (prep_latex.py + pandoc).

  python THESIS_V9/word/build_docx_v3.py <previous_thesis.docx> <conv_dir> <out.docx> [indexes.json]

The front pages, abstract, acknowledgments, abbreviations and Arabic summary of
the previous edition are kept; the contents and lists are rebuilt, and the
chapters, references and publications are replaced by the current source.
"""
from __future__ import annotations

import copy
import re
import sys

from build_docx import (AR_TITLE, THESIS, TITLE, Builder, clean_runs, pandoc_paragraphs, qn, run, set_size,
                        strip_prefix, tab_run, text_of)


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
        # degree line on both title pages: "Master of Science in Computer Engineering"
        fixed = 0
        for p in self.body.iter(qn("w:p")):
            if " ".join(text_of(p).split()) != "Master of Science In Computer Engineering":
                continue
            for r in p.findall(qn("w:r")):
                ts = r.findall(qn("w:t"))
                if len(ts) == 1 and ts[0].text == "In":
                    ts[0].text = "in"
                    fixed += 1
        assert fixed == 2, fixed
        # date of discussion: the day and month stay drop-down fields of the template, shown as blanks
        # to be filled in, in the color of the page and without highlight
        date = [p for p in self.body.iter(qn("w:p")) if text_of(p).strip().startswith("Date of Discussion")]
        assert len(date) == 1, len(date)
        blanks = {"choose day": "_____", "choose month": "________"}
        n = 0
        for sdt in date[0].iter(qn("w:sdt")):
            pr = sdt.find(qn("w:sdtPr"))
            alias = pr.find(qn("w:alias"))
            name = alias.get(qn("w:val")) if alias is not None else ""
            if name in blanks:
                ph = pr.find(qn("w:showingPlcHdr"))
                if ph is not None:
                    pr.remove(ph)
                ts = list(sdt.find(qn("w:sdtContent")).iter(qn("w:t")))
                ts[0].text = blanks[name]
                for t in ts[1:]:
                    t.text = ""
                n += 1
        assert n == 2, n
        for rpr in date[0].iter(qn("w:rPr")):
            for tag in ("w:highlight", "w:color", "w:rStyle"):
                for x in rpr.findall(qn(tag)):
                    rpr.remove(x)

    def abstract_and_ack(self):
        """Replace the abstract and the acknowledgments of the previous edition by the current source."""
        kids = list(self.body)
        start = next(i for i, k in enumerate(kids) if text_of(k).strip() == "Abstract")
        end = next(i for i in range(start + 1, len(kids)) if text_of(kids[i]).strip() == "Acknowledgments")
        ab = [strip_prefix(clean_runs(p), 0) for p in pandoc_paragraphs(self.conv / "prep/abstract.docx")]
        ab = [r for r in ab if r]
        new = [self.para(r, after=200, first_line=720, line=360) for r in ab]
        new[-1].find(qn("w:pPr")).find(qn("w:ind")).set(qn("w:firstLine"), "0")
        self.replace_block(kids[start + 1], kids[end - 1], new)
        # acknowledgments: paragraphs between the heading and the signature
        kids = list(self.body)
        head = next(i for i, k in enumerate(kids) if text_of(k).strip() == "Acknowledgments")
        sign = next(i for i in range(head + 1, len(kids)) if text_of(kids[i]).strip() == "Ahmed Gouda Ismail")
        ac = [clean_runs(p) for p in pandoc_paragraphs(self.conv / "prep/acknowledgments.docx")]
        ac = [r for r in ac if r]
        assert len(ac) == 3 and sign - head - 1 == 3, (len(ac), sign - head - 1)
        self.replace_block(kids[head + 1], kids[sign - 1],
                           [self.para(r, after=200, first_line=720, line=360) for r in ac])
        # signature block: name and place each on one line, centered on the right part of the page
        kids = list(self.body)
        head = next(i for i, k in enumerate(kids) if text_of(k).strip() == "Acknowledgments")
        sign = next(i for i in range(head + 1, len(kids)) if text_of(kids[i]).strip() == "Ahmed Gouda Ismail")
        for k in (kids[sign], kids[sign + 1]):
            assert text_of(k).strip() in ("Ahmed Gouda Ismail", "Cairo 2026"), text_of(k)
            ind = k.find(qn("w:pPr")).find(qn("w:ind"))
            ind.set(qn("w:left"), "4320")

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
        # the page heading "List of Abbreviations" is enough: drop the repeated "Abbreviations" line
        kids = list(self.body)
        sub = kids[start]
        heading = kids[start - 1]
        for be in sub.findall(qn("w:bookmarkEnd")):
            heading.append(be)
        sub.getparent().remove(sub)
        first = kids[start + 1]
        first.find(qn("w:pPr")).find(qn("w:spacing")).set(qn("w:before"), "240")

    def arabic_summary(self):
        """Replace the paragraphs of the Arabic summary page of the previous edition."""
        src = (THESIS / "arabic/arabic_summary.tex").read_text()
        body = src.split("\\thispagestyle{empty}", 1)[1].split("\\clearpage", 1)[0]
        body = re.sub(r"\\foreignlanguage\{english\}\{([^}]*)\}", r"\1", body)
        body = re.sub(r"\\vspace\{[^}]*\}|\\noindent", "", body)
        paras = [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip()]
        kids = list(self.body)
        i = next(i for i, k in enumerate(kids) if text_of(k).strip() == "ملخص الرسالة")
        j = i + 1
        while j < len(kids) and text_of(kids[j]).strip():
            j += 1
        proto = kids[i + 1]
        base = proto.find(qn("w:r")).find(qn("w:rPr"))
        new = []
        for t in paras:
            p = copy.deepcopy(proto)
            for r in p.findall(qn("w:r")):
                p.remove(r)
            p.append(run(re.sub(r"\s+", " ", t), base_rpr=base))
            new.append(p)
        assert len(new) == j - (i + 1), (len(new), j - i - 1)
        self.replace_block(kids[i + 1], kids[j - 1], new)
        # the page break that follows the summary sits in its own paragraph; keep that paragraph
        # one point high so that a full summary page never pushes it onto an empty page
        brk = new[-1].getnext()
        assert brk.tag == qn("w:p") and not text_of(brk).strip()
        assert any(b.get(qn("w:type")) == "page" for b in brk.iter(qn("w:br")))
        ppr = brk.find(qn("w:pPr"))
        sp = ppr.makeelement(qn("w:spacing"), {qn("w:before"): "0", qn("w:after"): "0",
                                               qn("w:line"): "20", qn("w:lineRule"): "exact"})
        ppr.insert(0, sp)
        for rpr in brk.iter(qn("w:rPr")):
            for tag in ("w:sz", "w:szCs"):
                for x in rpr.findall(qn(tag)):
                    x.set(qn("w:val"), "2")

    def front_layout(self):
        pass

    def fill_indexes(self):
        """Fill the contents and lists, then link every entry to its heading or caption."""
        super().fill_indexes()
        norm = lambda x: re.sub(r"\s+", "", x)
        styles = {"Heading1", "Heading1Title", "Heading2", "Heading3", "thesisfigures", "thesistables",
                  "myfiguresibrahim", "mytablesibrahim"}
        sdt = self.body.find(qn("w:sdt"))
        targets = []
        for p in self.body.iter(qn("w:p")):
            ppr = p.find(qn("w:pPr"))
            st = ppr.find(qn("w:pStyle")) if ppr is not None else None
            if st is not None and st.get(qn("w:val")) in styles and text_of(p).strip():
                targets.append([p, norm(text_of(p)), False])
        entries = []
        for p in self.body.iter(qn("w:p")):
            ppr = p.find(qn("w:pPr"))
            st = ppr.find(qn("w:pStyle")) if ppr is not None else None
            if st is None or st.get(qn("w:val")) not in ("TOC1", "TOC2", "TOC3", "TableofFigures"):
                continue
            runs = [r for r in p.findall(qn("w:r")) if r.find(qn("w:fldChar")) is None
                    and r.find(qn("w:instrText")) is None]
            if not any(r.find(qn("w:tab")) is not None for r in runs):
                continue
            title = ""
            for r in runs:
                if r.find(qn("w:tab")) is not None:
                    break
                title += "".join(t.text or "" for t in r.iter(qn("w:t")))
            entries.append((p, runs, norm(title)))
        bid, linked = 9000, 0
        for p, runs, key in entries:
            key = key[:40]
            hit = next((t for t in targets if not t[2] and t[0] is not p and t[1].startswith(key)), None)
            if hit is None:
                hit = next((t for t in targets if t[0] is not p and t[1].startswith(key)), None)
            if hit is None:
                continue
            tgt = hit[0]
            if not hit[2]:
                bid += 1
                name = f"_Toc{bid}"
                bs = tgt.makeelement(qn("w:bookmarkStart"), {qn("w:id"): str(bid), qn("w:name"): name})
                be = tgt.makeelement(qn("w:bookmarkEnd"), {qn("w:id"): str(bid)})
                ppr = tgt.find(qn("w:pPr"))
                (ppr.addnext(bs) if ppr is not None else tgt.insert(0, bs))
                tgt.append(be)
                hit[2] = name
            h = p.makeelement(qn("w:hyperlink"), {qn("w:anchor"): hit[2], qn("w:history"): "1"})
            runs[0].addprevious(h)
            for r in runs:
                h.append(r)
            linked += 1
        print("linked entries", linked, "of", len(entries))

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
