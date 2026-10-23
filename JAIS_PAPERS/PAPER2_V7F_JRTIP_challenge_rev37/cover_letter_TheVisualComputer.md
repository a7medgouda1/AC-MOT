The Editor-in-Chief
The Visual Computer
Springer

Dear Editor,

We submit the manuscript "Training-Free Self-Calibrating Control Layer for Heterogeneous
Multi-Object Trackers" for consideration as an original research article in The Visual Computer.

Video analysis systems often combine a detector and a multi-object tracker that were developed
separately. When the detector is replaced, retrained, or quantized, its confidence scores change,
while the tracker keeps thresholds that were tuned for another detector. The manuscript presents a
self-calibrating control layer that sits between a frozen detector and a frozen tracker. It needs no
training and no labels, uses no future frames, and reads the detector scores of recent frames with
nested Otsu thresholds to decide whether to keep the tracker's own settings or to take control of the
candidates, their scores, and the tracker's thresholds.

One frozen configuration was tested on seven published trackers, four detection sources, and three
datasets. It raised the HOTA of two single-stage trackers by 0.9%, recovered at least 97% of the
original HOTA of two trackers that failed completely when the detector scores were halved, and raised
the MOTA of two two-stage trackers with a noisy detector by 12.6% and 16.3%, while well-matched
two-stage trackers kept their accuracy. On held-out UAVDT test data, run once after a written
protocol, it raised the MOTA of ByteTrack with RT-DETR-L by 24.7 points. The layer takes 2.95 ms per frame on a CPU.

The manuscript is original, has not been published, and is not under consideration for publication
elsewhere. All authors have approved the submission and declare no competing interests. A related
manuscript by the same authors, on a controller of the detector operating point (AC-MOT), is under
review at the Journal of Aerospace Information Systems (manuscript ID 2026-10-I012138). It addresses a
different part of the pipeline and reports different experiments; following the journal's guidelines,
it is mentioned in the text and not listed among the references.

Thank you for considering our manuscript.

Sincerely,

Ahmed Gouda Ismail (corresponding author)
Computer Engineering and Artificial Intelligence Department
Military Technical College, Cairo, Egypt
a7medgouda1@gmail.com

on behalf of the co-authors Mohamed S. Mohamed (Military Technical College) and
Tarek Ahmed Mahmoud (Egypt University of Informatics)
