"""
Table "AOB vs SCL" of Paper2_V65 as a full-width table: for each strong published tracker on MOT17
val-half, the value of the tracker alone (Host), with the earlier design AOB (Host+AOB) and with the
final SCL (Host+SCL), each followed by its change and 95% paired-bootstrap interval on one line.
Absolute values come from research/final/V7_DEV_RESULTS.json (AOB = *_plus_V6TF runs) and
V7_MAIN_RESULTS.json (SparseTrack with SCL); changes and intervals are the recorded bootstrap
results already used in the paper (research/final/FINAL_RESULTS.md, STATISTICAL_ANALYSIS.md).

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev65/scripts/make_tab_prior.py
"""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

V = Path(__file__).resolve().parents[1]
F = V.parents[1] / "research/final"
dev = json.load(open(F / "V7_DEV_RESULTS.json"))
main = json.load(open(F / "V7_MAIN_RESULTS.json"))["sparsetrack"]
st, bt = dev["mot17_sparsetrack"], dev["mot17_boosttrack"]
M = ("HOTA", "MOTA", "IDF1")
ARROW = {"HOTA": r"HOTA$\uparrow$", "MOTA": r"MOTA$\uparrow$", "IDF1": r"IDF1$\uparrow$", "IDS": r"IDS$\downarrow$"}


def r2(x):
    return str(Decimal(repr(round(x, 3))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def val(m, x):
    return "%d" % round(x) if m == "IDS" else r2(x)


# recorded changes with 95% interval: (change, low, high, bold)
AOB = {
    "SparseTrack": {"HOTA": ("-4.15", "-5.54", "-1.66", 1), "MOTA": ("-6.14", "-8.10", "-2.74", 1),
                    "IDF1": ("-4.49", "-6.19", "-1.96", 1), "IDS": ("-16", "-47", "+12", 0)},
    "BoostTrack, online": {"HOTA": ("-5.89", "-7.76", "-2.87", 1), "MOTA": ("-8.87", "-12.37", "-7.14", 1),
                           "IDF1": ("-6.22", "-9.33", "-2.85", 1), "IDS": ("-38", "-81", "-1", 1)},
    "BoostTrack, with GBI": {"HOTA": ("-5.37", "-7.30", "-2.75", 1), "MOTA": ("-8.73", "-12.59", "-6.50", 1),
                             "IDF1": ("-5.65", "-8.96", "-2.77", 1), "IDS": ("-27", "-73", "+11", 0)},
}
SCL = {
    "SparseTrack": {"HOTA": ("+0.06", "-0.01", "+0.25", 0), "MOTA": ("+0.08", "-0.03", "+0.30", 0),
                    "IDF1": ("+0.16", "-0.02", "+0.70", 0), "IDS": ("+7", "0", "+19", 0)},
}
RUNS = {  # tracker -> (host, host+AOB, host+SCL), cite key
    "SparseTrack": ((main["reproduction"], st["ST_plus_V6TF"], main["V7f"]), "liu2025sparsetrack"),
    "BoostTrack, online": ((bt["BT7_BASELINE"], bt["BT_plus_V6TF"], bt["BT7_BASELINE"]), "stanojevic2024boosttrack"),
    "BoostTrack, with GBI": ((bt["BT7_BASELINE_post_gbi"], bt["BT_plus_V6TF_post_gbi"], bt["BT7_BASELINE_post_gbi"]),
                             "stanojevic2024boosttrack"),
}


def cell(c):
    d, lo, hi, b = c
    s = "$%s$ [$%s$, $%s$]" % (d, lo, hi)
    return "{\\boldmath %s}" % s if b else s


rows = []
for name, ((h, a, s), key) in RUNS.items():
    rows.append(r"\multicolumn{6}{@{}l}{\textit{%s} \cite{%s}}\\" % (name, key))
    for m in M:
        # the recorded change must match the recorded runs (within rounding of the 3-decimal values)
        da = float(AOB[name][m][0])
        assert abs((a[m] - h[m]) - da) <= (0 if m == "IDS" else 0.006), (name, m, a[m] - h[m], da)
        if name in SCL:
            ds = float(SCL[name][m][0])
            assert abs((s[m] - h[m]) - ds) <= (0 if m == "IDS" else 0.006), (name, m, s[m] - h[m], ds)
            scl = cell(SCL[name][m])
        else:
            assert s[m] == h[m]
            scl = "0 (identical)"
        rows.append(r"\quad %s & %s & %s & %s & %s & %s\\" % (
            ARROW[m], val(m, h[m]), val(m, a[m]), cell(AOB[name][m]), val(m, s[m]), scl))

tex = r"""\begin{table*}[!t]
\caption{MOT17 val-half with the published YOLOX-X detections: the earlier design \aob{} and the final \scl{}, each added to the same strong tracker. Host: the tracker alone; Host+\aob{} and Host+\scl{}: the same tracker with each layer, on the same detections. Change: the run with the layer minus Host, with its 95\% bootstrap interval in brackets; a negative HOTA, MOTA, or IDF1 change means the layer made the tracker worse; bold: the interval does not include zero, so the change is reliable. $\uparrow$: higher is better.}
\label{tab:prior}
\centering\footnotesize
\setlength{\tabcolsep}{6pt}
\begin{tabular}{@{}lrrlrl@{}}
\toprule
Metric & Host & Host+\aob{} & \aob{} change [95\% CI] & Host+\scl{} & \scl{} change [95\% CI]\\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table*}
"""
(V / "tables" / "tab_prior.tex").write_text(tex)
print(tex)
