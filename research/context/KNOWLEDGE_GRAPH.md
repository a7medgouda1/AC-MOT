# KNOWLEDGE GRAPH SOURCE — typed entities and relations for Graphify

Parsed by `tools/build_context_graph.py` (rows of the two tables below only).
Entity names are `Type: Name` and must be reused verbatim. Relations are
UPPER_SNAKE_CASE. Every row must be backed by the file in "Defined in".
Edit this file when the project state changes, then rebuild the graph.

## Entities
| Entity | Status | Summary | Defined in |
|---|---|---|---|
| Project: Universal AC-MOT | CURRENT | adaptive control layer around frozen detector and frozen tracker for drone multi-object tracking | PROJECT_STATE.md |
| Version: Legacy AC-MOT | FROZEN SUPERSEDED | original handcrafted SCI controller YOLOv8n ByteTrack 2026-09-11 | ARCHITECTURE.md |
| Version: V1 | FROZEN SUPERSEDED | histogram normaliser ratio gate legacy SCI not temperature invariant | FROZEN_VERSIONS.md |
| Version: V2 variants | SUPERSEDED | V2b V2c V2d V2e V2f density budgets reliability feedback all failed | FAILED_EXPERIMENTS.md |
| Version: V3 | FROZEN SUPERSEDED | calibration-invariant ECDF z-logit gate with legacy SCI | FROZEN_VERSIONS.md |
| Version: V4 | FROZEN BASELINE ONLY | previous frozen version (before V6-TF); baseline and ablation only, never the final system or a fallback; compute-budget-only, VisDrone-tuned constants | FROZEN_VERSIONS.md |
| Version: V5 learned controller | SUPERSEDED RESEARCH-ONLY | scene-state learned stump tree Optuna controller research upper bound not deployable | DECISIONS.md |
| Version: V5-TF | SUPERSEDED DEVELOPMENT | training-free Otsu-band line F1-F5 and E41; E41 locked then rejected by audit (FX-18); never frozen; succeeded by V6-TF | ARCHITECTURE.md |
| Version: V6-TF | FROZEN SUPERSEDED | previous frozen final target (tag universal-acmot-v6-freeze, 2cff95f): dedup IoU 0.5, nested exact-Otsu bands on logits of frames t-10..t-1, motion-conditioned association; negative external transfer D-029; superseded by V7 (Amendment 10) | ARCHITECTURE.md |
| Architecture: Original SCI architecture | SUPERSEDED | scene analysis SCI weighted sum resolution and sensitivity controller | ARCHITECTURE.md |
| Architecture: V4 compute-budget architecture | ABLATION | V4 is not the final architecture: compute-budget-only ablation, scene adaptation deletion rejected (D-009), VisDrone-tuned category E constants; resolution budget ECDF z-gate | ARCHITECTURE.md |
| Architecture: V5-TF target architecture | CURRENT | frame scene state analyzer online self-calibration AC controller before detector candidate handling tracker feedback | ARCHITECTURE.md |
| Component: Scene State Analyzer | EXPERIMENTAL | causal image motion detector tracker cues frames before t | ARCHITECTURE.md |
| Component: Online Self-Calibration | EXPERIMENTAL | rolling median MAD robust z ECDF Otsu over causal windows no training | ARCHITECTURE.md |
| Component: Universal AC Controller | EXPERIMENTAL | F3 selected by E36 but fixed Otsu bins and memory block freeze under C5 | ARCHITECTURE.md |
| Component: Compute Latency Constraint | CURRENT | resolution budget 640 736 832 largest level meeting target FPS | ARCHITECTURE.md |
| Component: ECDF Normaliser | CURRENT | order-only causal score normalisation exact Platt temperature invariance | ARCHITECTURE.md |
| Component: Otsu-3 Candidate Bands | EXPERIMENTAL | three-class Otsu on candidate logits primary extend-only discard | ARCHITECTURE.md |
| Component: Z-logit Leader Gate | FROZEN | V3 V4 gate demote candidates below EMA leader tau 0.75 | ARCHITECTURE.md |
| Component: Legacy SCI | REJECTED | old SCI handcrafted scene complexity index removed; old SCI cues rejected crowd tiny edges brightness darkness blur weights | DECISIONS.md |
| Component: Detector Adapter | CURRENT | detector-agnostic interface score floor 0.01 native suppression | ARCHITECTURE.md |
| Component: Tracker Adapter | CURRENT | tracker-agnostic interface native defaults set_retention association tolerance | ARCHITECTURE.md |
| Rule: F1 Otsu window bands | CANDIDATE | three-class Otsu on logits of causal window frames before t | ARCHITECTURE.md |
| Rule: F2 Otsu frame bands | CANDIDATE | three-class Otsu within frame t candidates | ARCHITECTURE.md |
| Rule: F3 motion-aware association | SELECTED EXPERIMENTAL | E36-selected current candidate F1 plus association tolerance scaled by motion ratio; category-E Otsu constants block freeze | DECISIONS.md |
| Rule: F5 scene-adaptive resolution R-res | FAILED DEVELOPMENT | F3 plus object-size ECDF resolution; E36 worse than F3 and random F5R at matched compute | FAILED_EXPERIMENTS.md |
| Rule: F5R random resolution control | CONTROL | F3 plus random resolution levels same budget guard not selectable | ARCHITECTURE.md |
| Rule: F4 online z-gate | DROPPED | identical to F1 by construction | DECISIONS.md |
| Cue: det_gap | CANDIDATE | detector leader gap signal beyond null both detectors | DECISIONS.md |
| Cue: det_count | CANDIDATE | detector candidate count density signal | DECISIONS.md |
| Cue: trk_survival | CANDIDATE | tracker survival association state | DECISIONS.md |
| Cue: trk_match | CANDIDATE | tracker match behaviour | DECISIONS.md |
| Cue: img_motion | CANDIDATE | global image motion used by F3 as ratio to rolling median | DECISIONS.md |
| Cue: img_motion_resp | CANDIDATE | motion response phase correlation peak | DECISIONS.md |
| Cue: img_edges | REJECTED | edge density rejected negative everywhere legacy SCI cue | DECISIONS.md |
| Cue: img_brightness | REJECTED | brightness darkness rejected legacy SCI cue | DECISIONS.md |
| Cue: img_blur | REJECTED | blur Laplacian rejected legacy SCI cue | DECISIONS.md |
| Cue: crowd count n/30 | REJECTED | legacy SCI crowd cue sign flips below random | DECISIONS.md |
| Cue: tiny object area | REJECTED | legacy SCI tiny cue no consistent benefit | DECISIONS.md |
| Cue: temporal persistence | REJECTED | high for clutter scene property not failure signal | FAILED_EXPERIMENTS.md |
| Parameter: RobustHistory window 100 | CATEGORY A | E39 insensitive at 50 and 200 both detectors no added catastrophic cell | PARAMETER_STATUS.md |
| Parameter: RobustHistory warm-up 5 | CATEGORY A | E39 insensitive at 3 and 10 | PARAMETER_STATUS.md |
| Parameter: Otsu window 10 frames | CATEGORY E FREEZE BLOCKER | E39 sensitive default retained only for recorded F3 not deployable under C5 | PARAMETER_STATUS.md |
| Parameter: OTSU_BINS 64 | CATEGORY E FREEZE BLOCKER | E39 sensitive default retained only for recorded F3 not deployable under C5 | PARAMETER_STATUS.md |
| Parameter: Z_REF 0.75 | CATEGORY E | equals V4 tau logging only must not enter V5-TF rule | PARAMETER_STATUS.md |
| Parameter: V4 tau 0.75 | CATEGORY E FOR V5-TF | VisDrone-selected gate threshold V4 only | PARAMETER_STATUS.md |
| Parameter: V4 sensitivity 0.4 | CATEGORY E FOR V5-TF | VisDrone-selected V4 only | PARAMETER_STATUS.md |
| Parameter: V4 association offset 0.10 | CATEGORY E FOR V5-TF | VisDrone-selected V4 only | PARAMETER_STATUS.md |
| Parameter: V4 NMS 0.45 | CATEGORY E FOR V5-TF | YOLO-derived V4 only V5-TF uses detector-native suppression | PARAMETER_STATUS.md |
| Parameter: V4 tracker 45/0.86 | CATEGORY E FOR V5-TF | legacy retention match V4 only | PARAMETER_STATUS.md |
| Parameter: F3 cap 0.95 | SAFETY BOUND | generic engineering bound category C | PARAMETER_STATUS.md |
| Parameter: native tracker defaults 30/0.8 | API | category D tracker defaults used by V5-TF | PARAMETER_STATUS.md |
| Parameter: fidelity gate thresholds | PROTOCOL CONSTANT | never relaxed after seeing gate | PARAMETER_STATUS.md |
| Detector: YOLOv8n | DEVELOPMENT | COCO pretrained frozen development detector | ENVIRONMENT_AND_PATHS.md |
| Detector: RT-DETR-L | DEVELOPMENT | COCO pretrained frozen NMS-free development detector | ENVIRONMENT_AND_PATHS.md |
| Detector: Faster R-CNN ResNet50-FPN v2 | PROTECTED | unseen detector transfer test no quality metrics before freeze | PROTECTED_EVALUATIONS.md |
| Tracker: ByteTrack | DEVELOPMENT | development tracker frozen | ENVIRONMENT_AND_PATHS.md |
| Tracker: BoT-SORT | PROTECTED | tracker transfer test for V5-TF | PROTECTED_EVALUATIONS.md |
| Dataset: VisDrone2019-MOT | USED | drone MOT benchmark train val test-dev | DATASETS_AND_SPLITS.md |
| Dataset: UAVDT | PROTECTED | unseen dataset transfer test | DATASETS_AND_SPLITS.md |
| Split: VisDrone2019-MOT-val | DEVELOPMENT NOT CLEAN | V1-V5 development secondary check only for V5-TF | DATASETS_AND_SPLITS.md |
| Split: VisDrone2019-MOT-train development-40 | DEVELOPMENT | V5-TF rule validation validate never fit | DATASETS_AND_SPLITS.md |
| Split: VisDrone2019-MOT-train confirmation-16 | PROTECTED | untouched evaluate once after V5-TF freeze | DATASETS_AND_SPLITS.md |
| Split: VisDrone2019-MOT-test-dev | HELD-OUT USED ONCE | V4 evaluated once post-hoc only for V5-TF | DATASETS_AND_SPLITS.md |
| Split: UAVDT test | PROTECTED | 20 sequences unseen dataset transfer | DATASETS_AND_SPLITS.md |
| Metric: HOTA | EVALUATION | TrackEval 12c8791 | VALIDATION_PROTOCOL.md |
| Metric: IDF1 | EVALUATION | motmetrics 1.4.0 | VALIDATION_PROTOCOL.md |
| Metric: MOTA | EVALUATION | motmetrics catastrophic cell MOTA below 0 | VALIDATION_PROTOCOL.md |
| Metric: IDS | EVALUATION | identity switches motmetrics | VALIDATION_PROTOCOL.md |
| Experiment: E17 signal audit | DONE | leader-relative score separates TP from clutter temporal persistence rejected | EXPERIMENT_REGISTRY.md |
| Experiment: E24-E26 SCI audit | DONE | legacy SCI no better than random allocation at matched compute | EXPERIMENT_REGISTRY.md |
| Experiment: E31 V4 test-dev held-out | DONE HELD-OUT | V4 evaluated once YOLO better RT-DETR below shared static | RESULTS_CANONICAL.md |
| Experiment: E32 S1 headroom | DONE DEVELOPMENT | headroom for tau association resolution sensitivity retention none | EXPERIMENT_REGISTRY.md |
| Experiment: E33 S2 cue utility | DONE DEVELOPMENT | candidate cues det_gap det_count trk_survival trk_match motion | EXPERIMENT_REGISTRY.md |
| Experiment: E34-E35 S3 learned controller | FAILED | learned controllers lose to V4 on val overfitting by scarcity | FAILED_EXPERIMENTS.md |
| Experiment: E36 V5-TF dev validation | DONE DEVELOPMENT | F3 selected; F5 worse than F3 and random F5R; F3 does not improve worst-detector criterion vs V4 | EXPERIMENT_REGISTRY.md |
| Experiment: E37 discovery S1-S3 on train | PLANNED OPTIONAL | research upper bound only never final fit | EXPERIMENT_REGISTRY.md |
| Experiment: E38 T4 fidelity gate | PENDING | Mac MPS vs Colab T4 cache fidelity before freeze | EXPERIMENT_REGISTRY.md |
| Experiment: E39 constant audit | DONE DEVELOPMENT | history window and warm-up insensitive A; Otsu bins and window sensitive E freeze blockers | EXPERIMENT_REGISTRY.md |
| Experiment: E40 F3 live replay parity | PASS DEVELOPMENT | exact tracks and controls on 80 of 80 frames two sequences two detectors no quality metric | EXPERIMENT_REGISTRY.md |
| Experiment: E41 exact-Otsu family | DONE DEVELOPMENT | exact current-frame 3-class Otsu; 80/80 artifacts, 15 catastrophic cells, +0.69 percent worst-detector relative gain vs V4; no fixed bins or Otsu memory | EXPERIMENT_REGISTRY.md |
| Result: V4 test-dev pooled metrics | HELD-OUT | outputs/heldout_v4/pooled_metrics.json | RESULTS_CANONICAL.md |
| Result: V5-TF E36 family choice | DEVELOPMENT | F3 selected 17 catastrophic cells worst-detector relative gain minus 0.339 percent; F5 18 and minus 2.646 percent | RESULTS_CANONICAL.md |
| Result: V5-TF E39 constant audit | DEVELOPMENT | Otsu bins and window sensitive category E; history and warm-up insensitive A | RESULTS_CANONICAL.md |
| Failure: V1 candidate explosion | FAILED | equal percentage not equal count | FAILED_EXPERIMENTS.md |
| Failure: V2 density budgets | FAILED | double budget additive offsets over-suppress | FAILED_EXPERIMENTS.md |
| Failure: V2f closed-loop trust windup | FAILED | reliability conflates hard scene with false candidates | FAILED_EXPERIMENTS.md |
| Failure: J2 max-min objective degenerate | FAILED | unnormalised max-min tracks weakest detector | FAILED_EXPERIMENTS.md |
| Failure: V1 temperature non-invariance | FAILED | histogram normaliser breaks under score recalibration | FAILED_EXPERIMENTS.md |
| Failure: legacy SCI below random | FAILED | handcrafted SCI cues do not generalise | FAILED_EXPERIMENTS.md |
| Failure: MOTA-aligned learning cost | FAILED | objective mismatch with HOTA IDF1 adoption criterion | FAILED_EXPERIMENTS.md |
| Failure: learned controller overfitting by scarcity | FAILED | stumps beat global value in training folds lose held-out | FAILED_EXPERIMENTS.md |
| Failure: unstable gate tau cue | FAILED | four different cues across folds tau not adapted | FAILED_EXPERIMENTS.md |
| Failure: V4 RT-DETR below shared static | FAILED HYPOTHESIS | H2 rejected recall-limited category E constants | FAILED_EXPERIMENTS.md |
| Failure: F5 size-state resolution below random | FAILED HYPOTHESIS | E36 F5 worse than fixed F3 and random F5R despite eligible compute | FAILED_EXPERIMENTS.md |
| Decision: D-005 remove legacy SCI | ACTIVE | legacy SCI removed from V4 decision path | DECISIONS.md |
| Decision: D-009 keep scene adaptation V4 is ablation | ACTIVE | why V4 is not the final architecture: V4 compute-only is an ablation, deleting scene adaptation rejected as final direction, V4 constants are VisDrone-tuned category E | DECISIONS.md |
| Decision: D-010 cue status | ACTIVE | candidate and rejected cues from S2 | DECISIONS.md |
| Decision: D-011 learned V5 not adopted | ACTIVE | move development to train | DECISIONS.md |
| Decision: D-012 40/16 train split | PARTLY SUPERSEDED | final fit clause superseded by D-015 | DECISIONS.md |
| Decision: D-014 fidelity gate constants | ACTIVE | T4 gate thresholds never relaxed | DECISIONS.md |
| Decision: D-015 training-free final AC | ACTIVE | final AC layer must not be trained Optuna discovery-only | DECISIONS.md |
| Decision: D-016 F4 dropped | ACTIVE | F4 identical to F1 | DECISIONS.md |
| Decision: D-018 final target V5-TF | SUPERSEDED | final target is V5-TF; V4 baseline ablation only never fallback; confirmation reported not a gate | DECISIONS.md |
| Decision: D-019 scene-state control R-res | ACTIVE | frozen V5-TF must contain scene-state control; selectable F3 F5 | DECISIONS.md |
| Decision: D-020 constant audit rule | ACTIVE | sensitivity audit insensitive to structural else reported category E never tuned | DECISIONS.md |
| Decision: D-022 E36 selects F3 | ACTIVE | F3 selected honestly; F5 scene-adaptive resolution did not beat random control | DECISIONS.md |
| Decision: D-023 E39 C5 blockers | ACTIVE | Otsu bins and window sensitive E block policy lock and freeze | DECISIONS.md |
| Decision: D-024 live replay parity | ACTIVE | F3 live motion path exactly equals cached replay on declared development subset | DECISIONS.md |
| Decision: D-017 repository is project memory | ACTIVE | context files over chat history | DECISIONS.md |
| Constraint: C0 final target V7 | HARD | FINAL TARGET = V7 frozen V7f (Amendment 10, owner decision 2026-10-20); V6-TF frozen history; V4 historical baseline ablation only; never revert to V4 | HARD_CONSTRAINTS.md |
| Constraint: C1 training-free final AC layer | HARD | AC training NOT allowed no fitted controller no labels no GT at deployment | HARD_CONSTRAINTS.md |
| Constraint: C3 causality | HARD | frame t uses only frames up to t no future no GT | HARD_CONSTRAINTS.md |
| Constraint: C5 no category E constants | HARD | E39 resolved history and warm-up as A; sensitive Otsu window and bins remain freeze blockers | HARD_CONSTRAINTS.md |
| Constraint: C6 AC before detector | HARD | not merely a post-detector score filter V4 is ablation | HARD_CONSTRAINTS.md |
| Constraint: C7 Optuna research-only | HARD | S1 S2 S3 C1 C2 C3 Optuna discovery tools only | HARD_CONSTRAINTS.md |
| Constraint: C8 protected evaluations | HARD | protected datasets and evaluations currently: confirmation-16, UAVDT test, Faster R-CNN, BoT-SORT; test-dev used once; no quality metrics before freeze | HARD_CONSTRAINTS.md |
| Constraint: C9 T4 official timing | HARD | Mac MPS development only fidelity gate constants | HARD_CONSTRAINTS.md |
| Constraint: C11 honest reporting | HARD | report if training-free does not beat V4 never switch to trained controller | HARD_CONSTRAINTS.md |
| Protocol: Amendment 4 | HISTORICAL | V4 whole-controller generalization audit | VALIDATION_PROTOCOL.md |
| Protocol: Amendment 5d | PARTLY SUPERSEDED | 40/16 train split protocol | VALIDATION_PROTOCOL.md |
| Protocol: Amendment 5f | ACTIVE | cross-hardware fidelity gate | VALIDATION_PROTOCOL.md |
| Protocol: Amendment 7 | SUPERSEDED IN PART | V5-TF final target, scene-adaptive resolution R-res, families F3 F5 F5R, constant audit | VALIDATION_PROTOCOL.md |
| Protocol: Amendment 6 | CURRENT | V5-TF training-free protocol families comparison freeze | VALIDATION_PROTOCOL.md |
| Tag: v1.0.0-acmot-frozen | FROZEN | legacy AC-MOT tag | FROZEN_VERSIONS.md |
| Tag: universal-acmot-v1-freeze | FROZEN | V1 tag | FROZEN_VERSIONS.md |
| Tag: universal-acmot-v3-freeze | FROZEN | V3 tag | FROZEN_VERSIONS.md |
| Tag: universal-acmot-v4-freeze | FROZEN | V4 tag latest frozen | FROZEN_VERSIONS.md |
| Tag: universal-acmot-v5tf-freeze | PLANNED | created only after rule design fixed and T4 gate PASS | FROZEN_VERSIONS.md |
| Commit: a6c1fa4 | HISTORY | legacy AC-MOT freeze commit | FROZEN_VERSIONS.md |
| Commit: e56c2f3 | HISTORY | V1 freeze commit | FROZEN_VERSIONS.md |
| Commit: c1e799d | HISTORY | V3 freeze commit | FROZEN_VERSIONS.md |
| Commit: fc003bf | HISTORY | V4 freeze commit | FROZEN_VERSIONS.md |
| Commit: 3684684 | HISTORY | Amendment 6 training-free requirement | DECISIONS.md |
| Commit: 71faf44 | HISTORY | V5-TF implementation F1 F2 F3 | DECISIONS.md |
| Lock: TESTDEV_LOCK_V4 | USED ONCE | V4 test-dev lock evaluated once E31 | ../TESTDEV_LOCK_V4.json |
| Lock: TRANSFER_LOCK_FASTERRCNN | LOCKED NOT EVALUATED | Faster R-CNN transfer lock for V4 | ../TRANSFER_LOCK_FASTERRCNN.json |
| Lock: TRANSFER_LOCK_UAVDT | LOCKED NOT EVALUATED | UAVDT transfer lock for V4 | ../TRANSFER_LOCK_UAVDT.json |
| Lock: TRAIN_SPLIT_V5 | ACTIVE | fixed 40/16 split seed 20260927 | ../TRAIN_SPLIT_V5.json |
| Families: detector and tracker families tested | EVIDENCE | detector families tested YOLOv8n RT-DETR-L; Faster R-CNN cached not yet evaluated; tracker families tested ByteTrack BoT-SORT | RESULTS_CANONICAL.md |
| Failure: Failures not to repeat | REGISTRY | failures that should not be repeated: legacy SCI, learned controllers, density budgets, temporal persistence, MOTA-aligned cost, closed-loop trust, max-min objective | FAILED_EXPERIMENTS.md |
| Protocol: Amendment 9 | CURRENT | E41 not freeze-worthy; V6-TF developed on val-7 sandbox; protected sets until universal-acmot-v6-freeze; causality frames < t; T4 deferred to pre-paper step; external published-system transfer after freeze | VALIDATION_PROTOCOL.md |
| Decision: D-026 E41 rejected V6-TF target | ACTIVE | E41 never frozen; final target V6-TF developed on val-7; supersedes D-018 and D-025 | DECISIONS.md |
| Decision: D-027 V6-TF is X5 | ACTIVE | duplicate suppression + nested exact-Otsu bands + motion; 0 catastrophic cells val-7, 2 on dev-40 vs V4 3 | DECISIONS.md |
| Experiment: E43 V6 development X1-X5 | DONE DEVELOPMENT | val-7 iterations X1 dedup, X2 no extension, X3 causal, X4 jitter band rejected, X5 nested Otsu selected | EXPERIMENT_REGISTRY.md |
| Experiment: E45 V6 dev-40 robustness | DONE DEVELOPMENT | X5 on development-40, not iterated: 2 catastrophic cells vs V4 3 and E41 15 | EXPERIMENT_REGISTRY.md |
| Experiment: E48 confirmation-16 | PLANNED POST-FREEZE | one-way evaluation of frozen V6-TF vs V4 vs shared-static, paired bootstrap 10000 seed 42 | NEXT_STEPS.md |
| Component: Duplicate Suppression | FINAL | class-agnostic greedy suppression at the IoU-0.5 correspondence rule | ARCHITECTURE.md |
| Component: Nested Otsu Bands | FINAL | background/foreground then extension/primary exact 2-class Otsu on pooled logits of frames t-10..t-1 | ARCHITECTURE.md |
| Experiment: E54 SparseTrack external transfer | DONE NEGATIVE | SparseTrack TCSVT 2025 faithful execution plus frozen V6-TF on identical detections: HOTA -4.15, MOTA -6.14, IDF1 -4.49; dedup and over-conservative bands in crowds | EXPERIMENT_REGISTRY.md |
| Decision: D-029 external transfer negative | ACTIVE | SparseTrack headline, BoostTrack supporting; frozen V6-TF degrades both; scope restricted to calibration and domain shift | DECISIONS.md |
| Version: V7 | FINAL TARGET FROZEN | latest frozen version and approved final version (tag universal-acmot-v7-freeze, 488df9a; Amendment 10); V7f self-limiting control layer between frozen detector and frozen tracker: nested Otsu on logits of frames t-10..t-1, whole-stream clean/noisy mode, host contract, rank remap, continuation rescue; frozen policy behind Paper 2 SCL | FROZEN_VERSIONS.md |
| Tag: universal-acmot-v7-freeze | FROZEN | V7f freeze commit 488df9a 2026-09-28 | FROZEN_VERSIONS.md |
| Lock: V7_POLICY_LOCK | ACTIVE | file hashes of the frozen V7f policy, config and evaluation scripts | ../V7_POLICY_LOCK.json |
| Tag: acmot-v3-exp-2026-10-04-freeze | FROZEN | AC-MOT V3 paper-ready experiment archive 280b4a2 evidence for Paper 1 | FROZEN_VERSIONS.md |
| Person: Ahmed Gouda Ismail | AUTHOR | M.Sc. student corresponding author of all papers a7medgouda1@gmail.com | PAPERS.md |
| Person: Mohamed S. Mohamed | SUPERVISOR | Associate Professor Computer Engineering and Artificial Intelligence Department Military Technical College second author | PAPERS.md |
| Person: Tarek Ahmed Mahmoud | SUPERVISOR | Professor Computer Engineering Department Egypt University of Informatics third author | PAPERS.md |
| Paper: Paper 0 ICMISI survey | PUBLISHED | Real-Time Object Detection and Tracking: Challenges, Innovations and Future Directions; IEEE ICMISI 2026 pp 119-125 DOI 10.1109/ICMISI69868.2026.11583994 | PAPERS.md |
| Paper: Paper 1 AC-MOT JAIS | SUBMITTED | Optimization-Guided Adaptive Detector Operating-Point Control for Multi-Object Aerial Tracking; training-free scene-adaptive operating-point controller; JAIS manuscript 2026-10-I012138 | PAPERS.md |
| Paper: Paper 2 SCL JRTIP | IN PREPARATION | Training-Free Self-Calibrating Control Layer for Heterogeneous Multi-Object Trackers; frozen V7f; target The Visual Computer (D-036, was JRTIP); not submitted | PAPERS.md |
| Venue: IEEE ICMISI 2026 | CONFERENCE | Machine Intelligence and Smart Innovation Alexandria May 9-11 2026 IEEE catalog CFP26UT0-POD | PAPERS.md |
| Venue: Journal of Aerospace Information Systems | JOURNAL | AIAA JAIS ScholarOne mc.manuscriptcentral.com/aiaa new-aiaa template 20-26 pages abstract 100-200 words no acronyms OA optional | PAPERS.md |
| Venue: Journal of Real-Time Image Processing | FORMER TARGET | Springer JRTIP sn-jnl template two-column abstract up to 250 words Statements and Declarations required | PAPERS.md |
| Submission: JAIS 2026-10-I012138 | SUBMITTED | Paper 1 submitted 18-Oct-2026 Full Paper with V12 PDF; co-author confirmations pending; declarations check in Author Center | PAPERS.md |
| Method: AC-MOT operating-point controller | PAPER 1 METHOD | selects LOW MEDIUM HIGH detector operating point every 10 frames from SCI scene cues with recovery probe hysteresis 30-frame dwell; training-free | PAPERS.md |
| Method: SCL self-calibrating control layer | PAPER 2 METHOD | the frozen V7f layer presented as SCL; clean mode keeps tracker settings, noisy mode remaps scores and sets thresholds, rescue for single-stage trackers | PAPERS.md |
| Manuscript: Paper1_V5 Springer | SENT TO SUPERVISOR | all 12 handwritten supervisor comments applied research/acmot_paper_v2/Paper1_Springer_Template/Paper1_V5 | PAPERS.md |
| Manuscript: Paper1_V6 Springer | SUPERSEDED | Springer version with clear Algorithm 1; 42 percent overlap with JAIS version do not double submit | PAPERS.md |
| Manuscript: Paper1_V12_JAIS | SUBMITTED VERSION | AIAA 26 pages abstract relative percentages final author titles research/acmot_paper_v2/Paper1_JAIS/Paper1_V12_JAIS | PAPERS.md |
| Manuscript: Paper1_V13_JAIS | REVISION READY | V12 plus AI-assisted language editing Acknowledgments and SUBMISSION_HANDOFF.md research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS | PAPERS.md |
| Manuscript: Paper2_V10 | SUPERSEDED | Paper 1 supervisor comments applied JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev10 | PAPERS.md |
| Manuscript: Paper2_V11 | COMPLETED | abstract relative percentages 249 words Algorithm 1 Input Output 12 pages JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11 | PAPERS.md |
| Manuscript: Paper2_V12 | NOT USED | The Visual Computer version with the full audit additions, kept unchanged, not used (D-037), JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev12 | PAPERS.md |
| Manuscript: Paper2_V13 | SUPERSEDED BY V14 | V11 content with the journal requirements only, 12 pages, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev13 | PAPERS.md |
| Manuscript: Paper2_V14 | SUPERSEDED BY V15 | V13 content in the standard two-column Springer Nature layout, 17 pages, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev14 | PAPERS.md |
| Manuscript: Paper2_V15 | SUPERSEDED BY V16 | V14 content in the template peer-review layout, 36 pages, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev15 | PAPERS.md |
| Manuscript: Paper2_V16 | SUPERSEDED BY V17 | V15 + held-out VisDrone confirmation-16 result (E55), 37 pages, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev16 | PAPERS.md |
| Manuscript: Paper2_V17 | SUPERSEDED BY V18 | V16 with every journal figure rule met, 37 pages, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev17 | PAPERS.md |
| Manuscript: Paper2_V18 | SUPERSEDED BY V19 | V17 + held-out UAVDT result (E56), 38 pages, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev18 | PAPERS.md |
| Manuscript: Paper2_V19 | LATEST ACTIVE | V18 + seven The Visual Computer references, 39 pages, ready for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev19 | PAPERS.md |
| Manuscript: Paper2_V20 | ACTIVE (supervisor copy) | V19 without the VisDrone result, owner-requested challenge copy for the supervisor, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev20 | PAPERS.md |
| Manuscript: Paper2_V21 | ACTIVE (supervisor copy) | V20 with polished simple English, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev21 | PAPERS.md |
| Manuscript: Paper2_V22 | ACTIVE (supervisor copy) | V21 in two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev22 | PAPERS.md |
| Manuscript: Paper2_V23 | ACTIVE (supervisor copy) | V22 in the journal submission layout with E57/E58 (positive cells), not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev23 | PAPERS.md |
| Manuscript: Paper2_V24 | ACTIVE (supervisor copy) | V23 content in two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev24 | PAPERS.md |
| Manuscript: Paper2_V25 | ACTIVE (supervisor copy) | V24 with exact rho definition, figure/table fixes and the ACT comparison (E59, halved-score cells), two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev25 | PAPERS.md |
| Manuscript: Paper2_V26 | ACTIVE (supervisor copy) | V25 with the ACT comparison on MOT17 and UAVDT (E60, Table 13), two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev26 | PAPERS.md |
| Manuscript: Paper2_V27 | ACTIVE (supervisor copy) | V26 with IDS in every result table, a terms table and a plain-English pass, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev27 | PAPERS.md |
| Manuscript: Paper2_V28 | ACTIVE (supervisor copy) | V27 with identity switches in the narrative and figures redrawn to the journal artwork rules, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev28 | PAPERS.md |
| Manuscript: Paper2_V29 | ACTIVE (supervisor copy) | V28 without the running-time and analysis text, with a score-groups figure and a KITTI example frame, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev29 | PAPERS.md |
| Manuscript: Paper2_V30 | ACTIVE (supervisor copy) | V29 restructured to follow Paper 1's sections and style (background with datasets, metric equations and survey; short discussion), two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev30 | PAPERS.md |
| Manuscript: Paper2_V31 | ACTIVE (supervisor copy) | V30 with the review wording fixes (score-distribution modes, frozen host with per-frame thresholds, qualified claims), two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev31 | PAPERS.md |
| Manuscript: Paper2_V32 | ACTIVE (supervisor copy) | positives-only challenge copy of V31 (caveats and unfavourable IDS columns removed, numbers unchanged), two columns, 26 pages, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev32 | PAPERS.md |
| Manuscript: Paper2_V33 | ACTIVE (supervisor copy) | V32 in 25 pages (layout and wording only, numbers unchanged), two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev33 | PAPERS.md |
| Manuscript: Paper2_V34 | ACTIVE (supervisor copy) | 16-page condensed version of V33 (all results kept, duplicate visuals removed), two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev34 | PAPERS.md |
| Manuscript: Paper2_V35 | ACTIVE (supervisor copy) | 15-page version of V34 with track paths in the KITTI example figure, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev35 | PAPERS.md |
| Manuscript: Paper2_V36 | ACTIVE (supervisor copy) | V35 without the Statements and Declarations section, 15 pages, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev36 | PAPERS.md |
| Manuscript: Paper2_V37 | ACTIVE (supervisor copy) | V36 with the three-frame tracking figure (colours per track ID, track paths), 15 pages, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev37 | PAPERS.md |
| Manuscript: Paper2_V38 | ACTIVE (supervisor copy) | V37 with the review wording fixes (positives-only), 15 pages, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev38 | PAPERS.md |
| Manuscript: Paper2_V39 | ACTIVE (supervisor copy) | V38 without Sect. 3.7 (algorithm and runtime table kept), 15 pages, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev39 | PAPERS.md |
| Manuscript: Paper2_V40 | ACTIVE (supervisor copy) | V39 without the running-time table, 15 pages, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev40 | PAPERS.md |
| Manuscript: Paper2_V41 | ACTIVE (supervisor copy) | V40 with the abstract below 250 words, 15 pages, two columns, not for submission, JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev41 | PAPERS.md |
| Decision: D-042 V7f on UAVDT test | ACTIVE | owner-authorized single run of the frozen V7f, preregistered, reported in Paper2_V18 | DECISIONS.md |
| Decision: D-041 V7f on VisDrone confirmation-16 | ACTIVE | owner-authorized single run of the frozen V7f, preregistered, reported in Paper2_V16 | DECISIONS.md |
| Decision: D-040 Paper2_V15 template peer-review layout | ACTIVE | official template manual followed: single column, referee, flat figures, eight declarations | DECISIONS.md |
| Decision: D-039 Paper2_V14 standard template layout | ACTIVE | V13 content, journal formatting rules applied, no content added | DECISIONS.md |
| Decision: D-037 Paper2_V13 keeps V11 content | ACTIVE | only journal requirements and clarity fixes added to V11 | DECISIONS.md |
| Venue: The Visual Computer | JOURNAL TARGET | Springer ISSN 1432-2315 single-blind abstract 150-250 words 4-6 keywords numbered references Statements and Declarations author biographies | PAPERS.md |
| Decision: D-036 Paper 2 to The Visual Computer | ACTIVE | Paper2_V12 with audit fixes for The Visual Computer | DECISIONS.md |
| Review: Paper2_V11 internal audit | OPEN | 9 verified items: VisDrone dev data missing in data table, 3 KITTI cells omitted incl BoT-SORT YOLOv8n MOTA -2.43, BoT-SORT 0020 Cholesky failure misdescribed, host contract values, rank memory, real-time wording, Hybrid-SORT cause, external scope, Springer declarations | PAPERS.md |
| Rule: Paper versioning and testing | ACTIVE | new folder per version; PDF + standalone main.tex + overleaf zip; 0 errors 0 overfull 0 undefined; integrity check; clean-folder compile; push only when owner says push | PAPERS.md |
| Dataset: MOT17 | USED | val-half 7 sequences published YOLOX-X detections Paper 2 development and predeclared external | PAPERS.md |
| Dataset: KITTI tracking | USED | training 21 sequences RT-DETR-L and YOLOv8n Paper 2 development detector transfer | PAPERS.md |
| Tracker: OATrack | USED | quality-gated tracker host in Paper 1 | PAPERS.md |
| Protocol: Amendment 10 | CURRENT | owner decision 2026-10-20: V7 frozen V7f is the approved final version; V6-TF history; no retuning | VALIDATION_PROTOCOL.md |
| Decision: D-032 V7f approved final version | ACTIVE | C0 amended to V7 frozen V7f; V6-TF frozen history; V4 baseline only; Paper 2 presents V7f | DECISIONS.md |
| Line: legacy thesis AC-MOT | HISTORY | handcrafted SCI controls detector resolution and confidence; YOLOv8n ByteTrack; tag v1.0.0-acmot-frozen | VERSION_HISTORY.md |
| Line: Universal AC-MOT layer | CURRENT | candidate admission scores and thresholds between frozen detector and frozen tracker; V1 to V7f | VERSION_HISTORY.md |
| Line: compute layers on V7f | DEVELOPMENT | detector compute upstream of frozen V7f: C1 SCI plus V7f, G1 constant compute, G2 gate; none adopted beyond a static compute point | VERSION_HISTORY.md |
| Line: Paper 1 operating-point controller | PAPER 1 | AC-MOT v3 controller of detector operating point resolution NMS IoU confidence floor from a crowd scene index; YOLO11m ByteTrack OATrack | VERSION_HISTORY.md |
| Version: V7a-V7d | DEVELOPMENT NOT FROZEN | rho regime host-anchored clean mode crowd-safe duplicates; tag v7-dev-assets-1 d56bba0 | VERSION_HISTORY.md |
| Version: C1 SCI plus V7f | NOT ADOPTED | historical SCI resolution rule upstream of frozen V7f candidate 5a8502f; -0.17 HOTA vs V7f only | VERSION_HISTORY.md |
| Version: G1 constant compute plus V7f | DEVELOPMENT CANDIDATE FROZEN | tag general-acmot-g1-freeze 751c602; behaviourally V7f at 736 px | VERSION_HISTORY.md |
| Version: G2 compute adaptation | GATE FAILED | resolution call-rate crop spaces fail the GT-oracle gate; static compute plus V7f | VERSION_HISTORY.md |
| Version: AC-MOT v3 controller | PAPER 1 FROZEN ARCHIVE | frozen at 309dca5; actions 1536/0.70/0.10 1280/0.45/0.40 1088/0.60/0.40; tau_m 0.297 tau_h 0.511; archive tag acmot-v3-exp-2026-10-04-freeze | VERSION_HISTORY.md |
| Mechanism: nested Otsu bands | IMPLEMENTED | two exact Otsu splits t1 t2 on pooled logits of frames t-10..t-1; acmot_v7 _bands | CODE_ARCHITECTURE.md |
| Mechanism: clean noisy mode | IMPLEMENTED | clean if median confident share rho over past non-cold frames >= 0.5; clean keeps host thresholds raw scores | CODE_ARCHITECTURE.md |
| Mechanism: background check | IMPLEMENTED | rho = 1 when fewer candidates below t1 than above; prevents wrong noisy decisions | CODE_ARCHITECTURE.md |
| Mechanism: rank score remap | IMPLEMENTED | noisy mode scores 0.5+0.5u confident 0.1+0.4u uncertain; u mid-rank ECDF of memory of 20 samples frame 1 and every 10th frame | CODE_ARCHITECTURE.md |
| Mechanism: crowd-safe duplicates | IMPLEMENTED | track-context duplicate rule in noisy frames, cross-class only in clean frames | CODE_ARCHITECTURE.md |
| Mechanism: continuation rescue | IMPLEMENTED | foreground candidate continuing an unmatched track passed just above the host lowest threshold; single-stage hosts | CODE_ARCHITECTURE.md |
| Mechanism: motion tolerance | IMPLEMENTED | match tolerance min(0.95, 1-(1-m0)/max(1,r)) from phase-correlation motion ratio, noisy frames only | CODE_ARCHITECTURE.md |
| Mechanism: host contract | IMPLEMENTED | tracker published settings a b l m0 declared by its adapter | CODE_ARCHITECTURE.md |
| Mechanism: SCI scene index | IMPLEMENTED | crowd cue from tracks of earlier frames; three levels with recovery probe hysteresis 30-frame dwell; acmot_sci SceneLayer | CODE_ARCHITECTURE.md |
| Mechanism: adaptive resolution before detector | REJECTED | V5-TF F5 R-res and C1 SCI compute rule; not better than random or constant compute | CODE_ARCHITECTURE.md |
| Module: acmot_v7.py V7Layer | CODE | V7 layer; V7f config; step L326 observe L478 _bands L289 _ecdf L319 | CODE_ARCHITECTURE.md |
| Module: acmot_sci.py SceneLayer | CODE | Paper 1 scene layer; decide L117 observe L113 | CODE_ARCHITECTURE.md |
| Module: acmot_sci_v7.py LevelSource | CODE | compute level upstream of V7f (C1 G1) | CODE_ARCHITECTURE.md |
| Module: acmot_g2.py G2Pipeline | CODE | G2 compute schedules | CODE_ARCHITECTURE.md |
| Module: online_calibration.py | CODE | exact Otsu nested_otsu dedup for V5-TF V6-TF | CODE_ARCHITECTURE.md |
| Module: tools/v7/dev.py | CODE | V7 development runner with protected-split guard | CODE_ARCHITECTURE.md |
| Module: tools/v7/bootstrap.py | CODE | paired sequence bootstrap 10000 seed 42 | CODE_ARCHITECTURE.md |
| Module: tools/v7/kitti/kitti_eval.py | CODE | official KITTI HOTA car pedestrian average | CODE_ARCHITECTURE.md |
| Module: tools/v7/mot17_eval_v7.py | CODE | TrackEval MOT17 val-half evaluation | CODE_ARCHITECTURE.md |
| Module: tools/v7/benchmark.py | CODE | live runtime benchmark | CODE_ARCHITECTURE.md |
| Module: tools/v6/eval_official.py | CODE | official-compatible VisDrone evaluation used by V6 V7 and Paper 1 | CODE_ARCHITECTURE.md |
| Module: adapters/trackers/oatrack.py | CODE | OATrack re-implementation for Paper 1 | CODE_ARCHITECTURE.md |
| Module: run_v3_joint_search.py | CODE | Paper 1 Phase B TPE search and run_policy_with_conf | CODE_ARCHITECTURE.md |
| Module: run_v3_second_val_read.py | CODE | Paper 1 final VisDrone second val read | CODE_ARCHITECTURE.md |
| Experiment: V7-E16 whole-stream mode | ADOPTED | ByteTrack 0.1 67.561 to 67.702; OC-SORT 65.697 to 66.071 | EXPERIMENT_REGISTRY.md |
| Experiment: V7-E17 continuation rescue | ADOPTED | OC-SORT 0.01 66.405 to 66.619; KITTI YOLOv8n OC 41.14 to 44.15 | EXPERIMENT_REGISTRY.md |
| Experiment: V7-E18 background check | ADOPTED | completes V7f; OC-SORT 0.01 67.041 | EXPERIMENT_REGISTRY.md |
| Experiment: V7-E19 KITTI motion rule | DONE | effects within 0.12 HOTA; BoT-SORT 0020 Cholesky error with layer output | EXPERIMENT_REGISTRY.md |
| Experiment: V7-E20 host-relative band | REJECTED | 26.9 vs 14.9 boxes per frame on noisy VisDrone RT-DETR stream | EXPERIMENT_REGISTRY.md |
| Experiment: V7-STRESS-L score shifts | REPRODUCIBLE | 14 conditions 7 significant recoveries 0 degradations; calib_boot.json | EXPERIMENT_REGISTRY.md |
| Experiment: V7-POST-ST SparseTrack | REPRODUCIBLE | 68.876 to 68.931 HOTA n.s.; GitHub Actions | EXPERIMENT_REGISTRY.md |
| Experiment: V7-POST-PD PD-SORT external | REPRODUCIBLE | HOTA +0.61 CI above zero MOTA +1.13 IDF1 +0.82 7/7 sequences | EXPERIMENT_REGISTRY.md |
| Experiment: V7-POST-HS Hybrid-SORT external | REPRODUCIBLE | identical output; reproduction CLOSE 66.698 vs 67.1 | EXPERIMENT_REGISTRY.md |
| Experiment: V7-POST-CTW C-TWiX external | REPRODUCIBLE | KITTIMOT car -1.52 HOTA CI below zero; MOT17 -0.05 DanceTrack -1.00 n.s. | EXPERIMENT_REGISTRY.md |
| Experiment: V7-POST-TOP TOPICTrack external | FAILED REPRODUCTION | 67.538 vs 69.6; excluded | EXPERIMENT_REGISTRY.md |
| Experiment: V7-POST-TT TrackTrack external | REPRODUCIBLE | DanceTrack -0.012 HOTA CI below zero; near pass-through | EXPERIMENT_REGISTRY.md |
| Experiment: V7-POST-VD VisDrone val-7 | PARTIALLY REPRODUCIBLE | YOLOv8n internal HOTA +2.17; official catastrophic cells 7 to 4; development split | EXPERIMENT_REGISTRY.md |
| Experiment: V7-POST-RT runtime | REPRODUCIBLE | 2.95 ms mean 4.39 ms P95 per frame 4-vCPU Xeon; pipeline 57.85 to 60.44 ms | EXPERIMENT_REGISTRY.md |
| Experiment: SCI-E1 SCI plus V7f | DONE NEGATIVE | -0.17 HOTA vs V7f only | EXPERIMENT_REGISTRY.md |
| Experiment: G2 oracle gate | DONE NEGATIVE | all compute spaces fail the gate | EXPERIMENT_REGISTRY.md |
| Experiment: P1-BASE baseline systems | PARTIALLY REPRODUCIBLE | r1536_n70 ByteTrack HOTA 41.586 OATrack 46.770 | EXPERIMENT_REGISTRY.md |
| Experiment: P1-A Phase A searches | DONE NEGATIVE | no policy beat the calibration matched-static point | EXPERIMENT_REGISTRY.md |
| Experiment: P1-B V3 joint search | PARTIALLY REPRODUCIBLE | 60-trial TPE; trial 7 frozen at 309dca5 | EXPERIMENT_REGISTRY.md |
| Experiment: P1-SHUF shuffled control | LIMITATION | timing value beyond the action mix not shown | EXPERIMENT_REGISTRY.md |
| Experiment: P1-STATIC first val read | DONE | static no-op policy bfa5caf | EXPERIMENT_REGISTRY.md |
| Experiment: P1-V3 second val read | PARTIALLY REPRODUCIBLE | ByteTrack HOTA 41.586 to 44.523 OATrack 46.770 to 48.095; commit 0af0066 | EXPERIMENT_REGISTRY.md |
| Experiment: P1-UAVDT transfer | PARTIALLY REPRODUCIBLE | MOTA ByteTrack -1.573 to 16.028 OATrack 19.607 to 22.873 | EXPERIMENT_REGISTRY.md |
| Experiment: P1-RT runtime | PARTIALLY REPRODUCIBLE | 4.256 and 4.201 ms controller overhead Tesla T4 | EXPERIMENT_REGISTRY.md |
| Experiment: P1-LEGACY U2MOT SparseTrack | HISTORICAL | Colab runs audited; artifacts on Drive | EXPERIMENT_REGISTRY.md |
| Result: V7 main results | CANONICAL | research/final/V7_MAIN_RESULTS.json | RESULTS_CANONICAL.md |
| Result: V7 recent externals | CANONICAL | research/final/V7_RECENT_EXTERNAL_RESULTS.json; negative or neutral | RESULTS_CANONICAL.md |
| Result: V7 KITTI six cells | CANONICAL | research/final/V7_STATISTICS.md; 3 positive 3 not | RESULTS_CANONICAL.md |
| Result: Paper 1 VisDrone second read | CANONICAL | research/acmot_paper_v2/SECOND_VAL_READ_V3_RESULT.json with BASELINE_SYSTEMS_RESULT.json | RESULTS_CANONICAL.md |
| Result: Paper 1 UAVDT transfer | CANONICAL | research/acmot_paper_v2/UAVDT_TRANSFER_RESULT.json | RESULTS_CANONICAL.md |
| Claim: P2 single-stage HOTA plus 0.9 percent | VERIFIED | OC-SORT 66.428 to 67.041 and PD-SORT 68.011 to 68.624 | PAPERS.md |
| Claim: P2 halved scores recover 97 percent | VERIFIED | 66.166 of 67.698 and 66.72 of 66.428 | PAPERS.md |
| Claim: P2 RT-DETR MOTA plus 12.6 and 16.3 percent | VERIFIED INCOMPLETE | 3 of 6 KITTI cells reported | PAPERS.md |
| Claim: P2 external validation | INCOMPLETE REPORTING | recent externals omitted | PAPERS.md |
| Claim: P2 real-time | TO NARROW | layer 2.95 ms; full pipeline about 16.5 FPS | PAPERS.md |
| Claim: P1 ByteTrack HOTA plus 7.1 percent | VERIFIED | 41.586 to 44.523 second val read | PAPERS.md |
| Claim: P1 UAVDT OATrack MOTA plus 16.7 percent | VERIFIED | 19.607 to 22.873 | PAPERS.md |
| Claim: P1 4.2 ms on T4 | VERIFIED | 4.256 and 4.201 ms | PAPERS.md |
| Figure: Paper 2 fig3 forest | SCRIPT NOT FOUND | JRTIP fig3_forest_col.pdf md5 6d64acca has no generation script in the repository | PAPERS.md |
| Figure: Paper 2 fig4 fig5 | TRACED | byte-identical to outputs of JAIS_PAPERS/PAPER2_UNIVERSAL_ACMOT_JAIS/scripts/make_figures.py | PAPERS.md |
| Conflict: CF-02 BoT-SORT 0020 caption | FIXED IN PAPER2_V12 | caption says unmodified tracker fails; ledger E19 says Cholesky error with layer output | RESULTS_CANONICAL.md |
| Conflict: CF-03 KITTI cells omitted | FIXED IN V12, NOT IN V13 (D-037) | Paper2_V11 shows 3 of 6 cells | RESULTS_CANONICAL.md |
| Conflict: CF-04 recent externals omitted | FIXED IN V12, NOT IN V13 (D-037) | negative or neutral predeclared externals not reported | RESULTS_CANONICAL.md |
| Conflict: CF-05 aerial val README | EXPLAINED | README run table predates the successful runs | RESULTS_CANONICAL.md |
| Conflict: CF-07 Paper 1 second val read | OPEN | V12 does not state that val-7 was read twice | RESULTS_CANONICAL.md |
| Failure: FX-20 V6-TF external negative | FAILED | SparseTrack -4.15 BoostTrack -5.89 HOTA | FAILED_EXPERIMENTS.md |
| Failure: FX-24 V7f KITTI YOLOv8n regression | FAILED | two-stage MOTA -1.87 -2.43 | FAILED_EXPERIMENTS.md |
| Failure: FX-25 V7f recent externals | FAILED | C-TWiX KITTIMOT -1.52; TrackTrack -0.012 | FAILED_EXPERIMENTS.md |
| Failure: FX-26 SCI plus V7f | FAILED | no gain over V7f only | FAILED_EXPERIMENTS.md |
| Failure: FX-27 G2 gate | FAILED | no compute headroom at matched compute | FAILED_EXPERIMENTS.md |
| Failure: FX-28 Paper 1 Phase A null | FAILED | no policy beat matched static | FAILED_EXPERIMENTS.md |
| Failure: FX-29 Paper 1 shuffled control | FAILED | timing value not shown | FAILED_EXPERIMENTS.md |
| Dataset: DanceTrack | USED EXTERNAL | val 25 sequences; C-TWiX and TrackTrack recent externals | DATASETS_AND_SPLITS.md |
| Dataset: KITTIMOT val | USED EXTERNAL | C-TWiX recent external car and pedestrian | DATASETS_AND_SPLITS.md |
| Split: VisDrone2019-MOT-train calibration-8 | PAPER 1 CALIBRATION | 8 sequences 3282 frames 4 folds | DATASETS_AND_SPLITS.md |
| Checkpoint: YOLO11m VisDrone dronefreak | FROZEN | sha256 c6f98247 AGPL-3.0 VisDrone-DET trained; Paper 1 detector | REPRODUCIBILITY.md |
| Tracker: SparseTrack | HOST | IEEE TCSVT 2025 two-stage development host 499844f | EXPERIMENT_REGISTRY.md |
| Tracker: BoostTrack | HOST | MVA 2024 two-stage development host fb5bfc3 | EXPERIMENT_REGISTRY.md |
| Tracker: OC-SORT | HOST | CVPR 2023 single-stage host | EXPERIMENT_REGISTRY.md |
| Tracker: PD-SORT | HOST | IEEE TCE 2025 single-stage predeclared external af21db6 | EXPERIMENT_REGISTRY.md |
| Tracker: Hybrid-SORT | HOST | AAAI 2024 two-stage predeclared external 396f8d3 | EXPERIMENT_REGISTRY.md |
| Tracker: C-TWiX | HOST | Pattern Recognition 2025 recent external 3cff9cc | EXPERIMENT_REGISTRY.md |
| Tracker: TOPICTrack | HOST | IEEE TIP 2025 recent external e7b260f | EXPERIMENT_REGISTRY.md |
| Tracker: TrackTrack | HOST | CVPR 2025 recent external ee7f1c5 | EXPERIMENT_REGISTRY.md |
| Commit: 0af0066 | HISTORY | Paper 1 second val read of frozen v3 | EXPERIMENT_REGISTRY.md |
| Commit: 309dca5 | HISTORY | Paper 1 v3 controller freeze | EXPERIMENT_REGISTRY.md |
| Commit: 488df9a | HISTORY | V7f freeze commit | VERSION_HISTORY.md |
| Decision: D-030 paper registry and venues | ACTIVE | PAPERS.md canonical; Paper 1 JAIS; Paper 2 JRTIP | DECISIONS.md |
| Decision: D-031 Paper 2 audit fixes | ACTIVE | Paper2_V11 not submitted until audit items fixed | DECISIONS.md |
| Decision: D-033 owner-only delete | ACTIVE | AI may create and edit; deletion needs the owner's explicit target-specific approval | DECISIONS.md |
| Decision: D-034 signed approval fail closed | ACTIVE | trailer alone never approval; owner-signed commit verified against trusted keys; fail closed | DECISIONS.md |
| Policy: owner-only delete | ACTIVE | Claude hook, git hooks, CI signature check, rulesets proposal; limits documented | PRESERVATION_POLICY.md |
| Conflict: CF-08 V4 lock rehash | EXPLAINED | TESTDEV_LOCK_V4 hashes match 3ea7d69 not fc003bf | RESULTS_CANONICAL.md |
| Decision: D-035 completed versions immutable | ACTIVE | completed versions read-only to AI; changes go into the next sequential version | DECISIONS.md |
| Decision: D-038 fast workflow | ACTIVE | work first; one deterministic maintenance pass at the end; protections unchanged | DECISIONS.md |
| Policy: completed versions immutable | ACTIVE | registry-backed R9 in Claude hook, git hooks and CI; owner OS lock script | PRESERVATION_POLICY.md |
| Registry: VERSION_REGISTRY | ACTIVE | authoritative status and Git hashes of completed versions; next Paper 1 V14, Paper 2 V12, Universal AC-MOT V8 | VERSION_REGISTRY.md |

