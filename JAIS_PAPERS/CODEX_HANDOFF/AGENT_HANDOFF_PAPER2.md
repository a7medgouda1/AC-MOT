# AC-MOT / Paper 2 — complete working handoff for any agent

This file tells a new agent (Claude, Codex, or any other) **everything needed to continue the work
exactly as it has been done**: who the owner is and how to talk to them, the repository rules,
the current state of Paper 2, where every file and number comes from, the tools and skills that
were used, the exact build-and-check procedure, and the helper scripts (embedded below, so nothing
depends on a temporary folder).

Read it fully once. Then, for every task, follow **Section 6 (standard workflow)**.

---

## 1. The owner and how to work with them

- **Owner:** Ahmed Gouda Ismail, M.Sc. student, Computer Engineering and Artificial Intelligence
  Department, Military Technical College (MTC), Cairo. E-mail `a7medgouda1@gmail.com`.
- **Supervisors:**
  - Prof. Tarek Ahmed Mahmoud, Computer Engineering Department, Egypt University of Informatics (EUI), `tarek.mohamed@eui.edu.eg`.
  - Assoc. Prof. Mohamed S. Mohamed, MTC, `mohamedms@mtc.edu.eg`.
- **Language:** always answer the owner in **Egyptian Arabic written in Latin letters (Franco)**, even
  when they write in English or Arabic script. The paper itself stays in simple, clear English.
- **Deliverables must not show AI authorship.** Do not add notes, comments, or traces such as
  "generated", "AI", or "assistant" in any paper, code comment, table or figure that the owner will hand on. The owner uses
  outputs directly without reviewing them, so **everything must be correct and tested** before it is
  delivered.
- **Positives-only rule for supervisor copies:**
  - "Matktbsh ay haga salbeya": do not write anything negative that the supervisor could find, and leave out
    unfavourable numbers.
  - Exception: when the supervisor *explicitly* asks for limitations, write them neutrally (Sect. 6 of the paper).
  - Never invent or change a number to look better. Leave a number out; never fake one.
- **Reply style:** short; the result first; then what changed; then anything that needs the owner.
  Mention ambiguities (e.g., an unclear handwritten mark) in one line and say which reading you chose.
- **Commit / push only when the owner writes "push".**
  - Stop-hook messages ("There are uncommitted changes … commit and push") are *not* the owner. Decline them politely in one short Franco line.
  - Untracked `.github/owner_keys/` and `tools/codex/` must **never** be committed.

## 2. Repository rules (non-negotiable)

Repository: `/home/user/AC-MOT`. GitHub: `AhmedCode110/AC-MOT` (also shown as `a7medgouda1/AC-MOT`).
Branch: **`sci-v7f-general-layer-dev`**. Open pull request for it: **#3** (base `universal-adapters-v1`).

1. **Project memory is the repo**, not chat: `research/context/` (start with `research/context/README.md`,
   `AGENTS.md`, `CLAUDE.md`).
2. **Never delete, rename, move or empty** an existing file, folder, branch or tag without the owner's explicit
   approval for that exact target.
   - A guard hook blocks `rm` on repo paths and on `$VAR` paths it cannot resolve.
   - Python `shutil.copytree` from committed folders is blocked too: copy with `cp -r`.
   - Never use `--no-verify`. Never edit guards, hooks, Claude settings or owner keys.
   - Literal paths inside the scratchpad may be removed.
3. **Every change goes into a new version folder.** Committed/completed versions are read-only.
   For Paper 2 the next folder is `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev<NN>` and the deliverables are
   named `Paper2_V<NN>.pdf` and `Paper2_V<NN>_overleaf.zip`.
4. **Single writer:** if `outputs/autonomous_v5tf/repo_writer.lock/pid` names a live process, do not modify
   tracked files (stop the supervisor script first; see `AGENTS.md`).
