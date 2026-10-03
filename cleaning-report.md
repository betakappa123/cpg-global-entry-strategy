# Module 6: Individual Data Cleaning Report

**Student:** Wendy Sun | **Project:** Yunnan Coffee Overseas-Entry Strategy

**Branch:** Wendy

**Branch URL:** https://github.com/betakappa123/cpg-global-entry-strategy/tree/Wendy

**Submitted implementation commit:** 04b6d32e57b1e559e8a1ccda4f7793502bbad252

This is the verified code, notebook and sample revision. Later report-only commits record this ID and refine presentation. The repository was verified public on October 3, 2026.

## Checklist 1-7: Inspect and clean

Vision: support a Yunnan coffee company's overseas-entry strategy. Main question: how do observed countries compare in Coffee retail volume and 2015-2025 volume CAGR? RTD is analyzed separately; channels and packaging support later route-to-market and product-format investigation. China is a domestic benchmark, not a foreign candidate.


| Item | Status | Evidence / explanation |
| --- | --- | --- |
| 1. Vision and question | Done | Compare country volume and 10-year CAGR within Coffee / Tonnes or RTD / million litres. No combined score or entry recommendation. |
| 2. One row / unique key | Done | All tables: Geography + Category + Data Type. Market Sizes adds Unit + Current Constant; Channels adds Outlet Type; Pack Type adds Packaging Class + Pack Type + Unit; Pack Size also adds Pack Size. Year joins the key only in long views. Zero duplicate keys. |
| 3. Preserve source | Done | USC Passport / Euromonitor; original XLS unchanged. Statistics Data sheet, header row 6 (pandas header=5). Market Sizes exported 2026-09-20 23:17:37 GMT; Channels, Pack Type, Pack Size exported 2026-10-01 at 07:02:34, 07:05:16, 07:07:44 GMT. README lists exact filenames/access; hashes checked unchanged. |
| 4. Types and conversions | Done | Year columns: object to float64. Annual dash/blank markers become missing; unexpected text stops processing. Zero conversion failures in all four tables. |
| 5. Standardize text | Done | PET Jars [trailing space] -> PET Jars: 9 cells in Pack Type, 56 in Pack Size. Preserve internal text, categories, units and identifiers; no new key collisions. |
| 6. Duplicates | Done | Exact duplicate rows and composite-key duplicates both zero, before and after cleaning. Repeated country names are valid across categories, metrics, channels and packages. No duplicate removal. |
| 7. Missing data | Done | All 6,260 missing annual observations originate as dashes; zero original annual blanks among data rows. Retain rows and unknown values, including entirely unavailable India RTD records. Per-column counts appear on page 4; do not fill zero or interpolate. |

**Source preservation:** Original-to-cleaned preservation is checked independently with xlrd and csv/pandas; originals remain local and unchanged.

<!--PAGEBREAK-->

## Checklist 8-14: Validate results

| Item | Status | Evidence / explanation |
| --- | --- | --- |
| 8. Suspicious values | Unresolved | Full scans found zero negative/non-finite available observations and zero channel shares above 100%. Flagged row-year observations: Market 7; Channels 2; Pack Type 100; Pack Size 1,845. Values match the source and are retained; causes/source semantics remain unknown. Large changes require review before interpretation. |
| 9. Merges | Not applicable | No cross-table analytical merge. Tables have different grains. Long reshaping preserves all observations and has unique descriptor + Year keys; do not join on country/year alone. |
| 10. Reconcile changes | Done | Table below accounts for all rows: 8,701 imported -> 8,675 data rows + 26 verified blank/footer rows. No substantive row dropped and no available number changed. Do not sum mixed currencies, geographic aggregates or parent/child categories. |
| 11. Calculations | Done | CAGR = ((value_2025 / value_2015) ** (1/10) - 1) * 100, requiring finite endpoints and positive baseline. Coffee: 10/10 country estimates; RTD: 9/10. India RTD has 0 available years and missing CAGR. No averages are used for screening. Group profiles report valid/missing counts; quantiles exclude missing. Missing descriptor keys stop the run. All-missing sums must remain missing; no overlapping hierarchy totals are calculated. |
| 12. Five records | Done | Page 3 shows original, expected and actual values with reasons. Expected rules/cases are documented in plan.md for the four-table implementation. Five examples supplement checks of every source cell; all selected checks match. |
| 13. Reproducibility | Done | Fresh coffee-market kernel: all 16 code cells completed. validate_cleaning.py --reproduce also launches a fresh Python process: outputs match byte-for-byte and source hashes are unchanged. Python 3.14.7; exact dependencies in requirements-cleaning.txt. |
| 14. Limitations | Done | Dash semantics, hierarchy coverage and causes of flags remain unconfirmed. Nine observed foreign countries are not the global candidate universe. Coffee does not isolate Yunnan/specialty demand. Nominal local currencies are not directly comparable; import access, competition, costs, margins and company constraints are still needed before an entry recommendation. |