## Relations
| Subject | Relation | Object |
|---|---|---|
| Project: Universal AC-MOT | HAS_VERSION | Version: Legacy AC-MOT |
| Project: Universal AC-MOT | HAS_VERSION | Version: V1 |
| Project: Universal AC-MOT | HAS_VERSION | Version: V2 variants |
| Project: Universal AC-MOT | HAS_VERSION | Version: V3 |
| Project: Universal AC-MOT | HAS_VERSION | Version: V4 |
| Project: Universal AC-MOT | HAS_VERSION | Version: V5 learned controller |
| Project: Universal AC-MOT | HAS_VERSION | Version: V5-TF |
| Project: Universal AC-MOT | CURRENT_VERSION | Version: V7 |
| Project: Universal AC-MOT | FINAL_TARGET | Version: V7 |
| Project: Universal AC-MOT | HAS_VERSION | Version: V6-TF |
| Project: Universal AC-MOT | BASELINE_ONLY | Version: V4 |
| Component: Universal AC Controller | HAS_CANDIDATE_RULE | Rule: F5 scene-adaptive resolution R-res |
| Rule: F5R random resolution control | CONTROLS_FOR | Rule: F5 scene-adaptive resolution R-res |
| Rule: F5 scene-adaptive resolution R-res | BELONGS_TO | Component: Compute Latency Constraint |
| Decision: D-018 final target V5-TF | SELECTS | Version: V5-TF |
| Decision: D-018 final target V5-TF | DEMOTES_TO_ABLATION | Version: V4 |
| Decision: D-018 final target V5-TF | RECORDED_IN | Protocol: Amendment 7 |
| Decision: D-019 scene-state control R-res | SELECTS | Rule: F5 scene-adaptive resolution R-res |
| Decision: D-019 scene-state control R-res | RECORDED_IN | Protocol: Amendment 7 |
| Decision: D-020 constant audit rule | GOVERNS | Experiment: E39 constant audit |
| Decision: D-022 E36 selects F3 | SELECTS | Rule: F3 motion-aware association |
| Decision: D-022 E36 selects F3 | REJECTS | Rule: F5 scene-adaptive resolution R-res |
| Decision: D-022 E36 selects F3 | SUPPORTED_BY | Experiment: E36 V5-TF dev validation |
| Decision: D-023 E39 C5 blockers | SUPPORTED_BY | Experiment: E39 constant audit |
| Decision: D-023 E39 C5 blockers | REQUIRES | Experiment: E41 exact-Otsu family |
| Decision: D-024 live replay parity | SUPPORTED_BY | Experiment: E40 F3 live replay parity |
| Constraint: C0 final target V7 | APPLIES_TO | Version: V6-TF |
| Constraint: C0 final target V7 | APPLIES_TO | Version: V4 |
| Constraint: C0 final target V7 | DERIVED_FROM | Decision: D-018 final target V5-TF |
| Protocol: Amendment 7 | GOVERNS | Version: V5-TF |
| Protocol: Amendment 7 | GOVERNS | Experiment: E39 constant audit |
| Experiment: E39 constant audit | EVALUATES | Version: V5-TF |
| Project: Universal AC-MOT | LATEST_FROZEN_VERSION | Version: V7 |
| Project: Universal AC-MOT | NEXT_EXPERIMENT | Experiment: E48 confirmation-16 |
| Version: V1 | SUPERSEDES | Version: Legacy AC-MOT |
| Version: V3 | SUPERSEDES | Version: V1 |
| Version: V4 | SUPERSEDES | Version: V3 |
| Version: V5-TF | SUPERSEDES | Version: V5 learned controller |
| Version: V5-TF | COMPARED_AGAINST | Version: V4 |
| Version: V5-TF | COMPARED_AGAINST | Version: V3 |
| Version: V5-TF | COMPARED_AGAINST | Version: V5 learned controller |
| Version: Legacy AC-MOT | HAS_ARCHITECTURE | Architecture: Original SCI architecture |
| Version: V4 | HAS_ARCHITECTURE | Architecture: V4 compute-budget architecture |
| Version: V5-TF | HAS_ARCHITECTURE | Architecture: V5-TF target architecture |
| Version: Legacy AC-MOT | USES_COMPONENT | Component: Legacy SCI |
| Version: V3 | USES_COMPONENT | Component: Legacy SCI |
| Version: V3 | USES_COMPONENT | Component: Z-logit Leader Gate |
| Version: V4 | USES_COMPONENT | Component: Z-logit Leader Gate |
| Version: V4 | USES_COMPONENT | Component: ECDF Normaliser |
| Version: V4 | USES_COMPONENT | Component: Compute Latency Constraint |
| Version: V5-TF | USES_COMPONENT | Component: Scene State Analyzer |
| Version: V5-TF | USES_COMPONENT | Component: Online Self-Calibration |
| Version: V5-TF | USES_COMPONENT | Component: Universal AC Controller |
| Version: V5-TF | USES_COMPONENT | Component: Compute Latency Constraint |
| Version: V5-TF | USES_COMPONENT | Component: Detector Adapter |
| Version: V5-TF | USES_COMPONENT | Component: ECDF Normaliser |
| Version: V5-TF | USES_COMPONENT | Component: Otsu-3 Candidate Bands |
| Version: V5-TF | USES_COMPONENT | Component: Tracker Adapter |
| Component: Universal AC Controller | HAS_CANDIDATE_RULE | Rule: F1 Otsu window bands |
| Component: Universal AC Controller | HAS_CANDIDATE_RULE | Rule: F2 Otsu frame bands |
| Component: Universal AC Controller | HAS_CANDIDATE_RULE | Rule: F3 motion-aware association |
| Rule: F3 motion-aware association | USES_CUE | Cue: img_motion |
| Decision: D-016 F4 dropped | REJECTS | Rule: F4 online z-gate |
| Decision: D-005 remove legacy SCI | REJECTS | Component: Legacy SCI |
| Decision: D-005 remove legacy SCI | REJECTS | Cue: crowd count n/30 |
| Decision: D-005 remove legacy SCI | REJECTS | Cue: tiny object area |
| Decision: D-005 remove legacy SCI | REJECTS | Cue: img_edges |
| Decision: D-005 remove legacy SCI | REJECTS | Cue: img_brightness |
| Decision: D-005 remove legacy SCI | REJECTS | Cue: img_blur |
| Decision: D-005 remove legacy SCI | SUPPORTED_BY | Experiment: E24-E26 SCI audit |
| Decision: D-010 cue status | REJECTS | Cue: img_edges |
| Decision: D-010 cue status | REJECTS | Cue: img_brightness |
| Decision: D-010 cue status | REJECTS | Cue: img_blur |
| Decision: D-010 cue status | KEEPS_CANDIDATE | Cue: det_gap |
| Decision: D-010 cue status | KEEPS_CANDIDATE | Cue: det_count |
| Decision: D-010 cue status | KEEPS_CANDIDATE | Cue: trk_survival |
| Decision: D-010 cue status | KEEPS_CANDIDATE | Cue: trk_match |
| Decision: D-010 cue status | KEEPS_CANDIDATE | Cue: img_motion |
| Decision: D-010 cue status | KEEPS_CANDIDATE | Cue: img_motion_resp |
| Decision: D-010 cue status | SUPPORTED_BY | Experiment: E33 S2 cue utility |
| Decision: D-009 keep scene adaptation V4 is ablation | SELECTS | Version: V5-TF |
| Decision: D-009 keep scene adaptation V4 is ablation | DEMOTES_TO_ABLATION | Version: V4 |
| Decision: D-009 keep scene adaptation V4 is ablation | EXPLAINS | Architecture: V4 compute-budget architecture |
| Decision: D-011 learned V5 not adopted | SUPPORTED_BY | Experiment: E34-E35 S3 learned controller |
| Decision: D-015 training-free final AC | SUPERSEDES | Decision: D-012 40/16 train split |
| Decision: D-015 training-free final AC | SELECTS | Component: Online Self-Calibration |
| Decision: D-015 training-free final AC | REJECTS | Version: V5 learned controller |
| Decision: D-015 training-free final AC | SUPPORTED_BY | Experiment: E34-E35 S3 learned controller |
| Decision: D-015 training-free final AC | RECORDED_IN | Protocol: Amendment 6 |
| Decision: D-015 training-free final AC | RECORDED_IN | Commit: 3684684 |
| Decision: D-014 fidelity gate constants | RECORDED_IN | Protocol: Amendment 5f |
| Decision: D-016 F4 dropped | RECORDED_IN | Commit: 71faf44 |
| Constraint: C1 training-free final AC layer | APPLIES_TO | Version: V5-TF |
| Constraint: C3 causality | APPLIES_TO | Version: V5-TF |
| Constraint: C5 no category E constants | APPLIES_TO | Version: V5-TF |
| Constraint: C6 AC before detector | APPLIES_TO | Version: V5-TF |
| Constraint: C7 Optuna research-only | APPLIES_TO | Version: V5 learned controller |
| Constraint: C8 protected evaluations | APPLIES_TO | Split: VisDrone2019-MOT-train confirmation-16 |
| Constraint: C8 protected evaluations | APPLIES_TO | Detector: Faster R-CNN ResNet50-FPN v2 |
| Constraint: C8 protected evaluations | APPLIES_TO | Tracker: BoT-SORT |
| Constraint: C8 protected evaluations | APPLIES_TO | Split: UAVDT test |
| Constraint: C9 T4 official timing | APPLIES_TO | Experiment: E38 T4 fidelity gate |
| Constraint: C11 honest reporting | APPLIES_TO | Version: V5-TF |
| Constraint: C1 training-free final AC layer | DERIVED_FROM | Decision: D-015 training-free final AC |
| Constraint: C5 no category E constants | FLAGS | Parameter: OTSU_BINS 64 |
| Constraint: C5 no category E constants | FLAGS | Parameter: Otsu window 10 frames |
| Constraint: C5 no category E constants | EXCLUDES_FROM_V5_TF | Parameter: Z_REF 0.75 |
| Constraint: C5 no category E constants | EXCLUDES | Parameter: V4 tau 0.75 |
| Constraint: C5 no category E constants | EXCLUDES | Parameter: V4 sensitivity 0.4 |
| Constraint: C5 no category E constants | EXCLUDES | Parameter: V4 association offset 0.10 |
| Constraint: C5 no category E constants | EXCLUDES | Parameter: V4 NMS 0.45 |
| Constraint: C5 no category E constants | EXCLUDES | Parameter: V4 tracker 45/0.86 |
| Parameter: RobustHistory window 100 | BELONGS_TO | Component: Online Self-Calibration |
| Parameter: RobustHistory warm-up 5 | BELONGS_TO | Component: Online Self-Calibration |
| Parameter: OTSU_BINS 64 | BELONGS_TO | Component: Otsu-3 Candidate Bands |
| Parameter: Otsu window 10 frames | BELONGS_TO | Component: Otsu-3 Candidate Bands |
| Parameter: Z_REF 0.75 | BELONGS_TO | Component: Scene State Analyzer |
| Parameter: F3 cap 0.95 | BELONGS_TO | Rule: F3 motion-aware association |
| Parameter: native tracker defaults 30/0.8 | BELONGS_TO | Component: Tracker Adapter |
| Parameter: V4 tau 0.75 | BELONGS_TO | Component: Z-logit Leader Gate |
| Parameter: V4 NMS 0.45 | BELONGS_TO | Version: V4 |
| Parameter: V4 sensitivity 0.4 | BELONGS_TO | Version: V4 |
| Parameter: V4 association offset 0.10 | BELONGS_TO | Version: V4 |
| Parameter: V4 tracker 45/0.86 | BELONGS_TO | Version: V4 |
| Parameter: fidelity gate thresholds | BELONGS_TO | Protocol: Amendment 5f |
| Dataset: VisDrone2019-MOT | HAS_SPLIT | Split: VisDrone2019-MOT-val |
| Dataset: VisDrone2019-MOT | HAS_SPLIT | Split: VisDrone2019-MOT-train development-40 |
| Dataset: VisDrone2019-MOT | HAS_SPLIT | Split: VisDrone2019-MOT-train confirmation-16 |
| Dataset: VisDrone2019-MOT | HAS_SPLIT | Split: VisDrone2019-MOT-test-dev |
| Dataset: UAVDT | HAS_SPLIT | Split: UAVDT test |
| Experiment: E31 V4 test-dev held-out | EVALUATES | Version: V4 |
| Experiment: E31 V4 test-dev held-out | USES | Split: VisDrone2019-MOT-test-dev |
| Experiment: E31 V4 test-dev held-out | USES | Detector: YOLOv8n |
| Experiment: E31 V4 test-dev held-out | USES | Detector: RT-DETR-L |
| Experiment: E31 V4 test-dev held-out | USES | Tracker: ByteTrack |
| Experiment: E31 V4 test-dev held-out | USES | Tracker: BoT-SORT |
| Experiment: E31 V4 test-dev held-out | PRODUCES | Result: V4 test-dev pooled metrics |
| Result: V4 test-dev pooled metrics | REPORTS | Metric: HOTA |
| Result: V4 test-dev pooled metrics | REPORTS | Metric: IDF1 |
| Result: V4 test-dev pooled metrics | REPORTS | Metric: MOTA |
| Result: V4 test-dev pooled metrics | REPORTS | Metric: IDS |
| Experiment: E24-E26 SCI audit | EVALUATES | Component: Legacy SCI |
| Experiment: E24-E26 SCI audit | USES | Split: VisDrone2019-MOT-val |
| Experiment: E32 S1 headroom | USES | Split: VisDrone2019-MOT-val |
| Experiment: E33 S2 cue utility | USES | Split: VisDrone2019-MOT-val |
| Experiment: E34-E35 S3 learned controller | EVALUATES | Version: V5 learned controller |
| Experiment: E34-E35 S3 learned controller | USES | Split: VisDrone2019-MOT-val |
| Experiment: E36 V5-TF dev validation | EVALUATES | Version: V5-TF |
| Experiment: E36 V5-TF dev validation | USES | Split: VisDrone2019-MOT-train development-40 |
| Experiment: E36 V5-TF dev validation | USES | Detector: YOLOv8n |
| Experiment: E36 V5-TF dev validation | USES | Detector: RT-DETR-L |
| Experiment: E36 V5-TF dev validation | USES | Tracker: ByteTrack |
| Experiment: E36 V5-TF dev validation | PRODUCES | Result: V5-TF E36 family choice |
| Experiment: E39 constant audit | PRODUCES | Result: V5-TF E39 constant audit |
| Experiment: E39 constant audit | USES | Split: VisDrone2019-MOT-train development-40 |
| Experiment: E40 F3 live replay parity | EVALUATES | Rule: F3 motion-aware association |
| Experiment: E40 F3 live replay parity | USES | Split: VisDrone2019-MOT-train development-40 |
| Failure: F5 size-state resolution below random | DERIVED_FROM | Experiment: E36 V5-TF dev validation |
| Experiment: E37 discovery S1-S3 on train | USES | Split: VisDrone2019-MOT-train development-40 |
| Experiment: E38 T4 fidelity gate | USES | Split: VisDrone2019-MOT-train development-40 |
| Failure: V1 candidate explosion | DERIVED_FROM | Version: V1 |
| Failure: V2 density budgets | DERIVED_FROM | Version: V2 variants |
| Failure: V2f closed-loop trust windup | DERIVED_FROM | Version: V2 variants |
| Failure: J2 max-min objective degenerate | DERIVED_FROM | Version: V1 |
| Failure: V1 temperature non-invariance | DERIVED_FROM | Version: V1 |
| Failure: legacy SCI below random | DERIVED_FROM | Experiment: E24-E26 SCI audit |
| Failure: MOTA-aligned learning cost | DERIVED_FROM | Experiment: E34-E35 S3 learned controller |
| Failure: learned controller overfitting by scarcity | DERIVED_FROM | Experiment: E34-E35 S3 learned controller |
| Failure: unstable gate tau cue | DERIVED_FROM | Experiment: E34-E35 S3 learned controller |
| Failure: V4 RT-DETR below shared static | DERIVED_FROM | Experiment: E31 V4 test-dev held-out |
| Experiment: E17 signal audit | REJECTS | Cue: temporal persistence |
| Experiment: E17 signal audit | USES | Split: VisDrone2019-MOT-val |
| Tag: v1.0.0-acmot-frozen | POINTS_TO | Commit: a6c1fa4 |
| Tag: universal-acmot-v1-freeze | POINTS_TO | Commit: e56c2f3 |
| Tag: universal-acmot-v3-freeze | POINTS_TO | Commit: c1e799d |
| Tag: universal-acmot-v4-freeze | POINTS_TO | Commit: fc003bf |
| Commit: a6c1fa4 | FREEZES | Version: Legacy AC-MOT |
| Commit: e56c2f3 | FREEZES | Version: V1 |
| Commit: c1e799d | FREEZES | Version: V3 |
| Commit: fc003bf | FREEZES | Version: V4 |
| Commit: 71faf44 | IMPLEMENTS | Version: V5-TF |
| Tag: universal-acmot-v5tf-freeze | PLANNED_FOR | Version: V5-TF |
| Protocol: Amendment 6 | GOVERNS | Version: V5-TF |
| Protocol: Amendment 4 | GOVERNS | Version: V4 |
| Protocol: Amendment 5f | GOVERNS | Experiment: E38 T4 fidelity gate |
| Protocol: Amendment 5d | GOVERNS | Split: VisDrone2019-MOT-train confirmation-16 |
| Version: V4 | TESTED_WITH | Detector: YOLOv8n |
| Version: V4 | TESTED_WITH | Detector: RT-DETR-L |
| Version: V4 | TESTED_WITH | Tracker: ByteTrack |
| Version: V4 | TESTED_WITH | Tracker: BoT-SORT |
| Lock: TESTDEV_LOCK_V4 | LOCKS | Split: VisDrone2019-MOT-test-dev |
| Lock: TRANSFER_LOCK_FASTERRCNN | LOCKS | Detector: Faster R-CNN ResNet50-FPN v2 |
| Lock: TRANSFER_LOCK_UAVDT | LOCKS | Split: UAVDT test |
| Lock: TRAIN_SPLIT_V5 | DEFINES_SPLIT | Split: VisDrone2019-MOT-train development-40 |
| Lock: TRAIN_SPLIT_V5 | DEFINES_SPLIT | Split: VisDrone2019-MOT-train confirmation-16 |
| Families: detector and tracker families tested | TESTED_DETECTOR | Detector: YOLOv8n |
| Families: detector and tracker families tested | TESTED_DETECTOR | Detector: RT-DETR-L |
| Families: detector and tracker families tested | CACHED_NOT_EVALUATED | Detector: Faster R-CNN ResNet50-FPN v2 |
| Families: detector and tracker families tested | TESTED_TRACKER | Tracker: ByteTrack |
| Families: detector and tracker families tested | TESTED_TRACKER | Tracker: BoT-SORT |
| Failure: Failures not to repeat | INCLUDES | Failure: V1 candidate explosion |
| Failure: Failures not to repeat | INCLUDES | Failure: V2 density budgets |
| Failure: Failures not to repeat | INCLUDES | Failure: V2f closed-loop trust windup |
| Failure: Failures not to repeat | INCLUDES | Failure: J2 max-min objective degenerate |
| Failure: Failures not to repeat | INCLUDES | Failure: V1 temperature non-invariance |
| Failure: Failures not to repeat | INCLUDES | Failure: legacy SCI below random |
| Failure: Failures not to repeat | INCLUDES | Failure: MOTA-aligned learning cost |
| Failure: Failures not to repeat | INCLUDES | Failure: learned controller overfitting by scarcity |
| Failure: Failures not to repeat | INCLUDES | Failure: unstable gate tau cue |
| Failure: Failures not to repeat | INCLUDES | Failure: V4 RT-DETR below shared static |
| Failure: Failures not to repeat | INCLUDES | Cue: temporal persistence |
| Component: Legacy SCI | HAD_CUE | Cue: crowd count n/30 |
| Component: Legacy SCI | HAD_CUE | Cue: tiny object area |
| Component: Legacy SCI | HAD_CUE | Cue: img_edges |
| Component: Legacy SCI | HAD_CUE | Cue: img_brightness |
| Component: Legacy SCI | HAD_CUE | Cue: img_blur |
| Decision: D-026 E41 rejected V6-TF target | SELECTS | Version: V6-TF |
| Decision: D-026 E41 rejected V6-TF target | RECORDED_IN | Protocol: Amendment 9 |
| Decision: D-026 E41 rejected V6-TF target | SUPERSEDES | Decision: D-018 final target V5-TF |
| Decision: D-027 V6-TF is X5 | SELECTS | Version: V6-TF |
| Experiment: E43 V6 development X1-X5 | EVALUATES | Version: V6-TF |
| Experiment: E45 V6 dev-40 robustness | EVALUATES | Version: V6-TF |
| Experiment: E48 confirmation-16 | EVALUATES | Version: V6-TF |
| Version: V6-TF | SUPERSEDES | Version: V5-TF |
| Version: V6-TF | COMPARED_AGAINST | Version: V4 |
| Version: V6-TF | USES_COMPONENT | Component: Duplicate Suppression |
| Version: V6-TF | USES_COMPONENT | Component: Nested Otsu Bands |
| Version: V6-TF | USES_COMPONENT | Component: ECDF Normaliser |
| Protocol: Amendment 9 | GOVERNS | Version: V6-TF |
| Constraint: C0 final target V7 | DERIVED_FROM | Decision: D-026 E41 rejected V6-TF target |
| Experiment: E54 SparseTrack external transfer | EVALUATES | Version: V6-TF |
| Decision: D-029 external transfer negative | RECORDED_IN | Protocol: Amendment 9 |
| Project: Universal AC-MOT | HAS_VERSION | Version: V7 |
| Version: V7 | FOLLOWS | Version: V6-TF |
| Version: V7 | FROZEN_AS | Tag: universal-acmot-v7-freeze |
| Version: V7 | LOCKED_BY | Lock: V7_POLICY_LOCK |
| Project: Universal AC-MOT | HAS_PAPER | Paper: Paper 0 ICMISI survey |
| Project: Universal AC-MOT | HAS_PAPER | Paper: Paper 1 AC-MOT JAIS |
| Project: Universal AC-MOT | HAS_PAPER | Paper: Paper 2 SCL JRTIP |
| Paper: Paper 0 ICMISI survey | PUBLISHED_IN | Venue: IEEE ICMISI 2026 |
| Paper: Paper 1 AC-MOT JAIS | SUBMITTED_TO | Venue: Journal of Aerospace Information Systems |
| Paper: Paper 2 SCL JRTIP | TARGETS | Venue: The Visual Computer |
| Paper: Paper 1 AC-MOT JAIS | HAS_SUBMISSION | Submission: JAIS 2026-10-I012138 |
| Submission: JAIS 2026-10-I012138 | USES_MANUSCRIPT | Manuscript: Paper1_V12_JAIS |
| Paper: Paper 1 AC-MOT JAIS | LATEST_VERSION | Manuscript: Paper1_V13_JAIS |
| Manuscript: Paper1_V13_JAIS | REVISES | Manuscript: Paper1_V12_JAIS |
| Manuscript: Paper1_V12_JAIS | REVISES | Manuscript: Paper1_V6 Springer |
| Manuscript: Paper1_V6 Springer | REVISES | Manuscript: Paper1_V5 Springer |
| Paper: Paper 1 AC-MOT JAIS | DESCRIBES | Method: AC-MOT operating-point controller |
| Paper: Paper 1 AC-MOT JAIS | EVIDENCE_FROM | Tag: acmot-v3-exp-2026-10-04-freeze |
| Paper: Paper 1 AC-MOT JAIS | EVALUATED_ON | Dataset: VisDrone2019-MOT |
| Paper: Paper 1 AC-MOT JAIS | EVALUATED_ON | Dataset: UAVDT |
| Paper: Paper 1 AC-MOT JAIS | USES_TRACKER | Tracker: ByteTrack |
| Paper: Paper 1 AC-MOT JAIS | USES_TRACKER | Tracker: OATrack |
| Paper: Paper 2 SCL JRTIP | DESCRIBES | Method: SCL self-calibrating control layer |
| Method: SCL self-calibrating control layer | IS_FROZEN_POLICY | Version: V7 |
| Paper: Paper 2 SCL JRTIP | LATEST_VERSION | Manuscript: Paper2_V19 |
| Manuscript: Paper2_V19 | REVISES | Manuscript: Paper2_V18 |
| Manuscript: Paper2_V20 | REVISES | Manuscript: Paper2_V19 |
| Manuscript: Paper2_V21 | REVISES | Manuscript: Paper2_V20 |
| Manuscript: Paper2_V22 | REVISES | Manuscript: Paper2_V21 |
| Manuscript: Paper2_V23 | REVISES | Manuscript: Paper2_V22 |
| Manuscript: Paper2_V24 | REVISES | Manuscript: Paper2_V23 |
| Manuscript: Paper2_V25 | REVISES | Manuscript: Paper2_V24 |
| Manuscript: Paper2_V26 | REVISES | Manuscript: Paper2_V25 |
| Manuscript: Paper2_V27 | REVISES | Manuscript: Paper2_V26 |
| Manuscript: Paper2_V28 | REVISES | Manuscript: Paper2_V27 |
| Manuscript: Paper2_V29 | REVISES | Manuscript: Paper2_V28 |
| Manuscript: Paper2_V30 | REVISES | Manuscript: Paper2_V29 |
| Manuscript: Paper2_V31 | REVISES | Manuscript: Paper2_V30 |
| Manuscript: Paper2_V32 | REVISES | Manuscript: Paper2_V31 |
| Manuscript: Paper2_V33 | REVISES | Manuscript: Paper2_V32 |
| Manuscript: Paper2_V34 | REVISES | Manuscript: Paper2_V33 |
| Manuscript: Paper2_V35 | REVISES | Manuscript: Paper2_V34 |
| Manuscript: Paper2_V36 | REVISES | Manuscript: Paper2_V35 |
| Manuscript: Paper2_V37 | REVISES | Manuscript: Paper2_V36 |
| Manuscript: Paper2_V38 | REVISES | Manuscript: Paper2_V37 |
| Manuscript: Paper2_V39 | REVISES | Manuscript: Paper2_V38 |
| Manuscript: Paper2_V40 | REVISES | Manuscript: Paper2_V39 |
| Manuscript: Paper2_V41 | REVISES | Manuscript: Paper2_V40 |
| Manuscript: Paper2_V18 | REVISES | Manuscript: Paper2_V17 |
| Decision: D-042 V7f on UAVDT test | DECIDES | Manuscript: Paper2_V18 |
| Manuscript: Paper2_V17 | REVISES | Manuscript: Paper2_V16 |
| Manuscript: Paper2_V16 | REVISES | Manuscript: Paper2_V15 |
| Decision: D-041 V7f on VisDrone confirmation-16 | DECIDES | Manuscript: Paper2_V16 |
| Manuscript: Paper2_V15 | REVISES | Manuscript: Paper2_V14 |
| Decision: D-040 Paper2_V15 template peer-review layout | DECIDES | Manuscript: Paper2_V15 |
| Manuscript: Paper2_V14 | REVISES | Manuscript: Paper2_V13 |
| Decision: D-039 Paper2_V14 standard template layout | DECIDES | Manuscript: Paper2_V14 |
| Manuscript: Paper2_V13 | REVISES | Manuscript: Paper2_V11 |
| Decision: D-037 Paper2_V13 keeps V11 content | DECIDES | Manuscript: Paper2_V13 |
| Manuscript: Paper2_V12 | REVISES | Manuscript: Paper2_V11 |
| Decision: D-036 Paper 2 to The Visual Computer | DECIDES | Paper: Paper 2 SCL JRTIP |
| Paper: Paper 2 SCL JRTIP | EVALUATED_ON | Dataset: DanceTrack |
| Manuscript: Paper2_V11 | REVISES | Manuscript: Paper2_V10 |
| Review: Paper2_V11 internal audit | AUDITS | Manuscript: Paper2_V11 |
| Paper: Paper 2 SCL JRTIP | CITES | Paper: Paper 1 AC-MOT JAIS |
| Paper: Paper 2 SCL JRTIP | EVALUATED_ON | Dataset: MOT17 |
| Paper: Paper 2 SCL JRTIP | EVALUATED_ON | Dataset: KITTI tracking |
| Paper: Paper 2 SCL JRTIP | DEVELOPED_ON | Dataset: VisDrone2019-MOT |
| Paper: Paper 2 SCL JRTIP | USES_DETECTOR | Detector: YOLOv8n |
| Paper: Paper 2 SCL JRTIP | USES_DETECTOR | Detector: RT-DETR-L |
| Paper: Paper 2 SCL JRTIP | USES_TRACKER | Tracker: ByteTrack |
| Paper: Paper 2 SCL JRTIP | USES_TRACKER | Tracker: BoT-SORT |
| Person: Ahmed Gouda Ismail | AUTHOR_OF | Paper: Paper 0 ICMISI survey |
| Person: Ahmed Gouda Ismail | AUTHOR_OF | Paper: Paper 1 AC-MOT JAIS |
| Person: Ahmed Gouda Ismail | AUTHOR_OF | Paper: Paper 2 SCL JRTIP |
| Person: Mohamed S. Mohamed | SUPERVISES | Paper: Paper 1 AC-MOT JAIS |
| Person: Mohamed S. Mohamed | SUPERVISES | Paper: Paper 2 SCL JRTIP |
| Person: Tarek Ahmed Mahmoud | SUPERVISES | Paper: Paper 1 AC-MOT JAIS |
| Person: Tarek Ahmed Mahmoud | SUPERVISES | Paper: Paper 2 SCL JRTIP |
| Rule: Paper versioning and testing | GOVERNS | Paper: Paper 1 AC-MOT JAIS |
| Rule: Paper versioning and testing | GOVERNS | Paper: Paper 2 SCL JRTIP |
| Decision: D-032 V7f approved final version | SELECTS | Version: V7 |
| Decision: D-032 V7f approved final version | RECORDED_IN | Protocol: Amendment 10 |
| Constraint: C0 final target V7 | DERIVED_FROM | Decision: D-032 V7f approved final version |
| Constraint: C0 final target V7 | APPLIES_TO | Version: V7 |
| Version: V7 | SUPERSEDES | Version: V6-TF |
| Decision: D-032 V7f approved final version | SUPERSEDES | Decision: D-026 E41 rejected V6-TF target |
| Line: Universal AC-MOT layer | HAS_VERSION | Version: V7 |
| Line: Universal AC-MOT layer | HAS_VERSION | Version: V6-TF |
| Line: Universal AC-MOT layer | HAS_VERSION | Version: V7a-V7d |
| Version: V7 | SUPERSEDES | Version: V7a-V7d |
| Version: V7a-V7d | FOLLOWS | Version: V6-TF |
| Line: legacy thesis AC-MOT | HAS_VERSION | Version: Legacy AC-MOT |
| Line: compute layers on V7f | HAS_VERSION | Version: C1 SCI plus V7f |
| Line: compute layers on V7f | HAS_VERSION | Version: G1 constant compute plus V7f |
| Line: compute layers on V7f | HAS_VERSION | Version: G2 compute adaptation |
| Version: C1 SCI plus V7f | BUILDS_ON | Version: V7 |
| Version: G1 constant compute plus V7f | BUILDS_ON | Version: V7 |
| Version: G2 compute adaptation | BUILDS_ON | Version: V7 |
| Line: Paper 1 operating-point controller | HAS_VERSION | Version: AC-MOT v3 controller |
| Paper: Paper 1 AC-MOT JAIS | DESCRIBES_VERSION | Version: AC-MOT v3 controller |
| Paper: Paper 2 SCL JRTIP | DESCRIBES_VERSION | Version: V7 |
| Version: V7 | USES_MECHANISM | Mechanism: nested Otsu bands |
| Mechanism: nested Otsu bands | IMPLEMENTED_BY | Module: acmot_v7.py V7Layer |
| Version: V7 | USES_MECHANISM | Mechanism: clean noisy mode |
| Mechanism: clean noisy mode | IMPLEMENTED_BY | Module: acmot_v7.py V7Layer |
| Version: V7 | USES_MECHANISM | Mechanism: background check |
| Mechanism: background check | IMPLEMENTED_BY | Module: acmot_v7.py V7Layer |
| Version: V7 | USES_MECHANISM | Mechanism: rank score remap |
| Mechanism: rank score remap | IMPLEMENTED_BY | Module: acmot_v7.py V7Layer |
| Version: V7 | USES_MECHANISM | Mechanism: crowd-safe duplicates |
| Mechanism: crowd-safe duplicates | IMPLEMENTED_BY | Module: acmot_v7.py V7Layer |
| Version: V7 | USES_MECHANISM | Mechanism: continuation rescue |
| Mechanism: continuation rescue | IMPLEMENTED_BY | Module: acmot_v7.py V7Layer |
| Version: V7 | USES_MECHANISM | Mechanism: motion tolerance |
| Mechanism: motion tolerance | IMPLEMENTED_BY | Module: acmot_v7.py V7Layer |
| Version: V7 | USES_MECHANISM | Mechanism: host contract |
| Mechanism: host contract | IMPLEMENTED_BY | Module: acmot_v7.py V7Layer |
| Version: V6-TF | USES_MECHANISM | Mechanism: nested Otsu bands |
| Version: V6-TF | USES_MECHANISM | Mechanism: motion tolerance |
| Version: AC-MOT v3 controller | USES_MECHANISM | Mechanism: SCI scene index |
| Mechanism: SCI scene index | IMPLEMENTED_BY | Module: acmot_sci.py SceneLayer |
| Version: C1 SCI plus V7f | USES_MECHANISM | Mechanism: adaptive resolution before detector |
| Failure: FX-26 SCI plus V7f | REJECTS | Mechanism: adaptive resolution before detector |
| Version: V7 | IMPLEMENTED_IN_MODULE | Module: acmot_v7.py V7Layer |
| Version: C1 SCI plus V7f | IMPLEMENTED_IN_MODULE | Module: acmot_sci.py SceneLayer |
| Version: C1 SCI plus V7f | IMPLEMENTED_IN_MODULE | Module: acmot_sci_v7.py LevelSource |
| Version: G1 constant compute plus V7f | IMPLEMENTED_IN_MODULE | Module: acmot_sci_v7.py LevelSource |
| Version: G2 compute adaptation | IMPLEMENTED_IN_MODULE | Module: acmot_g2.py G2Pipeline |
| Version: V6-TF | IMPLEMENTED_IN_MODULE | Module: online_calibration.py |
| Version: AC-MOT v3 controller | IMPLEMENTED_IN_MODULE | Module: acmot_sci.py SceneLayer |
| Version: AC-MOT v3 controller | IMPLEMENTED_IN_MODULE | Module: run_v3_joint_search.py |
| Version: AC-MOT v3 controller | FROZEN_AT | Commit: 309dca5 |
| Version: V7 | FROZEN_AT | Commit: 488df9a |
| Experiment: V7-E16 whole-stream mode | LED_TO | Version: V7 |
| Experiment: V7-E17 continuation rescue | LED_TO | Version: V7 |
| Experiment: V7-E18 background check | LED_TO | Version: V7 |
| Experiment: V7-E16 whole-stream mode | SUPPORTS | Mechanism: clean noisy mode |
| Experiment: V7-E17 continuation rescue | SUPPORTS | Mechanism: continuation rescue |
| Experiment: V7-E18 background check | SUPPORTS | Mechanism: background check |
| Experiment: V7-E20 host-relative band | REJECTED_BY_EVIDENCE | Version: V7a-V7d |
| Failure: FX-20 V6-TF external negative | MOTIVATED | Version: V7a-V7d |
| Experiment: V7-STRESS-L score shifts | EVALUATES | Version: V7 |
| Experiment: V7-POST-ST SparseTrack | EVALUATES | Version: V7 |
| Experiment: V7-POST-PD PD-SORT external | EVALUATES | Version: V7 |
| Experiment: V7-POST-HS Hybrid-SORT external | EVALUATES | Version: V7 |
| Experiment: V7-POST-CTW C-TWiX external | EVALUATES | Version: V7 |
| Experiment: V7-POST-TOP TOPICTrack external | EVALUATES | Version: V7 |
| Experiment: V7-POST-TT TrackTrack external | EVALUATES | Version: V7 |
| Experiment: V7-POST-VD VisDrone val-7 | EVALUATES | Version: V7 |
| Experiment: V7-POST-RT runtime | EVALUATES | Version: V7 |
| Experiment: V7-E19 KITTI motion rule | EVALUATES | Version: V7 |
| Experiment: V7-E19 KITTI motion rule | USES_MODULE | Module: tools/v7/kitti/kitti_eval.py |
| Experiment: V7-POST-PD PD-SORT external | USES_MODULE | Module: tools/v7/mot17_eval_v7.py |
| Experiment: V7-POST-RT runtime | USES_MODULE | Module: tools/v7/benchmark.py |
| Experiment: V7-POST-VD VisDrone val-7 | USES_MODULE | Module: tools/v7/dev.py |
| Experiment: V7-STRESS-L score shifts | USES_MODULE | Module: tools/v7/bootstrap.py |
| Experiment: V7-POST-PD PD-SORT external | USES_TRACKER | Tracker: PD-SORT |
| Experiment: V7-POST-HS Hybrid-SORT external | USES_TRACKER | Tracker: Hybrid-SORT |
| Experiment: V7-POST-CTW C-TWiX external | USES_TRACKER | Tracker: C-TWiX |
| Experiment: V7-POST-TOP TOPICTrack external | USES_TRACKER | Tracker: TOPICTrack |
| Experiment: V7-POST-TT TrackTrack external | USES_TRACKER | Tracker: TrackTrack |
| Experiment: V7-POST-ST SparseTrack | USES_TRACKER | Tracker: SparseTrack |
| Experiment: V7-POST-CTW C-TWiX external | USES_DATASET | Dataset: KITTIMOT val |
| Experiment: V7-POST-CTW C-TWiX external | USES_DATASET | Dataset: DanceTrack |
| Experiment: V7-POST-TT TrackTrack external | USES_DATASET | Dataset: DanceTrack |
| Experiment: V7-POST-PD PD-SORT external | USES_DATASET | Dataset: MOT17 |
| Experiment: V7-E19 KITTI motion rule | USES_DATASET | Dataset: KITTI tracking |
| Experiment: V7-POST-VD VisDrone val-7 | USES_DATASET | Split: VisDrone2019-MOT-val |
| Experiment: V7-POST-CTW C-TWiX external | PRODUCES | Result: V7 recent externals |
| Experiment: V7-POST-TT TrackTrack external | PRODUCES | Result: V7 recent externals |
| Experiment: V7-POST-PD PD-SORT external | PRODUCES | Result: V7 main results |
| Experiment: V7-E19 KITTI motion rule | PRODUCES | Result: V7 KITTI six cells |
| Failure: FX-24 V7f KITTI YOLOv8n regression | FOUND_IN | Result: V7 KITTI six cells |
| Failure: FX-25 V7f recent externals | FOUND_IN | Result: V7 recent externals |
| Experiment: SCI-E1 SCI plus V7f | EVALUATES | Version: C1 SCI plus V7f |
| Failure: FX-26 SCI plus V7f | FOUND_IN | Experiment: SCI-E1 SCI plus V7f |
| Experiment: G2 oracle gate | EVALUATES | Version: G2 compute adaptation |
| Failure: FX-27 G2 gate | FOUND_IN | Experiment: G2 oracle gate |
| Experiment: P1-BASE baseline systems | EVALUATES | Version: AC-MOT v3 controller |
| Experiment: P1-A Phase A searches | EVALUATES | Version: AC-MOT v3 controller |
| Experiment: P1-B V3 joint search | EVALUATES | Version: AC-MOT v3 controller |
| Experiment: P1-SHUF shuffled control | EVALUATES | Version: AC-MOT v3 controller |
| Experiment: P1-STATIC first val read | EVALUATES | Version: AC-MOT v3 controller |
| Experiment: P1-V3 second val read | EVALUATES | Version: AC-MOT v3 controller |
| Experiment: P1-UAVDT transfer | EVALUATES | Version: AC-MOT v3 controller |
| Experiment: P1-RT runtime | EVALUATES | Version: AC-MOT v3 controller |
| Experiment: P1-LEGACY U2MOT SparseTrack | EVALUATES | Version: Legacy AC-MOT |
| Experiment: P1-V3 second val read | PRODUCES | Result: Paper 1 VisDrone second read |
| Experiment: P1-BASE baseline systems | PRODUCES | Result: Paper 1 VisDrone second read |
| Experiment: P1-UAVDT transfer | PRODUCES | Result: Paper 1 UAVDT transfer |
| Experiment: P1-V3 second val read | USES_MODULE | Module: run_v3_second_val_read.py |
| Experiment: P1-V3 second val read | USES_MODULE | Module: tools/v6/eval_official.py |
| Experiment: P1-V3 second val read | USES_MODULE | Module: adapters/trackers/oatrack.py |
| Experiment: P1-V3 second val read | RECORDED_AT | Commit: 0af0066 |
| Experiment: P1-V3 second val read | USES_DATASET | Split: VisDrone2019-MOT-val |
| Experiment: P1-B V3 joint search | USES_DATASET | Split: VisDrone2019-MOT-train calibration-8 |
| Experiment: P1-UAVDT transfer | USES_DATASET | Split: UAVDT test |
| Experiment: P1-V3 second val read | USES_CHECKPOINT | Checkpoint: YOLO11m VisDrone dronefreak |
| Failure: FX-28 Paper 1 Phase A null | FOUND_IN | Experiment: P1-A Phase A searches |
| Failure: FX-29 Paper 1 shuffled control | FOUND_IN | Experiment: P1-SHUF shuffled control |
| Claim: P2 single-stage HOTA plus 0.9 percent | SUPPORTED_BY | Experiment: V7-POST-PD PD-SORT external |
| Paper: Paper 2 SCL JRTIP | MAKES_CLAIM | Claim: P2 single-stage HOTA plus 0.9 percent |
| Claim: P2 halved scores recover 97 percent | SUPPORTED_BY | Experiment: V7-STRESS-L score shifts |
| Paper: Paper 2 SCL JRTIP | MAKES_CLAIM | Claim: P2 halved scores recover 97 percent |
| Claim: P2 RT-DETR MOTA plus 12.6 and 16.3 percent | SUPPORTED_BY | Experiment: V7-E19 KITTI motion rule |
| Paper: Paper 2 SCL JRTIP | MAKES_CLAIM | Claim: P2 RT-DETR MOTA plus 12.6 and 16.3 percent |
| Claim: P2 external validation | SUPPORTED_BY | Experiment: V7-POST-CTW C-TWiX external |
| Paper: Paper 2 SCL JRTIP | MAKES_CLAIM | Claim: P2 external validation |
| Claim: P2 real-time | SUPPORTED_BY | Experiment: V7-POST-RT runtime |
| Paper: Paper 2 SCL JRTIP | MAKES_CLAIM | Claim: P2 real-time |
| Claim: P1 ByteTrack HOTA plus 7.1 percent | SUPPORTED_BY | Experiment: P1-V3 second val read |
| Paper: Paper 1 AC-MOT JAIS | MAKES_CLAIM | Claim: P1 ByteTrack HOTA plus 7.1 percent |
| Claim: P1 UAVDT OATrack MOTA plus 16.7 percent | SUPPORTED_BY | Experiment: P1-UAVDT transfer |
| Paper: Paper 1 AC-MOT JAIS | MAKES_CLAIM | Claim: P1 UAVDT OATrack MOTA plus 16.7 percent |
| Claim: P1 4.2 ms on T4 | SUPPORTED_BY | Experiment: P1-RT runtime |
| Paper: Paper 1 AC-MOT JAIS | MAKES_CLAIM | Claim: P1 4.2 ms on T4 |
| Paper: Paper 2 SCL JRTIP | HAS_FIGURE | Figure: Paper 2 fig3 forest |
| Paper: Paper 2 SCL JRTIP | HAS_FIGURE | Figure: Paper 2 fig4 fig5 |
| Conflict: CF-02 BoT-SORT 0020 caption | AFFECTS | Manuscript: Paper2_V11 |
| Conflict: CF-03 KITTI cells omitted | AFFECTS | Manuscript: Paper2_V11 |
| Conflict: CF-04 recent externals omitted | AFFECTS | Manuscript: Paper2_V11 |
| Conflict: CF-07 Paper 1 second val read | AFFECTS | Manuscript: Paper1_V12_JAIS |
| Conflict: CF-05 aerial val README | AFFECTS | Experiment: V7-POST-VD VisDrone val-7 |
| Review: Paper2_V11 internal audit | RECORDS | Conflict: CF-04 recent externals omitted |
| Decision: D-030 paper registry and venues | GOVERNS | Paper: Paper 1 AC-MOT JAIS |
| Decision: D-031 Paper 2 audit fixes | GOVERNS | Manuscript: Paper2_V11 |
| Decision: D-031 Paper 2 audit fixes | SUPPORTED_BY | Review: Paper2_V11 internal audit |
| Policy: owner-only delete | DECIDED_BY | Decision: D-033 owner-only delete |
| Decision: D-034 signed approval fail closed | REFINES | Decision: D-033 owner-only delete |
| Policy: owner-only delete | DECIDED_BY | Decision: D-034 signed approval fail closed |
| Policy: completed versions immutable | DECIDED_BY | Decision: D-035 completed versions immutable |
| Policy: completed versions immutable | USES | Registry: VERSION_REGISTRY |
| Policy: completed versions immutable | EXTENDS | Policy: owner-only delete |
| Registry: VERSION_REGISTRY | RECORDS | Paper: Paper 1 AC-MOT JAIS |
| Registry: VERSION_REGISTRY | RECORDS | Paper: Paper 2 SCL JRTIP |
| Registry: VERSION_REGISTRY | RECORDS | Version: V7 |