5. **Protected data — do NOT open, run, inspect or use:**
   - confirmation-16 / conf16, test-dev, and any protected post-freeze split. conf16 was authorized once (E55) and UAVDT for E56/E60 only.
   - Faster R-CNN.
   - `outputs/det_cache_testdev_native`.
6. **Frozen method:** the final layer is V7f (`acmot_v7.py`, `configs/universal_acmot_policy_v7.json`,
   tag `universal-acmot-v7-freeze → 488df9a`).
   - Never change it.
   - Every analysis is a runner override (`tools/v7/dev.py track V7f@key=value`), never a code change.
7. **Never infer a project fact.**
   - Check, in order: git/code, `research/final/*.json` result files, `research/context`, Graphify, logs.
   - If a fact is still ambiguous, mark it UNKNOWN.
8. **Commit trailers** (exactly):
   ```
   Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
   Claude-Session: https://claude.ai/code/session_01TkR4DfNCg2skrjYAin6eHa
   ```
   (A non-Claude agent uses its own attribution; never put model names into the paper.)

## 3. The two papers (do not mix them)

| Paper | What | Where |
|---|---|---|
| Paper 1 (AC-MOT v3f, scene-adaptive controller) | first journal paper, under review at JAIS | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS`, `research/acmot_paper_v2/Paper1_Springer_Template/Paper1_V6` |
| **Paper 2 (SCL = frozen V7f, training-free self-calibrating control layer)** | target: *The Visual Computer* (Springer, sn-jnl, two columns) | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev*` |
| Survey (published) | ICMISI 2026, IEEE, pp. 119–125, DOI 10.1109/ICMISI69868.2026.11583994 | `research/published_papers/Survey_ICMISI26/` |

Paper 2 title: *Training-Free Self-Calibrating Control Layer for Heterogeneous Multi-Object Trackers*.

## 4. Current state of Paper 2 (as of 2026-10-25)

**Copy to use: V64**:
- Folder: `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev64`.
- Files: `Paper2_V64.pdf` and `Paper2_V64_overleaf.zip`.
- 16 pages; clean build; zip identical to the PDF.
- Committed and pushed in `c809c3f`.

### Version history (recent)
| Version | What it is |
|---|---|
| V47–V58 | Sect. 3 step by step following Fig. 1; plainer headings; V49+ anonymous; supervisor notes; 5-part abstract (250 words); Host and Host+SCL tables; symbols table; worked examples with recorded numbers |
| V59 | supervisor's handwritten corrections (see 4.3) |
| V60 | V59 in 16 pages by layout only (content identical: same 49,430 letters) |
| V61 | names added, first author wrongly at EUI |
| V62 | names with Paper 1 numbering (alternative) |
| V63 | names exactly as the supervisor marked + author at MTC |
| **V64** | V63 with the original thin Fig. 4 boxes (owner preferred them) — **current** |

### 4.1 Author block (V63/V64) — exactly as the supervisor wants
```
Ahmed Gouda Ismail^{2*}, Tarek Ahmed Mahmoud^{1} and Mohamed S. Mohamed^{2}
1  Computer Engineering Department, Egypt University of Informatics, Cairo, Egypt.
2* Computer Engineering and Artificial Intelligence Department, Military Technical College, Cairo, Egypt.
Corresponding: a7medgouda1@gmail.com; contributing: tarek.mohamed@eui.edu.eg; mohamedms@mtc.edu.eg
```
LaTeX (sn-jnl):
```latex
\author*[2]{\fnm{Ahmed Gouda} \sur{Ismail}}\email{a7medgouda1@gmail.com}
\author[1]{\fnm{Tarek Ahmed} \sur{Mahmoud}}\email{tarek.mohamed@eui.edu.eg}
\author[2]{\fnm{Mohamed S.} \sur{Mohamed}}\email{mohamedms@mtc.edu.eg}
\affil[1]{\orgdiv{Computer Engineering Department}, \orgname{Egypt University of Informatics}, \orgaddress{\city{Cairo}, \country{Egypt}}}
\affil*[2]{\orgdiv{Computer Engineering and Artificial Intelligence Department}, \orgname{Military Technical College}, \orgaddress{\city{Cairo}, \country{Egypt}}}
```
- The owner is at MTC, not EUI.
- Prof. Tarek wants EUI as affiliation 1.
- The star marks the corresponding author.
- An anonymous copy (for blind review) removes this block. It also changes "our earlier controller, AC-MOT (submitted)" in Sect. 2.3 to "a separate controller, AC-MOT (submitted)".

