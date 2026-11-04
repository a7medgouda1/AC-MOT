# Changes from Thesis V4 to Thesis V5

| # | Where | Change |
|---|---|---|
| 1 | Word PDF | Display equations are drawn (LibreOffice Math installed in the build environment; the equations were blank in the V3 and V4 PDFs, while the .docx files contained them). |
| 2 | Abstract, keywords | Opening sentence names the thesis topic, real-time target detection and tracking; the survey is mentioned as the basis of the work; keyword "real-time target detection" added. Results unchanged. |
| 3 | Arabic summary | Same two additions in Arabic. |
| 4 | Ch.1 §1.1 | One sentence defining real-time target detection and tracking. |
| 5 | Ch.1 §1.2 | MOTA gains attributed to replacing the fixed operating point by the operating points selected online by AC-MOT; statement on occlusion, illumination, blur and weather limited to what the cited sources support. |
| 6 | Ch.2 §2.2.2 | Feature pyramid networks: "a common" instead of "the standard" response to scale variation. |
| 7 | Ch.2 §2.2.8 | "Run once" statement limited to the UAVDT test split (both controllers) and the predeclared external trackers of SCL. |
| 8 | Ch.2 Table 2.4 | AC-MOT and SCL rows: "--" (all requirements met), explained in the caption. |
| 9 | All chapters | American spelling throughout (labeled, unlabeled, color, favor, equaled). |
| 10 | References | The two submitted manuscripts printed as journal entries, title case, "Submitted (under review)". |
| 11 | Build | `word/build_all.sh` writes the versioned files `Thesis_V<n>.*`; the abstract and Arabic summary of the Word file are rebuilt from the source. |
| 12 | Folder | Only the files used by the build were copied from V4. |
