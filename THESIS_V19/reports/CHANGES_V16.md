# Changes from Thesis V15 to Thesis V16

Three equations showed an error mark (¿) in the PDF in place of a symbol. The text of the thesis is unchanged.

| # | Equation | Symbol | V15 PDF | V16 PDF |
|---|---|---|---|---|
| 1 | Eq. (2.3), Section 2.2.3 (page 15) | the star of π*ₜ | ¿ | * |
| 2 | Eq. (2.5), Section 2.2.6 (page 20) | the star of k* | ¿ | * |
| 3 | Eq. (4.2), Section 4.3.2 (page 63) | the "<" of Z₍<t₎ | ¿ | < |

Cause: in the Word file the three symbols were stored correctly, but each one opens a superscript or subscript, and the equation editor of LibreOffice, which draws the PDF, read it as an operator without its first operand. `word/build_docx_v3.py` now marks a "*", "<" or ">" that opens a superscript or subscript as normal text inside the equation, so Word and LibreOffice both show the symbol itself.

## Checks on the V16 build
| Check | Result |
|---|---|
| Error marks (¿) and red error spans in the PDF | 0 (V15: 3) |
| Word tables (38) | identical to V15 |
| Text | identical to V15 |
| Contents and lists | 139 of 139 page numbers correct |
| Figures, tables and algorithms after first mention | 53 of 53 |
| Pages | Word PDF 109 |