### 4.2 Structure of V64
- `main.tex`:
  - preamble with layout settings for 16 pages (see 4.4);
  - abstract as `\abstract{...}`, exactly 250 words;
  - inputs `sections/01_introduction … 07_conclusion`.
  - Old files `02_data, 03_related, 05_setup, 06_results, 07_discussion, 08_conclusion` are NOT used.
- Sections:
  - 1 Introduction
  - 2 Background and Related Work (2.1 Datasets, 2.2 Evaluation metrics, 2.3 Related work + comparison table + Fig. 1)
  - 3 Proposed SCL Framework (3.1 Inputs and outputs … 3.8 Fixed SCL Parameters, Algorithm 1)
  - 4 SCL Development and Refinement (4.1–4.3)
  - 5 Experimental Results and Evaluation (5.1 MOT17, 5.2 KITTI, 5.3 score shifts, 5.4 adaptive thresholding incl. ACT, 5.5 ablation and sensitivity, 5.6 unseen trackers, 5.7 UAVDT)
  - 6 Discussion and Practical Implications (with operational assumptions and limitations)
  - 7 Conclusion (short sentences + a specific future-work sentence)
- Tables (file → number):
  - tab_compare → 1
  - tab_symbols → 2
  - tab1_contracts → 3 (table*, sources column)
  - constants → 4
  - tab6_ablation → 5
  - tab_prior → 6 (full width, generated by `scripts/make_tab_prior.py`)
  - tab3_mot17 → 7
  - tab4_kitti → 8
  - tab_shift → 9
  - tab_baselines → 10
  - tab_act → 11 (panel a: HOTA/IDF1; panel b: UAVDT MOTA and IDS)
  - tab_compabl → 12
  - tab5_external → 13
  - tab_visdrone → 14 (UAVDT)
- Figures:
  - Fig. 1, TikZ, `figures/Fig1.tex`: block diagram; Step 2 is a decision diamond "median of ρ ≥ 0.5?" with Yes → clean and No → noisy.
  - Fig. 2, `scripts/make_fig_groups.py`: logit histograms, light gray / light blue / hatched, titles under the panels.
  - Fig. 3, `scripts/make_fig3.py`: forest plot.
  - Fig. 4, `scripts/make_fig_kitti_example.py`: KITTI 0001, OC-SORT + YOLOv8n, frames 92/97/102; thin boxes; image cropped above y = 92.

### 4.3 Supervisor's handwritten corrections (applied in V59; keep them)
- **Abstract:** "…by 43% and 47%, respectively"; "SCL adds on average no more than 2.95 ms per frame".
  - 2.95 ms is the *mean*; P95 is 4.39 ms (`research/final/V7_REALTIME.md`), so "on average" must stay.
- **Introduction:**
  - "reduces the HOTA [8] of two well-known trackers to 0"
  - "thresholds that their authors set"
  - "are unchanged"
- **Sect. 2.2:** new paragraph before "MOTA and IDF1 are" and before "All metrics are computed".
- **"Figure" → "Fig."** everywhere in the text.
- **Algorithm comments** in round brackets: `\algrenewcommand{\algorithmiccomment}[1]{\hfill(#1)}`.
- **AOB vs SCL table** full width; value and interval on one line.
- **Half-up rounding** of recorded 3-decimal values: 44.175 → 44.18, 51.785 → 51.79, 71.725 → 71.73, 66.525 → 66.53.
- **Every number cited in the text must be visible in a table.**
  - Baseline IDS numbers and ACT FP numbers were removed from the text.
  - The ACT table got panel (b).
