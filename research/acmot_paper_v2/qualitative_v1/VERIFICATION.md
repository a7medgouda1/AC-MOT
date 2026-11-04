# Qualitative tracking figures (Thesis V13) — verification

## 1. Data
- The mirror holds 349 frames for `uav0000117_02622_v`; the seven evaluation sequences hold 2,846 frames in total, as in the archived evaluation.
- Per-class ground-truth counts of the seven sequences after the official filtering equal the archived counts; the archived aggregate HOTA (ByteTrack baseline, 41.586) is reproduced from the archived per-sequence statistics with `combine_official`.

## 2. Detector re-run
`uav0000117_02622_v.cpu_cache_log.json`: checkpoint sha256 asserted; at every resolution (1088, 1280, 1536) the one-pass path gives boxes identical to the original two-call path on frames 1 and 2 (`verify`: 6 of 6 true).

## 3. Fidelity to the frozen evaluation (ByteTrack, this sequence)
| Metric | Archived baseline | Re-run baseline | Archived AC-MOT | Re-run AC-MOT |
|---|---|---|---|---|
| HOTA | 34.429 | 34.214 | 37.474 | 37.424 |
| HOTA gain | | | +3.045 | +3.210 |
| MOTA | −12.64 | −12.71 | 13.56 | 13.25 |
| IDS | 439 | 439 | 403 | 400 |
| FP | 9,986 | 9,958 | 6,436 | 6,479 |

OATrack re-run: HOTA 39.361 → 41.975, MOTA 18.78 → 24.44, IDS 158 → 139 (`tracks/uav0000117_02622_v_summary.json`).
AC-MOT states of the re-run: LOW in frames 1–30, HIGH in frames 31–349 (one change, 0.287 per 100 frames, equal to the archived switch rate of this sequence). `scene_trace.py` asserts that its per-frame states equal the levels file of `run_tracks.py`.

## 4. Numbers quoted in the thesis (Section 3.6.5, Figs. 1.3, 2.2, 3.5–3.7; Thesis V13 and V14)
| Statement | Source |
|---|---|
| HOTA 34.21 → 37.42, IDF1 37.50 → 42.01, MOTA −12.71 → 13.25, IDS 439 → 400, FP 9,958 → 6,479 | `tracks/uav0000117_02622_v_summary.json` |
| LOW, MEDIUM, HIGH 7.4 %, 30.1 %, 62.5 % over the seven sequences (Thesis V14) | archived frozen results (`SECOND_VAL_READ_V3_RESULT.json`, `level_frac`), as in Section 3.6.2 |
| 18 to 68 annotated objects per frame | `figs/acmot_qual_timeline.json` |
| frames 268/273/278: false 47/53/54 vs 22/28/23; tracked 27/26/24 vs 27/26/25 | `figs/acmot_qual_false.json` |
| 1,255 vs 1,732 output tracks | unique IDs of the two ByteTrack track files |
| SCI 0.72–1.00 after frame 31; HIGH from frame 31 | `tracks/…_scene_trace.json`, `figs/acmot_qual_timeline.json` |
| frames 1–30 equal false tracks; from frame 31 fewer in 306 of 319 frames, 18.0 vs 28.9 per frame | per-frame counts of `make_fig_timeline.py` |
| pedestrian 5 → 2 identities (68 / 70 of 71 frames); van 6 → 3 (46 / 75 of 153); truck 2 → 1 (149 / 198 of 228); 31 objects with fewer identities | `figs/acmot_qual_identity.json` |
| Fig. 2.2: pedestrian 118, track 1497 (frame 47) → 1693 (frame 48) | `figs/mot_elements.json` |
| Fig. 4.5: all values | Table 4.9 of the thesis (unchanged) |

## 5. Thesis build (THESIS_V13)
- LaTeX: 0 errors, 0 undefined references, 0 overfull boxes; bibliography order identical to V12 (no reference renumbered).
- Word: 109 pages; contents and lists 139 of 139 entries on their printed pages; 53 of 53 figures, tables and algorithms after their first mention; 38 of 38 tables cell-for-cell identical to V12.
- Sources: compared word by word with V12, every change is an insertion, except one sentence of Section 3.7 that is extended with a reference to Section 3.6.5.
