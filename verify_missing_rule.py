"""Targeted source-based check of the proposed annual dash handling rule.

Expected results are specified before reading cleaned output. This is an automated
check performed with Codex assistance, not a claim of a manual Excel inspection.
"""
import csv
from pathlib import Path
import xlrd

ROOT = Path(__file__).resolve().parent

def verify():
    # Pre-specified expectations: preserve both identified records; all 22 annual
    # source dashes become missing, never zero; descriptor dashes remain literal.
    expected_keys = {('India', 'RTD Coffee', 'Off-trade Volume'),
                     ('India', 'RTD Coffee', 'Off-trade Value RSP')}
    book = xlrd.open_workbook(str(ROOT / 'data/coffee_market_sizes_2015_2025.xls'))
    sheet = book.sheet_by_name('Statistics Data')
    headers = sheet.row_values(5)
    years = [str(y) for y in range(2015, 2026)]
    source = []
    for i in range(6, sheet.nrows):
        record = dict(zip(headers, sheet.row_values(i)))
        if tuple(record[k] for k in ['Geography', 'Category', 'Data Type']) in expected_keys:
            source.append(record)
    assert len(source) == 2
    assert all(str(row[year]).strip() == '-' for row in source for year in years)
    with (ROOT / 'data/market_sizes_clean.csv').open(encoding='utf-8-sig', newline='') as stream:
        cleaned = list(csv.DictReader(stream))
    actual = [row for row in cleaned if tuple(row[k] for k in ['Geography', 'Category', 'Data Type']) in expected_keys]
    assert len(actual) == 2
    assert all(row[year] == '' for row in actual for year in years)
    volume = next(row for row in actual if row['Data Type'] == 'Off-trade Volume')
    assert volume['Current Constant'] == '-'
    with (ROOT / 'data/coffee_country_screening.csv').open(encoding='utf-8-sig', newline='') as stream:
        screen = list(csv.DictReader(stream))
    india = next(row for row in screen if row['Geography']=='India' and row['Category']=='RTD Coffee')
    assert india['Available Years']=='0' and india['CAGR 2015-2025 (%)']==''
    text='''# Source-based review of a Codex suggestion

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
'''
    (ROOT/'submission/missing-rule-review.md').write_text(text)
    print(text)

if __name__ == '__main__':
    verify()
