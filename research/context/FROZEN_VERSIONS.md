# FROZEN VERSIONS

Historical meaning is never overwritten. Tag → commit mappings are verified
by tools/context_health_check.py (`git rev-list -n1 <tag>`).

| Name | Tag | Commit | Architecture | Purpose | What was frozen | Evaluation status | Superseded? |
|---|---|---|---|---|---|---|---|
| Legacy AC-MOT | v1.0.0-acmot-frozen | a6c1fa49fce1d402513c2df05b7d04b962a6e89e | handcrafted SCI + resolution/sensitivity controller, YOLOv8n + ByteTrack | original thesis method | SCI, controller, three-worker final test workflow | legacy 17-seq test-dev runs (exploratory); legacy UAVDT run on branch freeze/final-after-uavdt-2026-09-12 | yes (research line) |
| Version: V1 | universal-acmot-v1-freeze | e56c2f37793450aa3189a3734298f295194ffa77 | adapters + histogram normaliser + ratio gate ρ 0.6 + legacy SCI | first universal freeze | `configs/universal_acmot_policy.json` at that commit | val only; later run on test-dev as a baseline inside E31 | yes → V3 (Amendment 3) |
| Version: V3 | universal-acmot-v3-freeze | c1e799d3ba74d4c220b6be88f1659cdde1b20bf9 | ECDF + z-logit gate τ 0.75 + legacy SCI | calibration-invariant | policy + pipeline hashes in research/TESTDEV_LOCK.json (lock SUPERSEDED before any test-dev metric) | val; baseline row in E31 | yes → V4 (Amendment 4) |
| Version: V4 | universal-acmot-v4-freeze | fc003bf96621214dc09a0e55f720128093972927 | compute-budget only, ECDF + z-gate, global τ .75 / s .4 / assoc .10 / NMS .45 / tracker 45,.86 | latest frozen Universal system | hashes in research/TESTDEV_LOCK_V4.json | held-out test-dev once (E31); transfer locks FRCNN/UAVDT not yet evaluated | no — BASELINE/ABLATION ONLY, never the final system (Amendment 7, C0); contains category-E constants under Amendment 6 |
| Version: V5-TF | (never created) universal-acmot-v5tf-freeze | — | training-free Otsu bands (F1–F5, E41) | development history | E41 policy lock research/V5TF_POLICY_LOCK.json (PRE_FREEZE, rejected by audit, FX-18) | development-40 only | yes → V6-TF (Amendment 9) |
| Version: V6-TF | universal-acmot-v6-freeze | 2cff95f8a565fdff17f5b1fb06c23cf78e0ffed0 | dedup IoU 0.5 + nested exact-Otsu bands on logits of frames t−10..t−1 + ECDF within band + motion-conditioned association | FINAL TARGET / contribution | configs/universal_acmot_policy_v6tf.json; hashes in research/V6TF_POLICY_LOCK.json; record research/final/FREEZE_RECORD_V6TF.md | development (val-7, dev-40); post-freeze evaluations listed in research/final/FINAL_RESULTS.md | yes → V7 (Amendment 10) |
| Version: V7 | universal-acmot-v7-freeze | 488df9a95472b839cb75b72fb243c7ab3f826df7 | V7f: self-limiting layer between frozen detector and frozen tracker; nested exact Otsu on logits of frames t-10..t-1, whole-stream clean/noisy mode (median rho >= 0.5), host contract (a, b, l, m0), crowd-safe duplicates, rank score remap in noisy frames, continuation rescue, motion tolerance | frozen policy behind Paper 2 (SCL) | configs/universal_acmot_policy_v7.json; hashes in research/V7_POLICY_LOCK.json; code acmot_v7.py | development MOT17/KITTI/score shifts + predeclared PD-SORT and Hybrid-SORT (research/final/V7_MAIN_RESULTS.md) | no — FINAL (Amendment 10, owner decision 2026-10-20) |

Never-to-be-created tag: `universal-acmot-v5-scene-generalized-freeze`
(the learned V5 final fit it would have tagged is forbidden by Amendment 6).

Reproducibility notes: policy/pipeline file hashes for V3/V4 are in the lock
JSONs; detector weights: yolov8n.pt sha256 f59b3d83…, rtdetr-l.pt sha256
6de60b10… (full values in TESTDEV_LOCK_V4.json). Evaluator: TrackEval
12c8791, motmetrics 1.4.0. Cache replay fidelity: E05, E30.

## Other tags (assets, experiment archives, manuscripts)
| Tag | Commit | Meaning |
|---|---|---|
| recent-assets-1 | 70e5f7dc4904444d1091bca2d4d783aee87dacdc | strict SparseTrack Colab bootstrap (assets) |
| v7-dev-assets-1 | d56bba0d83de535541bb8ee0b7d52c4578fe2fb4 | V7 development snapshot, not frozen (ledger E0-E10) |
| jais-overleaf-1 | 8c50fc542fde83fe168bff6364ce5ffcf8586844 | author block and affiliations from the ICMISI 2026 paper; cover letters |
| general-acmot-g1-freeze | 751c602212aed8c0c2c302594dcd42436e2296f0 | General AC-MOT G1 development candidate (research/GENERAL_ACMOT_G1_LOCK.json) |
| g2-s3-1 | 6c88f5d699e7a5d86cec43ff43064b5d7d6b71e0 | G2 S3 workflow release (35 cache jobs, latency) |
| sci-v7f-sweep-1 | e9c3bc0e021af387e08d0abfb9a4be38d879b7eb | SCI+V7f sweep workflow release |
| sci-v7f-unseen-1 | 3da0d1782c756f70159e1b2688cae7e3df80cc2e | G1 transfer workflow release |
| acmot-v3-exp-2026-10-04-freeze | 280b4a2d2c2a53311d18b27886bce714b046f3b8 | frozen AC-MOT V3 paper-ready experiment archive (VisDrone, runtime, statistics, UAVDT) behind Paper 1 |
| jrtip-submission-v1 | c9aa32d334b0a2ec27068d761b37b244776005e4 | AC-MOT JRTIP manuscript v1 (Paper 1 lineage) |
| jrtip-submission-v2 | 2b466f3f8990b4d50c332b53cb18dc29e0449283 | AC-MOT JRTIP manuscript v2 (Paper 1 lineage) |
| v3f-paper-first-journal | 25a55113fcb137690c34f2df5c097229ed74b393 | AC-MOT JRTIP supervisor challenge copy (Paper 1 lineage) |

Manuscript versions and submission state: PAPERS.md.