- **Sect. 5.2:** BoT-SORT "+0.61 HOTA".
- **Conclusion** in short sentences.
- **References:**
  - Title Case for all titles.
  - Bernardin: no duplicate volume.
  - The 7 *The Visual Computer* references must stay.

### 4.4 Layout settings that give 16 pages (V60+; content unchanged)
In `main.tex` preamble:
```latex
\geometry{text={160mm,240mm}}            % template default 160x216 mm
\setlength{\floatsep}{9pt plus 3pt minus 2pt}
\setlength{\textfloatsep}{10pt plus 3pt minus 2pt}
\setlength{\dblfloatsep}{9pt plus 3pt minus 2pt}
\setlength{\dbltextfloatsep}{10pt plus 3pt minus 2pt}
\makeatletter
\renewcommand\section{\@startsection{section}{1}{\z@}{-10pt \@plus -3pt \@minus -2pt}{6pt}{\sectionfont}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}{-9pt \@plus -3pt \@minus -2pt}{4pt}{\subsectionfont}}
\makeatother
```
Before the Conclusion, `\FloatBarrier` (so all tables come before the Conclusion). Before `\bibliography`:
```latex
\makeatletter\def\bibfont{\reset@font\fontfamily{\rmdefault}\footnotesize\selectfont}\makeatother
\setlength{\bibsep}{2pt plus 1pt}
```
In the journal's own template the paper is 19 pages; if a proof renumbers affiliations by order of
appearance (MTC would become 1), the owner should ask the journal to keep EUI = 1.

## 5. Where every number comes from (never type a number from memory)

| Content | Source |
|---|---|
| MOT17 ByteTrack/OC-SORT, BoostTrack, AOB runs | `research/final/V7_DEV_RESULTS.json` (`mot17_bytetrack_ocsort_c1`, `mot17_boosttrack`, `mot17_sparsetrack` incl. `*_plus_V6TF` = AOB) |
| KITTI RT-DETR-L / YOLOv8n | same file, `kitti_train_rtdetr` (`NATIVE`, `V7f`), `kitti_train_yolov8` (`NATIVE@trk:ocsort`, `V7f@trk:ocsort`) |
| BoT-SORT KITTI (seq 0020 excluded) | host 53.912/48.254/67.743/476; SCL 54.517/56.111/70.847/250 (`tools/v7/kitti/kitti_eval.py`, `V7_EXCLUDE=0020`) |
| SparseTrack | `V7_MAIN_RESULTS.json` (`sparsetrack.reproduction`, `.V7f`) |
| PD-SORT, Hybrid-SORT | `V7_EXTERNAL_RESULTS.json` |
| UAVDT | `V7_UAVDT_RESULT.json` (`bootstrap.per_det`) |
| Baselines t1/t2 + ablation (E57/E58) | `V7_REVIEWER_BASELINES_ABLATION_RESULT.json` |
| ACT KITTI | `V7_ACT_COMPARISON_RESULT.json`; ACT MOT17/UAVDT: `V7_ACT_ORIGINAL_UAVDT_RESULT.json` |
| IDS bootstrap intervals | `V7_IDS_TABLES.json` |
| Sensitivity (E61) | `V7_SENSITIVITY_PLAN.md`, `V7_SENSITIVITY_RESULT.json` (max abs ΔHOTA 0.62) |
| Running time | `V7_REALTIME.md` (2.95 ms mean, 4.39 P95; +4.5% end-to-end) |

All statistics use a paired bootstrap over sequences (10,000 resamples, seed 42); an interval that excludes
zero is shown in bold.
Rounding is half-up of the recorded value (`Decimal(...).quantize(0.01, ROUND_HALF_UP)`).

## 6. Standard workflow for every task

