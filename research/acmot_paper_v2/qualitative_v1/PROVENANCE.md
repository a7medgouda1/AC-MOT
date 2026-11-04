# Qualitative tracking figures (Thesis V13) — provenance

All figures are drawn from real video frames and from the track files written by the frozen pipeline.
No box, ID, path or number in a figure is entered by hand.

## Data
| Item | Source | Identity |
|---|---|---|
| Video | VisDrone2019-MOT validation, sequence `uav0000117_02622_v` (349 frames, 2720×1530) | Hugging Face dataset mirror `huseyincavus/visdrone2019-mot`, revision `46a3dc80661a98deb796d886fef52042190ffbf1`, files `VisDrone2019-MOT-val/VisDrone2019-MOT-val/{sequences/uav0000117_02622_v/*, annotations/*}` |
| Annotations | `annotations/uav0000117_02622_v.txt` | sha256 `31658130cfc9a03b…` |
| Detector | YOLO11m, `dronefreak/visdrone-yolo11m` `best.pt`, revision `ed725b7` | sha256 `c6f98247e7c731a567aaf37ca7b808beff588b687623e028b25a2e1d846e96e7` (asserted by `make_cpu_cache.py`) |
| Controller | frozen AC-MOT v3, `research/acmot_paper_v2/controller_search/FREEZE_MANIFEST_V3_ADAPTIVE.json` | action map and thresholds asserted equal to `run_v3_second_val_read.ACTION_MAP` / `SPEC` by `run_tracks.py` |
| Trackers | `adapters.trackers.bytetrack.ByteTrackAdapter`, `adapters.trackers.oatrack.OATrackAdapter` | repository code, unchanged |
| Scoring | `tools/v6/eval_official` (official VisDrone Task 4b filtering, motmetrics, TrackEval HOTA) | repository code, unchanged |

Data, weights and detector caches are kept outside the repository (`/home/user/acmot_viz_data/`).
The sequence is one of the seven VisDrone evaluation sequences of the frozen AC-MOT evaluation (protected-evaluation class P6, development data); no protected split was opened.

### Frames shown in the thesis
| Thesis figure | Frames | sha256 (first 16 hex) |
|---|---|---|
| Fig. 1.3 (top row) | 278 | `0000278.jpg` 39729578c929b397 |
| Fig. 2.2 | 47, 48 | 5a69ca47601ede93, 0326201b2d902641 |
| Fig. 3.5 | 268, 273, 278 | c66a9c8f091b67f6, 4efcc204725950f3, 39729578c929b397 |
| Fig. 3.7 | 72, 349 (last frame of each object) | 1a444be3b1389e14, 8888d955af578d29 |
| Fig. 3.6 | all 349 frames (counts only) | — |
| Fig. 1.3 (bottom row) | KITTI 0001, frame 102: the last row of Fig. 4.4 (`figures/scl_kitti_example_v3.pdf`), reused pixel for pixel | — |

## Software
CPU (4 threads), PyTorch 2.15.0+cpu, Ultralytics 8.3.200, motmetrics 1.4.0, NumPy 2.2.6, OpenCV 4.11.0, Matplotlib 3.11.2.

