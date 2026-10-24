"""
Adds the column "Host+SCL" (the same tracker with SCL) next to "Host" (the tracker alone) in the
result tables of Paper2_V62 (MOT17, KITTI, external trackers, UAVDT), so that both runs are shown
and not only their difference. The values are read from the recorded result files; the BoT-SORT
KITTI values (sequence 0020 left out, as in the paper) come from tools/v7/kitti/kitti_eval.py with
V7_EXCLUDE=0020 on the recorded outputs (re-evaluated 2026-10-24, host values equal to the paper).

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev62/scripts/make_ab_tables.py
"""
import json
import re
from pathlib import Path

V = Path(__file__).resolve().parents[1]
F = V.parents[1] / "research/final"
dev = json.load(open(F / "V7_DEV_RESULTS.json"))
main = json.load(open(F / "V7_MAIN_RESULTS.json"))["sparsetrack"]
ext = json.load(open(F / "V7_EXTERNAL_RESULTS.json"))["results"]
uav = json.load(open(F / "V7_UAVDT_RESULT.json"))["bootstrap"]["per_det"]
M = ("HOTA", "MOTA", "IDF1", "IDS")


def pick(d, keys=M, idsum=False):
    return {m: d[m + ("_avg" if not idsum and m != "IDS" else "")] if idsum else d[m] for m in keys}


def kitti(d):
    return {"HOTA": d["HOTA_avg"], "MOTA": d["MOTA_avg"], "IDF1": d["IDF1_avg"], "IDS": d["IDS_sum"]}


by = dev["mot17_bytetrack_ocsort_c1"]
bt = dev["mot17_boosttrack"]
pd = next(v for k, v in ext.items() if k.startswith("PD-SORT"))
hy = next(v for k, v in ext.items() if k.startswith("Hybrid-SORT"))
# block title (as written in the table) -> (host values, Host+SCL values)
PAIRS = {
    "tab3_mot17": {
        "SparseTrack": (main["reproduction"], main["V7f"]),
        "BoostTrack, online": (bt["BT7_BASELINE"], bt["BT7_BASELINE"]),
        "BoostTrack, + GBI": (bt["BT7_BASELINE_post_gbi"], bt["BT7_BASELINE_post_gbi"]),
        "ByteTrack, floor 0.01": (by["BY_official_st_BASELINE"], by["BY_official_st_V7f"]),
        "ByteTrack, floor 0.1": (by["BY_official_bt_BASELINE"], by["BY_official_bt_V7f"]),
        "OC-SORT, floor 0.01": (by["OC_st_BASELINE"], by["OC_st_V7f"]),
        "OC-SORT, floor 0.1": (by["OC_bt_BASELINE"], by["OC_bt_V7f"]),
    },
    "tab4_kitti": {
        "ByteTrack": (kitti(dev["kitti_train_rtdetr"]["NATIVE"]), kitti(dev["kitti_train_rtdetr"]["V7f"])),
        "BoT-SORT": ({"HOTA": 53.912, "MOTA": 48.254, "IDF1": 67.743, "IDS": 476},
                     {"HOTA": 54.517, "MOTA": 56.111, "IDF1": 70.847, "IDS": 250}),
        "OC-SORT": (kitti(dev["kitti_train_yolov8"]["NATIVE@trk:ocsort"]),
                    kitti(dev["kitti_train_yolov8"]["V7f@trk:ocsort"])),
    },
    "tab5_external": {
        "PD-SORT": (pd["reproduction"], pd["with_v7f"]),
        "Hybrid-SORT": (hy["reproduction"], hy["reproduction"]),
    },
    "tab_visdrone": {
        "ByteTrack, RT-DETR-L": ({m: uav["rtdetr"][m]["A"] for m in M}, {m: uav["rtdetr"][m]["B"] for m in M}),
        "ByteTrack, YOLOv8n": ({m: uav["yolov8"][m]["A"] for m in M}, {m: uav["yolov8"][m]["B"] for m in M}),
    },
}
ARROW = {"HOTA": r"HOTA$\uparrow$", "MOTA": r"MOTA$\uparrow$", "IDF1": r"IDF1$\uparrow$", "IDS": r"IDS$\downarrow$"}


def fmt(m, x):
    # half-up rounding of the recorded value (e.g. 44.175 -> 44.18), as everywhere in the paper
    from decimal import Decimal, ROUND_HALF_UP
    if m == "IDS":
        return "%d" % round(x)
    return str(Decimal(repr(round(x, 3))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


for name, blocks in PAIRS.items():
    p = V / "tables" / f"{name}.tex"
    lines = p.read_text().split("\n")
    out, cur = [], None
    for l in lines:
        mb = re.match(r"\\multicolumn\{(\d)\}\{@\{\}l\}\{\\textit\{([^}]*)\}", l)
        if mb:
            cur = next(b for b in blocks if mb.group(2).startswith(b))
            n = int(mb.group(1))
            l = l.replace(r"\multicolumn{%d}" % n, r"\multicolumn{%d}" % (n + 1), 1)
        mr = re.match(r"\\quad (HOTA|MOTA|IDF1|IDS) & (.*)$", l)
        if mr and cur:
            m, rest = mr.group(1), mr.group(2).split(" & ")
            host, scl = blocks[cur]
            hcell = rest[-2]
            assert hcell.strip() == fmt(m, host[m]), (name, cur, m, hcell, fmt(m, host[m]))
            rest.insert(len(rest) - 1, fmt(m, scl[m]))
            l = r"\quad %s & " % ARROW[m] + " & ".join(rest)
        out.append(l)
    s = "\n".join(out)
    # header and column layout: one more right-aligned column after Host
    s = s.replace("Metric & Paper & Host & $\\Delta$ [95\\% CI]\\\\",
                  "Metric & Paper & Host & Host+\\scl{} & Change [95\\% CI]\\\\")
    s = s.replace("Metric & Host & $\\Delta$ [95\\% CI]\\\\",
                  "Metric & Host & Host+\\scl{} & Change [95\\% CI]\\\\")
    s = s.replace("\\begin{tabular}{@{}lrrl@{}}", "\\begin{tabular}{@{}lrrrl@{}}")
    s = s.replace("\\begin{tabular}{@{}lrl@{}}", "\\begin{tabular}{@{}lrrl@{}}")
    p.write_text(s)
    print("updated", name)