### Full-data row and value reconciliation

| Dataset | Imported | Excluded | Retained | Numeric values | Missing |
| --- | --- | --- | --- | --- | --- |
| Market Sizes | 79 | 7 | 72 | 770 | 22 |
| Channels | 871 | 7 | 864 | 6120 | 3384 |
| Pack Type | 536 | 6 | 530 | 5734 | 96 |
| Pack Size | 7215 | 6 | 7209 | 76541 | 2758 |

The independent validator checked 89,165 available annual values, 6,260 missing observations and 57,459 original descriptor cells. CSV reloads match in-memory results. Exact/key duplicate counts and conversion failures are zero. Explicit zero counts retained: Market 0; Channels 278; Pack Type 148; Pack Size 4,439. Detailed reproducible logs: data/quality/ and saved notebook outputs.

<!--PAGEBREAK-->

## Cleaning decision log: Rule, reason, check

| Rule | Reason | Check / result |
| --- | --- | --- |
| Preserve original XLS; clean four tables separately | Keep provenance and avoid row multiplication | Unchanged source hashes; independent row/key checks. |
| Remove verified blank/footer rows only | Notes are not observations | Only known footer labels with all other fields missing qualify; 26 exclusions logged. |
| Trim surrounding text whitespace | Normalize formatting without recategorizing | 65 PET Jars corrections; all descriptors compared with trimmed source; no key collisions. |
| Annual dash -> missing; retain zero and rows | Unknown is not zero | Per-year counts reconcile; all 22 India RTD dashes verified directly; no imputation or dropped records. |
| Preserve descriptor dash, categories and units; add channel % | Keep metric meaning; source channel title states % breakdown | Independent descriptor/value comparison; added % checked on every channel row. |
| Retain totals, parent/child labels and geography levels | Avoid double counting | No pooled totals or cross-table joins; long row count = wide count x 11; unknown geographies stop run. |
| Flag >50% quantity changes, >10 percentage-point share changes and movement from zero | Unusual changes need review, not automatic deletion | Source-verified flags retained. These are review thresholds, not confirmed errors. |
| Parse size only in optional long view; restrict growth inputs | Allow meaningful sorting and valid comparisons | Positive g/ml sizes parse; Total has no numeric size. All 19 computable CAGRs independently recalculated. |

## Five record checks using REAL source data

These are selected original records, not synthetic examples. Values in a row retain their original unit. Expected rules and reasons for these record checks are documented in plan.md.

| Source / Excel row / year | Original | Expected | Actual | Reason and match |
| --- | --- | --- | --- | --- |
| Market: China / Coffee / Retail Volume; row 15; 2025 | 61314.5 Tonnes | 61314.5 Tonnes | 61314.5 Tonnes | Preserve reported quantity and unit. Match. |
| Market: India / RTD / Off-trade Volume; row 21; 2015 | - | Missing | Missing | Unknown quantity must not become zero. Match. |
| Channels: World / Coffee / Retail Offline; row 8; 2015 | 97.8 (% in source title) | 97.8; Unit % | 97.8; Unit % | Retain share, document unit. Match. |
| Pack Type: Thailand / Coffee; row 297; 2025 | PET Jars [space]; 24.2 | PET Jars; 24.2 | PET Jars; 24.2 | Trim label; retain million units. Match. |
| Pack Size: World / RTD / Total Packaging; row 6021; 2025 | 250 ml; 2508.1 | 250 ml; 2508.1 | 250 ml; 2508.1 | Preserve size and million-unit count separately. Match. |

