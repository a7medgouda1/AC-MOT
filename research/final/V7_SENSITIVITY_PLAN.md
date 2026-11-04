# Parameter sensitivity of the frozen V7f — plan (written before the runs)

Date: 2026-10-23. Owner instruction (supervisor comment: "add controlled component ablation and parameter
sensitivity analysis"). Development data only (KITTI tracking training, non-protected). The frozen V7f code
(`acmot_v7.py`) and configuration (`configs/universal_acmot_policy_v7.json`) are not changed: every variant is a
runner override `V7f@key=value` of `tools/v7/dev.py`, exactly as in E58. The frozen values stay the reported
values whatever the outcome; this is an analysis, not a retuning.

## Cells (the E57/E58 cells, fixed before the runs)
- C1 ByteTrack, RT-DETR-L; C3 OC-SORT, YOLOv8n;
- C4 ByteTrack, RT-DETR-L with halved scores (`t:scale05`); C5 OC-SORT, YOLOv8n with halved scores.
Cached detections `outputs/det_cache_kitti_native`; official KITTI HOTA (car/pedestrian average,
`tools/v7/kitti/kitti_eval.py`); paired bootstrap over sequences (10,000, seed 42) against V7f.

## Variants (one value changed at a time, all other values frozen)
| Parameter | Frozen | Tested | Override |
|---|---|---|---|
| Window W (frames of logits) | 10 | 5, 20 | `window=5`, `window=20` |
| Frames whose median rho decides the mode | whole stream | last 100, last 300 | `rho_frames=100`, `rho_frames=300` |
| IoU of the duplicate and rescue rules | 0.5 | 0.4, 0.6 | `dup_iou=0.4`, `dup_iou=0.6` |
| Motion history | 100 frames | 50, 200 | `hist=50`, `hist=200` |

The mode threshold 0.5 and the noisy score ranges are fixed in the frozen code and are not varied (changing them
would need a code change of the frozen layer).

## Prediction (written before the runs)
HOTA stays within 1 point of V7f for W, IoU and motion history in every cell. A short median window (100 frames)
lets the mode change inside a sequence; it is expected to be within 1 point on these KITTI cells, whose sequences
have one score scale each.

## Reporting
HOTA (and MOTA, IDF1) of every variant and cell, next to V7f, reported as they come out.
