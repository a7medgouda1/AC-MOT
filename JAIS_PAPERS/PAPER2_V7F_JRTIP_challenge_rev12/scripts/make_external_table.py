"""
Table tab:external of Paper2_V12. Systems declared at the freeze come from
scripts/evidence.py (V7_EXTERNAL_TRANSFER.md); systems declared after the freeze are
read from research/final/V7_RECENT_EXTERNAL_RESULTS.json. Systems with a FAILED
reproduction are excluded, as the registered protocol requires.

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev12/scripts/make_external_table.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence as E  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "tables" / "tab5_external.tex"
BS = "\\"


def ci(d, lo, hi, nd=2):
    """Value above its interval (macros \\ci / \\cib of main.tex); bold when the interval excludes 0."""
    f = "{:+.%df}" % nd
    mac = BS + ("cib" if (lo > 0 or hi < 0) else "ci")
    return mac + "{" + f.format(d) + "}{" + f.format(lo) + "}{" + f.format(hi) + "}"


def nd_for(d):
    """Three decimals only for narrow intervals, where two would hide the result."""
    vals = (d["diff"], d["ci_lo"], d["ci_hi"])
    tiny = any(0 < abs(v) < 0.005 for v in vals)  # would print as 0.00
    return 3 if (d["ci_hi"] - d["ci_lo"]) < 0.2 or tiny else 2


def twol(a, b):
    return BS + "twol{" + a + "}{" + b + "}"


rows = []
pd = E.EXT_PRE[0]
rows.append((twol("PD-SORT " + BS + "cite{wang2025pdsort}", "(EXACT)"), "MOT17", twol("68.01", f"{pd[2][0]:.2f}"),
             ci(*pd[3]), ci(*pd[4]), ci(*pd[5]), "7/0/0"))
hs = E.EXT_PRE[1]
rows.append((twol("Hybrid-SORT " + BS + "cite{yang2024hybridsort}", "(CLOSE)"), "MOT17", twol("67.1", f"{hs[2][0]:.2f}"),
             twol("0", "(identical)"), "0", "0", "0/7/0"))
rows.append(None)
REF = {("ctwix", "MOT17", "pedestrian"): "77.8", ("ctwix", "KITTIMOT", "car"): "89.3",
       ("ctwix", "KITTIMOT", "pedestrian"): "71.4", ("ctwix", "DanceTrack", "pedestrian"): "60.4",
       ("tracktrack", "DanceTrack_post", "pedestrian"): "63.3"}
CLS = {("ctwix", "MOT17", "pedestrian"): "CLOSE", ("ctwix", "KITTIMOT", "car"): "EXACT",
       ("ctwix", "KITTIMOT", "pedestrian"): "CLOSE", ("ctwix", "DanceTrack", "pedestrian"): "CLOSE",
       ("tracktrack", "DanceTrack_post", "pedestrian"): "CLOSE"}
DATA = {("MOT17", "pedestrian"): "MOT17", ("KITTIMOT", "car"): "KITTI cars",
        ("KITTIMOT", "pedestrian"): "KITTI ped.", ("DanceTrack", "pedestrian"): "DanceTrack",
        ("DanceTrack_post", "pedestrian"): "DanceTrack"}
CITE = {"ctwix": "C-TWiX " + BS + "cite{miah2025twix}", "tracktrack": "TrackTrack " + BS + "cite{shim2025tracktrack}"}
for key in ("ctwix", "tracktrack"):
    s = E.RECENT["systems"][key]
    for ds, r in s["runs"].items():
        if key == "tracktrack" and ds != "DanceTrack_post":
            continue  # reported on its post-processed output, as in its paper
        for c, v in r["classes"].items():
            k = (key, ds, c)
            dl = v["delta"]
            h, m, i = dl["HOTA"], dl["MOTA"], dl["IDF1"]
            w, t, l_ = v["seq_wins_ties_losses"]
            rows.append((twol(CITE[key], f"({CLS[k]})"), DATA[(ds, c)],
                         twol(REF[k], f"{v['baseline']['pooled']['HOTA']:.2f}"),
                         ci(h["diff"], h["ci_lo"], h["ci_hi"], nd_for(h)),
                         ci(m["diff"], m["ci_lo"], m["ci_hi"], nd_for(m)),
                         ci(i["diff"], i["ci_lo"], i["ci_hi"], nd_for(i)), f"{w}/{t}/{l_}"))

head = r"""\begin{table*}[t]
\caption{Baseline comparison on the external systems, each run once with the frozen \scl{}.
Top: declared at the freeze (MOT17 val-half, authors' released detections). Bottom:
declared after the freeze under the registered protocol (authors' released detections;
TrackTrack after its post-processing, as in its paper). Ref.: HOTA reported by the
authors (for PD-SORT, their released output). Class: reproduction against Ref. (EXACT:
$|\Delta\mathrm{HOTA}|\le0.2$; CLOSE: $\le1.0$ with a documented, untuned cause).
Host: HOTA of the published tracker alone (our reproduction). $\Delta$: host with \scl{}
minus host, with the 95\% paired-bootstrap interval below it; bold intervals exclude zero.
W/T/L: sequences where HOTA rose, stayed within 0.01, or fell; ped.: pedestrians. TOPICTrack (FAILED
reproduction) is excluded.}
\label{tab:external}
\centering\footnotesize
\setlength{\tabcolsep}{2.5pt}
\renewcommand{\arraystretch}{1.15}
\begin{tabular}{@{}llccccc@{}}
\toprule
System (class) & Data & \twol{Ref.}{Host} & $\Delta$HOTA & $\Delta$MOTA & $\Delta$IDF1 & W/T/L\\
\midrule"""
lines = [head]
for r in rows:
    lines.append(BS + "midrule" if r is None else " & ".join(r) + BS + BS)
lines.append(r"""\bottomrule
\end{tabular}
\end{table*}""")
OUT.write_text("\n".join(lines) + "\n")
print(f"wrote {OUT}")