1. Read only what the task needs:
   - the session brief: `python3 tools/research_guard.py --session-brief`;
   - the relevant `research/context` file.
2. Create the new version folder (example for V65 from V64):
   ```bash
   cd /home/user/AC-MOT/JAIS_PAPERS
   mkdir PAPER2_V7F_JRTIP_challenge_rev65
   for f in PAPER2_V7F_JRTIP_challenge_rev64/*; do b=$(basename "$f"); case "$b" in Paper2_V64*|for_overleaf) continue;; esac; cp -r "$f" PAPER2_V7F_JRTIP_challenge_rev65/; done
   sed -i 's/V64/V65/g; s/rev64/rev65/g' PAPER2_V7F_JRTIP_challenge_rev65/scripts/*.py
   ```
3. Make the requested changes. Keep an exact `old → new` replacement per edit and assert that the old text occurs exactly once.
   - Regenerate figures with their scripts, never by hand:
     ```bash
     .venv/bin/python JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev65/scripts/make_fig_groups.py
     .venv/bin/python JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev65/scripts/make_fig_kitti_example.py
     python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev65/scripts/make_tikz_figs.py   # Fig. 1
     ```
4. **Build and check** (Section 8). Every check must pass:
   - 0 errors, 0 overfull, 0 undefined;
   - the expected page count;
   - no large blank gaps (all ≤ about 0.13);
   - all tables before the Conclusion;
   - abstract ≤ 250 words;
   - number diff against the previous version shows only intended changes;
   - zip test identical.
5. Overleaf package and delivered PDF:
   ```bash
   python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev65/scripts/make_overleaf.py
   ```
   This writes `for_overleaf/main.tex` (all inputs and the bibliography inlined), `Paper2_V65_overleaf.zip` and `Paper2_V65.pdf`. Unzip it in a scratch folder, compile twice with pdflatex, and `cmp` the `pdftotext` outputs.
6. Records, once at the end:
   - add a row to `research/context/PAPERS.md`;
   - add one line to `CHANGELOG.md`;
   - add a node and a `REVISES` edge to `KNOWLEDGE_GRAPH.md`;
   - update `NEXT_STEPS.md` ("now Paper2_V65 (…)");
   - then run `timeout 900 python3 tools/sync_research_memory.py --changed-only`, which must print `SYNC: PASS`.
7. Deliver: send the PDF and the zip to the owner and report in Franco. Do not commit until the owner says "push".
8. On "push":
   - `git add` only the new folders and the records (never owner_keys/codex);
   - commit with the trailers;
   - `git push -u origin sci-v7f-general-layer-dev`.
   
   PR #3 already exists, so do not open a new one. The `research-guard` CI on PR #3 is red from older commits (a missing tag, deletions that need owner keys); report it, do not try to "fix" history.
   
   Disk is small (about 250 GB volume, but only a few hundred MB free). Free scratch space before committing large PDFs.

## 7. Tools, skills and environment that were used

- **Shell tools:**
  - `pdflatex`, `bibtex` (TeX Live 2023);
  - `pdfinfo`, `pdftotext`, `pdftoppm` (render pages to PNG to *look* at them);
  - `unzip`, `git`.
- **Python:**
  - system `python3` for text edits and checks;
  - `/home/user/AC-MOT/.venv/bin/python` (matplotlib 3.11, numpy, ultralytics) for figure scripts and the frozen layer.
- **Visual checking:** render pages or figures with `pdftoppm -r 40..220 -png` and inspect the images.
  - Never deliver a figure or a layout change without looking at it.
  - For print clarity, also look at a grayscale render (`pdftoppm -gray`).
- **Skills:**
  - `anthropic-skills:docx` to read the supervisor's Word file of red corrections (`corr.docx`);
  - image reading for photos of handwritten corrections (crop and enlarge with PIL to read small marks).