## Commands (run in this folder)
```
D=/home/user/acmot_viz_data; DATA=$D/visdrone/hf_mirror/VisDrone2019-MOT-val/VisDrone2019-MOT-val
P=/home/user/acmot_viz_venv/bin/python; export PYTHONPATH=$D/TrackEval
$P make_cpu_cache.py --seq uav0000117_02622_v --data $DATA --out $D/cache/yolo11m_vd/visdrone_val --ckpt $D/weights/best_ed725b7.pt
$P run_tracks.py --seq uav0000117_02622_v --data $DATA --cache $D/cache/yolo11m_vd --out tracks --trackeval $D/TrackEval
$P scene_trace.py --seq uav0000117_02622_v --data $DATA --cache $D/cache/yolo11m_vd --tracks tracks --trackeval $D/TrackEval
$P continuity_metrics.py --seq uav0000117_02622_v --data $DATA --tracks tracks
$P make_fig_acmot_example.py --seq uav0000117_02622_v --data $DATA --tracks tracks --out figs/acmot_qual_false.pdf --mode false
$P make_fig_identity.py      --seq uav0000117_02622_v --data $DATA --tracks tracks --out figs/acmot_qual_identity.pdf
$P make_fig_timeline.py      --seq uav0000117_02622_v --data $DATA --tracks tracks --out figs/acmot_qual_timeline.pdf
$P make_fig_mot_elements.py  --seq uav0000117_02622_v --data $DATA --tracks tracks --out figs/mot_elements.pdf
$P make_fig_overview.py --acmot figs/acmot_qual_false.pdf --scl ../../../THESIS_V13/figures/scl_kitti_example_v3.pdf --out figs/overview_examples.pdf
```
Copies in the thesis: `acmot_qual_false.pdf` → `THESIS_V13/figures/acmot_qual_frames.pdf`; `acmot_qual_identity.pdf`, `acmot_qual_timeline.pdf` (same names); `mot_elements.pdf` → `bg_mot_elements.pdf`; `overview_examples.pdf` → `intro_examples.pdf`.
Each figure script also writes a `.json` with the selected frames, crop window and per-panel counts.
`acmot_qual_switch.*` (switch-window variant) and `make_video.py` are not used in the thesis.

## Selection rules (fixed in the scripts before the images were viewed)
- Sequence: median ByteTrack HOTA gain of the seven evaluation sequences in the archived frozen results.
- Fig. 3.5: the frame with the largest reduction in false tracks (baseline minus AC-MOT), and the frames 5 and 10 earlier; crop = the 1280×720 window holding the most false tracks of both runs in that frame.
- Fig. 3.7: objects present in ≥ 40 frames that AC-MOT follows in at least as many frames as the baseline, ranked by the ratio of identity counts (AC-MOT / baseline), first three.
- Fig. 2.2 (baseline run only): the identity switch of the largest object among switches where the old track ends and the new one starts within 5 frames, after the first 40 frames.

## Differences from the archived run
The archived GPU detector cache is not in the repository, so the detector was run again on the CPU in FP32 (archived: T4 GPU, FP16), with the same checkpoint, resolutions, NMS values, confidence floor, `max_det` and class filter. The tracking, controller and scoring code is the repository code, imported unchanged; only the data paths of `controller_search/sim.py` are redirected at run time.

## Display (Thesis V15)
The figure scripts use `thesis_style.py`: Times New Roman text (the font of the thesis) and STIX mathematics, and an optional display gamma for night frames (`--gamma`). The gamma is applied to every pixel of every panel of a figure in the same way, so both pipelines are always shown on identical frames: 1.3 for `acmot_qual_false` (Figs. 1.3 and 3.5), 1.6 for `acmot_qual_identity` (Fig. 3.7) and `mot_elements` (Fig. 2.2), none for the timeline. Frames, objects, tracks and counts are those of V13/V14.
```
$P make_fig_acmot_example.py --seq uav0000117_02622_v --data $DATA --tracks tracks --out figs/acmot_qual_false.pdf --mode false --gamma 1.3
$P make_fig_identity.py      --seq uav0000117_02622_v --data $DATA --tracks tracks --out figs/acmot_qual_identity.pdf --gamma 1.6
$P make_fig_mot_elements.py  --seq uav0000117_02622_v --data $DATA --tracks tracks --out figs/mot_elements.pdf --gamma 1.6
$P make_fig_timeline.py      --seq uav0000117_02622_v --data $DATA --tracks tracks --out figs/acmot_qual_timeline.pdf
$P make_fig_overview.py --acmot figs/acmot_qual_false.pdf --scl ../../../THESIS_V15/figures/scl_kitti_example_v3.pdf --out figs/overview_examples.pdf
```
