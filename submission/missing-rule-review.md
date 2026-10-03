# Source-based review of a Codex suggestion

## Suggestion
Convert annual dash markers to missing numeric observations, retain their rows,
and do not fill zero. Keep the descriptor dash in Current Constant separate.

## Expected results specified before comparison
The two India / RTD Coffee records (Off-trade Volume and Off-trade Value RSP)
should both remain. If all eleven source annual cells in each record are dashes,
the cleaned output should have 22 missing observations, no imputed zeros, and no
dropped record. A missing baseline must not produce a fabricated growth estimate.

## Test and actual results
The script reads original XLS cells using xlrd and cleaned CSV cells using csv.
Two matching source records found: PASS.
All 22 original annual observations are literal dashes: PASS.
Both records remain in the CSV: PASS.
All 22 annual CSV fields are missing, with no zero imputation: PASS.
Current Constant remains a literal dash on the volume row: PASS.
India RTD country screen has zero available years and missing CAGR: PASS.

## Decision and limits
Accept this conservative rule: the source provides no numeric basis for zero-fill.
Unknown observations stay missing. These checks demonstrate faithful conversion,
not the exact business meaning of Passport's marker. Student review consisted of
questioning and evaluating the notebook results and this rule's reasoning; this
additional source-based test was executed with Codex assistance. No manual
cell-by-cell Excel audit by the student is claimed.

Reproduce: `.venv/bin/python verify_missing_rule.py`.