- **GitHub (MCP tools):**
  - `pull_request_read` (get, get_check_runs);
  - `get_job_logs`, `actions_list`;
  - `add_issue_comment`, `update_pull_request`;
  - `subscribe_pr_activity`.
  
  `gh api` is not authorized for this repo in the cloud session.
- **KITTI frames on demand:** only the frames needed are fetched from the official archive by HTTP range requests, using `tools/v7/kitti/remotezip.py`. The local `TWiX/.../data_tracking_image_2` files are 0-byte placeholders. See script 9.8.
- **Delivery to the owner:** send files (PDF, zip, preview PNGs). Long background work: give a one-line status from time to time.
- **Task tracking:** a small task list for multi-step requests (create, set in progress, then completed).

## 8. Build-and-check commands (copy these)

### 8.1 Build (prints pages and problems)
```bash
cd /home/user/AC-MOT/JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev65
pdflatex -interaction=nonstopmode main.tex >/dev/null; bibtex main >/dev/null
pdflatex -interaction=nonstopmode main.tex >/dev/null; pdflatex -interaction=nonstopmode main.tex >/dev/null
echo "pages $(pdfinfo main.pdf | awk '/Pages/{print $2}')"
grep -c "^! " main.log; grep -c "Overfull" main.log; grep -ci "undefined" main.log
grep -o "newlabel{\(sec:conclusion\|tab:visdrone\)}{{[^}]*}{[0-9]*}" main.aux   # tables before Conclusion
```

### 8.2 Zip test
```bash
Z=$(mktemp -d); cd $Z && unzip -oq /home/user/AC-MOT/JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev65/Paper2_V65_overleaf.zip
pdflatex -interaction=nonstopmode main.tex >/dev/null; pdflatex -interaction=nonstopmode main.tex >/dev/null
pdftotext main.pdf a.txt; pdftotext /home/user/AC-MOT/JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev65/Paper2_V65.pdf b.txt
cmp a.txt b.txt && echo "zip text identical"
grep -ci "gouda\|ismail\|tarek\|gmail\|mtc.edu\|eui.edu" b.txt   # must be 0 for an anonymous copy only
```

## 9. Helper scripts (save to a scratch folder and run)

### 9.1 `gaps.py` — largest blank vertical gap per column (layout check)
```python
import sys, subprocess, glob, tempfile
import numpy as np
from PIL import Image
pdf = sys.argv[1]
with tempfile.TemporaryDirectory() as d:
    subprocess.run(["pdftoppm", "-r", "30", "-png", pdf, f"{d}/p"], check=True)
    for i, f in enumerate(sorted(glob.glob(f"{d}/p-*.png")), 1):
        a = np.asarray(Image.open(f).convert("L")).astype(float)
        h, w = a.shape; top, bot = int(0.07 * h), int(0.90 * h); res = []
        for x0, x1 in ((int(0.10 * w), int(0.49 * w)), (int(0.51 * w), int(0.90 * w))):
            blank = (a[top:bot, x0:x1] > 245).all(axis=1); run = best = 0
            for b in blank:
                run = run + 1 if b else 0; best = max(best, run)
            res.append(best / (bot - top))
        print(f"p{i}: L {res[0]:.2f} R {res[1]:.2f}")
```
Values above about 0.15 (except the last page) mean a visible gap.

### 9.2 `abswc.py` — abstract word count (limit 250)
```python
import re, sys
s = open(sys.argv[1]).read()
a = re.search(r"\\abstract\{(.*?)\}\n", s, re.S).group(1).replace(r"\scl{}", "SCL").replace(r"\%", "%")
print(len(a.split()))
```