## Code links
| Entity | Relation | Code file |
|---|---|---|
| Component: Online Self-Calibration | IMPLEMENTED_IN | online_calibration.py |
| Component: Otsu-3 Candidate Bands | IMPLEMENTED_IN | online_calibration.py |
| Component: Otsu-3 Candidate Bands | IMPLEMENTED_IN | universal_policy_pipeline.py |
| Component: Universal AC Controller | IMPLEMENTED_IN | universal_policy_pipeline.py |
| Component: Z-logit Leader Gate | IMPLEMENTED_IN | universal_policy_pipeline.py |
| Component: ECDF Normaliser | IMPLEMENTED_IN | adapters/detectors/online_normalizer.py |
| Component: Scene State Analyzer | IMPLEMENTED_IN | scene_state.py |
| Component: Scene State Analyzer | IMPLEMENTED_IN | tools/visual_cues.py |
| Component: Compute Latency Constraint | IMPLEMENTED_IN | universal_acmot.py |
| Component: Detector Adapter | IMPLEMENTED_IN | adapters/detectors/base.py |
| Component: Tracker Adapter | IMPLEMENTED_IN | adapters/trackers/base.py |
| Component: Legacy SCI | IMPLEMENTED_IN | core.py |
| Version: V5 learned controller | IMPLEMENTED_IN | v5_controller.py |
| Version: V5 learned controller | IMPLEMENTED_IN | tools/v5_train.py |
| Experiment: E32 S1 headroom | IMPLEMENTED_IN | tools/v5_s1_headroom.py |
| Experiment: E33 S2 cue utility | IMPLEMENTED_IN | tools/v5_s2_cues.py |
| Experiment: E34-E35 S3 learned controller | IMPLEMENTED_IN | tools/v5_s3_nested.py |
| Experiment: E36 V5-TF dev validation | IMPLEMENTED_IN | tools/v5tf_dev.py |
| Experiment: E39 constant audit | IMPLEMENTED_IN | tools/v5tf_dev.py |
| Rule: F5 scene-adaptive resolution R-res | IMPLEMENTED_IN | universal_policy_pipeline.py |
| Rule: F5R random resolution control | IMPLEMENTED_IN | universal_policy_pipeline.py |
| Experiment: E38 T4 fidelity gate | IMPLEMENTED_IN | tools/fidelity_gate.py |
| Experiment: E31 V4 test-dev held-out | IMPLEMENTED_IN | tools/heldout_run.py |
| Constraint: C9 T4 official timing | IMPLEMENTED_IN | tools/t4_benchmark.py |
| Detector: YOLOv8n | IMPLEMENTED_IN | adapters/detectors/yolov8.py |
| Detector: RT-DETR-L | IMPLEMENTED_IN | adapters/detectors/rtdetr.py |
| Detector: Faster R-CNN ResNet50-FPN v2 | IMPLEMENTED_IN | adapters/detectors/fasterrcnn.py |
| Tracker: ByteTrack | IMPLEMENTED_IN | adapters/trackers/bytetrack.py |
| Tracker: BoT-SORT | IMPLEMENTED_IN | adapters/trackers/botsort.py |
| Component: Duplicate Suppression | IMPLEMENTED_IN | online_calibration.py |
| Component: Nested Otsu Bands | IMPLEMENTED_IN | online_calibration.py |
| Component: Nested Otsu Bands | IMPLEMENTED_IN | universal_policy_pipeline.py |
| Experiment: E43 V6 development X1-X5 | IMPLEMENTED_IN | tools/v6/dev.py |
| Experiment: E54 SparseTrack external transfer | IMPLEMENTED_IN | tools/v6/external/sparsetrack_v6.py |
| Method: SCL self-calibrating control layer | IMPLEMENTED_IN | acmot_v7.py |
| Version: V7 | IMPLEMENTED_IN | acmot_v7.py |
| Method: AC-MOT operating-point controller | IMPLEMENTED_IN | acmot_sci.py |
| Module: acmot_v7.py V7Layer | IMPLEMENTED_IN | acmot_v7.py |
| Module: acmot_sci.py SceneLayer | IMPLEMENTED_IN | acmot_sci.py |
| Module: acmot_sci_v7.py LevelSource | IMPLEMENTED_IN | acmot_sci_v7.py |
| Module: acmot_g2.py G2Pipeline | IMPLEMENTED_IN | acmot_g2.py |
| Module: online_calibration.py | IMPLEMENTED_IN | online_calibration.py |
| Module: tools/v7/dev.py | IMPLEMENTED_IN | tools/v7/dev.py |
| Module: tools/v7/bootstrap.py | IMPLEMENTED_IN | tools/v7/bootstrap.py |
| Module: tools/v7/kitti/kitti_eval.py | IMPLEMENTED_IN | tools/v7/kitti/kitti_eval.py |
| Module: tools/v7/mot17_eval_v7.py | IMPLEMENTED_IN | tools/v7/mot17_eval_v7.py |
| Module: tools/v7/benchmark.py | IMPLEMENTED_IN | tools/v7/benchmark.py |
| Module: tools/v6/eval_official.py | IMPLEMENTED_IN | tools/v6/eval_official.py |
| Module: adapters/trackers/oatrack.py | IMPLEMENTED_IN | adapters/trackers/oatrack.py |
| Module: run_v3_joint_search.py | IMPLEMENTED_IN | research/acmot_paper_v2/controller_search/run_v3_joint_search.py |
| Module: run_v3_second_val_read.py | IMPLEMENTED_IN | research/acmot_paper_v2/run_v3_second_val_read.py |
| Policy: owner-only delete | IMPLEMENTED_IN | tools/claude_tool_guard.py |
| Policy: owner-only delete | IMPLEMENTED_IN | tools/research_guard.py |
| Policy: completed versions immutable | IMPLEMENTED_IN | tools/version_registry.py |
| Registry: VERSION_REGISTRY | IMPLEMENTED_IN | tools/version_registry.py |
| Decision: D-038 fast workflow | IMPLEMENTED_IN | tools/sync_research_memory.py |