<!--PAGEBREAK-->

## Missingness evidence for every affected year column

M = Market Sizes; C = Channels; T = Pack Type; S = Pack Size. Each entry below is original dash count / cleaned missing count. Original annual blank counts and conversion failures are zero in every column. Valid count = retained rows (M 72; C 864; T 530; S 7,209) minus that column's missing count. Missing/empty descriptor keys: zero.

| Year | M: before / after | C: before / after | T: before / after | S: before / after |
| --- | --- | --- | --- | --- |
| 2015 | 2 / 2 | 315 / 315 | 14 / 14 | 411 / 411 |
| 2016 | 2 / 2 | 314 / 314 | 13 / 13 | 329 / 329 |
| 2017 | 2 / 2 | 310 / 310 | 11 / 11 | 303 / 303 |
| 2018 | 2 / 2 | 314 / 314 | 8 / 8 | 264 / 264 |
| 2019 | 2 / 2 | 310 / 310 | 8 / 8 | 218 / 218 |
| 2020 | 2 / 2 | 309 / 309 | 8 / 8 | 216 / 216 |
| 2021 | 2 / 2 | 308 / 308 | 5 / 5 | 197 / 197 |
| 2022 | 2 / 2 | 301 / 301 | 5 / 5 | 197 / 197 |
| 2023 | 2 / 2 | 304 / 304 | 8 / 8 | 207 / 207 |
| 2024 | 2 / 2 | 298 / 298 | 8 / 8 | 207 / 207 |
| 2025 | 2 / 2 | 301 / 301 | 8 / 8 | 209 / 209 |

## How I checked a Codex suggestion

Codex suggested retaining annual missing values instead of filling zero. I reviewed the displayed before/after counts and questioned why each year still had two missing values, why the affected rows were retained, and why Current Constant dashes were treated differently. The reconciliation 72 = 70 valid + 2 missing, together with the difference between unknown and zero, supported accepting the rule. This was a review of results and reasoning, not a claimed manual Excel audit.

A supplemental source-based check with Codex assistance specified the expected result before comparing the cleaned output: preserve both India RTD records and convert their 22 annual dashes to missing. verify_missing_rule.py confirmed 22 literal source dashes, two retained rows, 22 missing outputs, no zero-fill, the retained volume price-basis dash, and missing RTD CAGR. All checks passed. The precise business meaning of the source marker remains unresolved.

## Reproduce and inspect the sample

Run from the repository root after installing requirements-cleaning.txt and placing the authorized original exports at the README paths: python clean_coffee.py; python validate_cleaning.py --reproduce; python verify_missing_rule.py. Alternatively select coffee market, Restart Kernel and Run All in DataClean.ipynb. The four *_clean.csv files, country screen and quality evidence are regenerated. Full checks use REAL data, not a sample.

The prepared submission/samples/ folder contains 40 REAL cleaned rows, ten per table, copied unchanged from data/samples/. All cleaned columns and Source Excel Row are included. Selection starts with planned record-check cases, adds missing/all-missing/zero/whitespace cases where available, then fills in source order. The sample is illustrative, not statistically representative. make_submission_samples.py verifies every field against the full cleaned CSV before copying. These are real-data subsets, not synthetic examples.

README lists source versions, USC Passport access links, run instructions and expected outputs. Original workbooks and full cleaned tables remain local. An instructor with authorized source access can rerun the workflow; Wendy can arrange exact-version review through a course-approved channel. The sample is for inspection only; all reported checks use the full real dataset.