### 9.3 `numdiff.py` — every number that changed between two versions
```python
import re, sys, collections
def nums(P):
    files = [P+'/main.tex'] + [P+'/sections/%s.tex' % n for n in ['01_introduction','02_background','03_method','04_development','05_results','06_discussion','07_conclusion']]
    txt = ''.join(open(f).read() for f in files)
    for t in set(re.findall(r'\\input\{(tables/[^}]+)\}', txt)): txt += open(P+'/'+t+'.tex').read()
    txt = re.sub(r'\\cite\{[^}]*\}|\\ref\{[^}]*\}|\\label\{[^}]*\}|\\eqref\{[^}]*\}', '', txt)
    return collections.Counter(re.findall(r'(?<![\w.])[-+]?\d[\d,]*\.?\d*', txt))
a, b = nums(sys.argv[1]), nums(sys.argv[2])
print('only/more in old:', sorted((a-b).items())); print('only/more in new:', sorted((b-a).items()))
```

### 9.4 Content-identical check (layout-only versions)
```python
import subprocess, collections
def chars(p): return collections.Counter(c for c in subprocess.run(['pdftotext', p, '-'], capture_output=True, text=True).stdout if c.isalpha())
a, b = chars('OLD/main.pdf'), chars('NEW/main.pdf'); print(sum(a.values()), sum(b.values()), dict((a-b)+(b-a)))
```

### 9.5 `round5.py` — find values that may have been rounded down from x.xx5
Scan all floats in `research/final/*.json` whose repr has exactly 3 decimals ending in 5. Then list paper numbers equal to their round-down. Verify each hit against its *real* source before changing it, because many hits are coincidences.

### 9.6 `titlecase.py` — Title Case for `references.bib` titles
Rules:
- Capitalize every word.
- Keep lowercase: articles, coordinating conjunctions and all prepositions (a, an, the, and, or, for, of, in, on, at, to, by, via, with, from, as, into, through, under, …), except as the first word or after a colon or question mark.
- Capitalize each part of a hyphenated compound, except minor words in the middle (State-of-the-Art).
- Keep acronyms and CamelCase as they are (YOLOv8, DETRs, OC-SORT).
- Wrap titles in double braces `{{…}}`.

### 9.7 `fill.py` — total used columns (to aim for a page count)
Render the last page at 40 dpi. For each column, find the lowest row with ink. Total = 2·(pages−1) + left fill + right fill.

### 9.8 `fetch_kitti.py` — fetch single KITTI frames (official archive, CRC-checked)
```python
import sys, zipfile, hashlib
sys.path.insert(0, "/home/user/AC-MOT/tools/v7/kitti")
from remotezip import RangeFile
URL = "https://s3.eu-central-1.amazonaws.com/avg-kitti/data_tracking_image_2.zip"
out, seq = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(RangeFile(URL))
for fr in sys.argv[3:]:
    name = f"training/image_02/{seq}/{int(fr):06d}.png"; data = z.read(name)
    open(f"{out}/{seq}_{int(fr):06d}.png", "wb").write(data); print(name, len(data), hashlib.sha256(data).hexdigest()[:16])
```

## 10. Lessons learned (avoid repeating these)

- **Read handwritten marks literally, then check them against facts.** The supervisor's affiliation marks swapped the numbers. The literal result put the owner at EUI, which is wrong. The correct result keeps the supervisor's numbering *and* puts each person at their real institution.
- **Keep the owner's preferred look.** Thick white-outlined boxes in Fig. 4 were rejected; thin boxes are preferred. Ask before changing the example sequence.
- **`\FloatBarrier` placement:**
  - Before Section 4 or after Results it created big gaps.
  - Before the Conclusion it works.
- **`sed` with `\a` inside an insert command eats the backslash.** Use Python for LaTeX edits.
- **Many result tables use stacked cells (`\ci`, `\cib`).**
  - Host and Host+SCL tables use a two-line header and `tabcolsep` 2.5pt to fit the column.
  - Adding columns often causes overfull boxes, so check them.
- **Fig. 2 must be regenerated from the frozen layer.** The script asserts the values against the original per-frame logs; it needs `/root/acmot_work/acmot_external/runs/bytetrack_mot17/...`.
- **The disk fills up easily.** Delete only scratch folders, using literal paths.
