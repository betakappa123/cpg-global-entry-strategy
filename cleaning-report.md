# Coffee Data Cleaning: Individual Evidence and Checklist

**Project:** Yunnan Coffee Overseas-Entry Strategy  
**Student:** Wendy Sun  
**Prepared:** October 3, 2026  
**Status:** Individual submission under the updated Module 6 instructions. No group submission or ZIP is required.

**Branch:** Wendy

**Branch URL:** https://github.com/betakappa123/cpg-global-entry-strategy/tree/Wendy

**Submitted implementation commit:** 22722b9b5fc136c01b9d2cebea9dc6f000623aa4

This immutable commit identifies the submitted code, notebook and demonstration sample. A later documentation-only commit adds its ID to the report and README. Instructor repository access must be available; a URL does not grant private-repository access.

## Vision and analytical purpose

Prepare four Passport datasets to investigate: (1) country-level Coffee and RTD Coffee demand scale and historical volume growth, (2) retail-channel patterns, and (3) packaging formats and sizes. Market Sizes enables a descriptive 2015-2025 volume screen; channel and packaging tables support subsequent country-specific investigation. A broad category's historical performance is not a direct estimate of demand for a Yunnan company's particular product.

Preserve all observed countries and contextual regions, treating China as the domestic benchmark. Do not preselect a winning market. The company product, price tier, capacity, budget, cost structure, and export constraints are not yet established. Both Coffee and RTD remain available as separate product paths.

## Result and full-data reconciliation

| Dataset | Imported rows | Non-data rows excluded | Cleaned rows | Available annual values | Missing annual values | Text cells trimmed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Market Sizes | 79 | 7 | 72 | 770 | 22 | 0 |
| Retail Channels | 871 | 7 | 864 | 6,120 | 3,384 | 0 |
| Pack Type | 536 | 6 | 530 | 5,734 | 96 | 9 |
| Pack Size | 7,215 | 6 | 7,209 | 76,541 | 2,758 | 56 |

All 8,675 substantive rows are retained. The 26 excluded rows are verified blank rows or research-source/export/copyright notes; they are preserved in the XLS and recorded with source row numbers in `excluded_rows.csv`. The 95,425 annual observations reconcile to 89,165 available values and 6,260 missing values. No available source number changes. All 6,260 missing observations were annual dash markers; there were no blank annual cells among retained rows in these exports. Explicit zeros remain: 0 in Market Sizes, 278 in Channels, 148 in Pack Type, and 4,439 in Pack Size.

There are zero failed annual-value conversions, zero exact duplicate data rows, and zero composite-key duplicates before or after trimming. Rows repeated by geography or category are legitimate because other key fields differ. No source XLS is edited. Each exported CSV is reloaded and compared exactly with its in-memory result.

Full evidence is in `data/quality/summary.csv`, the four dataset subdirectories, and `independent_validation.json`. Checks run on the complete exports, not only the samples shown in the notebook.

## Cleaning decision log

| Rule | Reason | Check and result |
| --- | --- | --- |
| Preserve sources and clean separately | Reproducibility and different row definitions | Original XLS SHA-256 hashes unchanged; separate CSV paths and row counts verified. |
| Exclude verified footer/blank rows only | Notes are not market records | Excluded rows must have missing non-Geography fields and recognized note/blank labels; 26 rows logged. |
| Trim surrounding descriptor whitespace | Fix observed formatting without recategorizing | Text-change log records 65 corrections; key collisions remain zero; all descriptors independently compared. |
| Convert annual numbers; annual dash becomes missing | Unavailable quantities must not become zero | Per-column before/after missing counts reconcile; conversion failures zero; every numeric/missing cell checked. |
| Preserve `Current Constant = -` | It is a volume-row descriptor, not an annual value | Independent descriptor comparison confirms the source dash is retained on the same records. |
| Add `%` to Channels | Source title explicitly states percentage breakdown | Source title contains % breakdown; validator checks the added unit on every channel record. |
| Preserve original unit/currency/category boundaries | Avoid invalid comparisons | Independent comparison verifies every original unit/category and available number unchanged. |
| Keep hierarchy and total labels | Parents and children can overlap | Composite keys and source labels preserved; no totals calculated across hierarchy levels. |
| Flag, do not erase, unusual changes | A large change need not be an error | Complete flag lists saved; all flagged cells included in source comparisons; zero negative/non-finite values. |
| Add optional analytical views | Make subsequent country/year/size filtering explicit | Long row count equals wide rows times 11; long keys unique; all non-total sizes parse as positive g/ml. |
| Derive country volume screen | Provide a narrow, reproducible starting comparison | Independent recalculation matches all 19 computable CAGRs; India RTD remains uncomputable. |
| Defer cross-table merge and shares | Grain and denominators require confirmation | No cross-table analytical joins; each table independently reconciles its source/output row counts. |

**Workflow history:** the first Market Sizes notebook draft preceded `plan.md`. The original four-table proposals were based on source inspection. The October 2 revision in `plan.md` was written before this implementation following the student's request to prepare all datasets for the overseas strategy. That revision moved optional size parsing into a separate analytical view and added the descriptive country screen. This history must not be represented as a plan that preceded the first draft.

## Four row definitions

Every wide row has eleven year observations. The expected unique keys are:

- Market Sizes: Geography + Category + Data Type + Unit + Current Constant.
- Retail Channels: Geography + Category + Outlet Type + Data Type. Added Unit is always `%`.
- Pack Type: Geography + Category + Packaging Class + Pack Type + Data Type + Unit.
- Pack Size: Geography + Category + Packaging Class + Pack Type + Pack Size + Data Type + Unit.

The optional long view adds Year to each key. Its row count is exactly eleven times the wide count; it preserves missing Value rows. Geographic classification uses an explicit mapping of the ten countries, seven named regions, and World in these files; an unknown geography stops for review. Specific sizes parse as positive g or ml quantities; `Total` is explicitly an aggregate with no numeric size. None of the current size labels fail parsing.

## Suspicious observations and their treatment

| Dataset | Relative change >50% | Nonzero after zero | Channel change >10 percentage points | Total flags |
| --- | ---: | ---: | ---: | ---: |
| Market Sizes | 7 | 0 | Not applicable | 7 |
| Retail Channels | Not applicable | Not applicable | 2 | 2 |
| Pack Type | 93 | 7 | Not applicable | 100 |
| Pack Size | 1,515 | 330 | Not applicable | 1,845 |

Flags count row-year observations, not unique records or proven errors. There are no negative/non-finite available observations and no channel share above 100 in these exports. Thresholds are review aids chosen for this implementation, not instructor requirements. The source is rounded, and small positive or rounded-zero baselines can produce unstable percentage changes; do not interpret a flag alone as business growth or a data error.

Examples inspected and retained:

- Australia RTD volume rises from 3.4 to 5.2 million litres in 2019; this exceeds the review threshold, but agrees with the workbook. The business cause is unverified.
- China's RTD supermarket share changes from 36.3% to 19.1% in 2020; small-local-grocer share changes from 33.6% to 46.3%. Both match the source. Do not infer a causal channel shift or reporting change without additional evidence.
- World Coffee Flexible Paper/Plastic packaging rises from 54.6 to 118.4 million units in 2016; the original figures remain. Parent/child and geographic aggregates must not be double-counted.
- Asia Pacific Coffee Total Packaging / 112 g rises from 10.7 to 20.0 million units in 2016; retain the source values and investigate coverage or market explanations before relying on the change.

Every flagged cell is covered by the independent full-source comparison. This verifies faithful transcription, not the source's business accuracy. Source semantics and the causes of unusual movements remain unresolved; no correction is justified by the available evidence.

## Calculation checks

The descriptive screen contains 10 countries for each category: China as benchmark and 9 foreign candidates. It uses Coffee / Retail Volume / Tonnes and RTD Coffee / Off-trade Volume / million litres only. Countries are listed alphabetically, not ranked. Each row includes the number of available years.

`CAGR = ((value_2025 / value_2015) ** (1 / 10) - 1) * 100` only if both endpoints are finite, the baseline is positive, and the endpoint is nonnegative. Coffee has 10 valid estimates and RTD has 9; India's RTD record has zero available years and remains uncomputable. A zero or missing baseline is not assigned zero growth. The independent validator recalculates every available estimate.

Full numeric profiles report rows, valid count, missing count, minimum, quartiles, median, and maximum by year within category/metric/unit/geographic-level groups, retaining outlet, pack type, and size distinctions where applicable. Quantiles exclude missing values; the valid count makes that denominator visible. Missing group keys would stop cleaning; profiling also uses `dropna=False` defensively. No cross-currency or hierarchy totals or pooled averages are used for strategy. If totals are added later, all-missing inputs must stay missing (for example, pandas `sum(min_count=1)`), and only a verified non-overlapping set may be summed.

## Individual 14-item checklist

| Item | Status | Evidence / explanation |
| --- | --- | --- |
| 1. Vision and analysis question | Done | Vision above; separate country volume screen, channel and packaging questions in notebook |
| 2. Define one row | Done | Four composite keys above; zero key duplicates; Year added in long views |
| 3. Preserve source | Done | Original XLS paths/export versions in README; hashes and footer notes in quality outputs |
| 4. Inspect columns/types | Done | `missingness_and_types.csv` for each table; numeric float conversion with zero failures |
| 5. Standardize text | Done | `text_changes.csv` and before/after `categories.csv`; 9 + 56 PET Jars corrections |
| 6. Investigate duplicates | Done | Exact and key checks before/after in summary; no rows removed as duplicates |
| 7. Handle missing data | Done | Per-year before/after evidence; preserve all unavailable values and all-missing rows; precise dash semantics remain a limitation |
| 8. Check suspicious values | Unresolved | Full flags and source comparisons complete; causes/semantic accuracy unverified, so observations retained and investigation remains required |
| 9. Verify merges | Not applicable | No dataset joins are performed. Reshaping within a table and collecting audit results are not analytical joins |
| 10. Reconcile changes | Done | Row/value reconciliation above; all source numbers preserved; no aggregate total changed by cleaning |
| 11. Check calculations | Done | Country growth recalculated independently; 10/10 Coffee and 9/10 RTD endpoints usable; valid/missing group counts recorded |
| 12. Verify individual records | Done | Twenty selected checks in `data/quality/record_checks.csv`, five per table; all match; every source cell also verified |
| 13. Test reproducibility | Done | `python validate_cleaning.py --reproduce` starts a fresh Python process and reproduces byte-identical CSV/audit outputs while preserving XLS hashes |
| 14. Remaining limitations | Done | Limitations below and notebook; documenting them does not resolve them |

## Five record checks per dataset

The full twenty-case log records source Excel row, selection key, year, original value, expected value, actual value, match, and reason. The selected cases are those documented in plan sections A6, B4, C4, and D4. They include:

- Market Sizes: China Coffee volume, Japan JPY-billion sales value, India's two missing RTD measures, and World Coffee aggregate volume.
- Channels: World Coffee total and offline/e-commerce shares, a missing apparel-specialist observation, and the distinct `Total` row.
- Pack Type: Western Europe aggregate, Latin America missing and later available packaging observations, Thailand's whitespace-corrected PET Jars, and Other Packaging.
- Pack Size: World 100 g and RTD 250 ml, China's missing 1000 g observation, North America's `Total` size, and Western Europe's whitespace-corrected PET Jars.

Expected rules preserve reported values and their units; missing stays unknown; whitespace correction preserves category meaning; totals remain explicitly distinguishable from details. Five checks per dataset exceed the assignment's five-record minimum and supplement the full-data comparison.

## How I checked one Codex suggestion

Codex suggested converting annual dash markers to missing numeric values while retaining the affected records rather than filling them with zero or deleting them. I inspected the notebook's before/after missingness table and questioned why every year still had two missing values, what the columns meant, and why keeping the incomplete records was useful. I also asked why dashes remained in Current Constant and learned that descriptor markers and annual observations require different rules.

For Market Sizes, the displayed evidence was 72 records per year = 70 available numeric values + 2 missing values, with zero unexpected conversion failures. The same two India RTD records have unavailable annual observations throughout the period. This count reconciliation, together with the distinction between unknown quantities and confirmed zero sales, supported retaining the records and excluding unavailable growth estimates from calculation. I accepted that decision after the explanation. Source definitions remain a limitation.

This was a review of displayed results and the reasoning behind the suggestion. I did not personally verify every Excel cell or independently establish Passport's business meaning for the dash. Codex performed the separate full-source comparison described below. This distinction preserves an accurate account of my role.

## Automated verification evidence

The implementation was checked against the documented rules. An independent validator reads original workbook cells with xlrd, without importing the cleaning functions to calculate expected values. It verified all 89,165 available annual values, 6,260 missing observations, and 57,459 original descriptor cells against the CSVs. The channel unit is separately checked. Twenty illustrative record checks passed, as did the country-growth calculations and CSV reload checks. A fresh Python process reproduced identical generated data and audit files, and all four original workbook hashes stayed unchanged. Tested versions and the verification command are recorded in `data/quality/independent_validation.json`.

This evidence supports faithful, reproducible cleaning for the stated initial comparisons. It does not validate Passport's missing-value meanings, the causes of flagged changes, company-product fit, or the feasibility of entering a country. Student review is described below from the actual discussion; no manual source-workbook audit by the student is claimed. Team reconciliation is not required by the updated assignment.

The 33-cell notebook was also executed from a fresh `coffee-market` kernel, with all 16 code cells completed and outputs saved. A structural scan found no error outputs or Chinese text. The student reviewed the saved notebook output during the discussion. PDF presentation is checked separately before delivery.

## Limitations and next evidence

1. **Missing-value meaning:** dash markers might reflect unavailable, non-applicable, or suppressed observations. Preserve them until source definitions are confirmed; never interpret them as zero demand.
2. **Category fit:** Coffee is broader than a particular Yunnan product. It does not isolate specialty beans, origin preference, café demand, or all possible import opportunities. RTD is a separate business model.
3. **Coverage:** nine foreign countries plus China are observed, not an exhaustive candidate universe. Countries absent from the export cannot be rejected based on this dataset.
4. **Measures:** Coffee retail volume, RTD off-trade volume, channel percentages, packaging counts, and nominal local-currency values have different meanings. Currency, scale, inflation, population, and channel-coverage differences require additional work where relevant.
5. **Hierarchies:** region/world, channel, pack-type, and size totals overlap with components. Definitions and complete non-overlapping coverage must be verified before adding detail or calculating new shares.
6. **Source precision and unusual changes:** rounded values and small baselines affect rates. Flags have been retained and traced; business causes remain unknown. A clean file is not necessarily an error-free source.
7. **Strategy:** competition, import access, logistics, duties, landed cost, margins, consumer preferences, and company capacity/budget are missing. These can reverse a volume-based preference.
8. **Submission:** local real-data samples total forty rows. They are not a substitute for full checks or evidence of redistribution permission. Use licensed/approved review access or a clearly labeled synthetic sample if actual redistribution is prohibited. The updated assignment requires this personal PDF on Gradescope and the accompanying materials on the individual branch.


## Additional source-based check of the Codex suggestion



### Suggestion
Convert annual dash markers to missing numeric observations, retain their rows,
and do not fill zero. Keep the descriptor dash in Current Constant separate.

### Expected results specified before comparison
The two India / RTD Coffee records (Off-trade Volume and Off-trade Value RSP)
should both remain. If all eleven source annual cells in each record are dashes,
the cleaned output should have 22 missing observations, no imputed zeros, and no
dropped record. A missing baseline must not produce a fabricated growth estimate.

### Test and actual results
The script reads original XLS cells using xlrd and cleaned CSV cells using csv.
Two matching source records found: PASS.
All 22 original annual observations are literal dashes: PASS.
Both records remain in the CSV: PASS.
All 22 annual CSV fields are missing, with no zero imputation: PASS.
Current Constant remains a literal dash on the volume row: PASS.
India RTD country screen has zero available years and missing CAGR: PASS.

### Decision and limits
Accept this conservative rule: the source provides no numeric basis for zero-fill.
Unknown observations stay missing. These checks demonstrate faithful conversion,
not the exact business meaning of Passport's marker. Student review consisted of
questioning and evaluating the notebook results and this rule's reasoning; this
additional source-based test was executed with Codex assistance. No manual
cell-by-cell Excel audit by the student is claimed.

Reproduce: `.venv/bin/python verify_missing_rule.py`.


## Embedded evidence A: Five original-to-cleaned record checks

Expected rules and selected cases were documented in plan.md before the four-table implementation; the earlier Market Sizes draft is explicitly disclosed in the workflow history. These five cases cover all four datasets and include missing values and whitespace correction. They supplement, rather than replace, the full-data validation.

### Record 1: market_sizes

Category: Coffee; Data Type: Retail Volume; Geography: China.

| Excel row | Year | Original | Expected | Actual | Match |
| --- | --- | --- | --- | --- | --- |
| 15 | 2025 | 61314.5 | 61314.5 | 61314.5 | True |

Reason: Preserve reported number, original unit, and row identity.

### Record 2: market_sizes

Category: RTD Coffee; Data Type: Off-trade Volume; Geography: India.

| Excel row | Year | Original | Expected | Actual | Match |
| --- | --- | --- | --- | --- | --- |
| 21 | 2015 | - | Missing (NaN) | Missing (NaN) | True |

Reason: Preserve unavailable observation, not zero.

### Record 3: retail_channels

Category: Coffee; Geography: World; Outlet Type: Retail Offline.

| Excel row | Year | Original | Expected | Actual | Match |
| --- | --- | --- | --- | --- | --- |
| 8 | 2015 | 97.8 | 97.8 | 97.8 | True |

Reason: Preserve reported number, original unit, and row identity.

### Record 4: pack_type

Category: Coffee; Geography: Thailand; Pack Type: PET Jars.

| Excel row | Year | Original | Expected | Actual | Match |
| --- | --- | --- | --- | --- | --- |
| 297 | 2025 | PET Jars [trailing space]; 24.2 | PET Jars; 24.2 | PET Jars; 24.2 | True |

Reason: Preserve reported number, original unit, and row identity; trim the observed trailing space without changing category meaning.

### Record 5: pack_size

Category: RTD Coffee; Geography: World; Pack Size: 250 ml; Pack Type: Total Packaging.

| Excel row | Year | Original | Expected | Actual | Match |
| --- | --- | --- | --- | --- | --- |
| 6021 | 2025 | 2508.1 | 2508.1 | 2508.1 | True |

Reason: Preserve reported number, original unit, and row identity.

## Embedded evidence B: Missingness and types by year column

All affected year columns are shown. Before types are object; after types are float64. Original blanks exclude the separately logged footer rows. A dash is not an original blank, but becomes a missing numeric observation. Descriptor fields have zero missing/empty keys after trimming.

### market_sizes

| Year | Blanks before | Dashes before | Missing after | Valid after | Failures |
| --- | --- | --- | --- | --- | --- |
| 2015 | 0 | 2 | 2 | 70 | 0 |
| 2016 | 0 | 2 | 2 | 70 | 0 |
| 2017 | 0 | 2 | 2 | 70 | 0 |
| 2018 | 0 | 2 | 2 | 70 | 0 |
| 2019 | 0 | 2 | 2 | 70 | 0 |
| 2020 | 0 | 2 | 2 | 70 | 0 |
| 2021 | 0 | 2 | 2 | 70 | 0 |
| 2022 | 0 | 2 | 2 | 70 | 0 |
| 2023 | 0 | 2 | 2 | 70 | 0 |
| 2024 | 0 | 2 | 2 | 70 | 0 |
| 2025 | 0 | 2 | 2 | 70 | 0 |

### retail_channels

| Year | Blanks before | Dashes before | Missing after | Valid after | Failures |
| --- | --- | --- | --- | --- | --- |
| 2015 | 0 | 315 | 315 | 549 | 0 |
| 2016 | 0 | 314 | 314 | 550 | 0 |
| 2017 | 0 | 310 | 310 | 554 | 0 |
| 2018 | 0 | 314 | 314 | 550 | 0 |
| 2019 | 0 | 310 | 310 | 554 | 0 |
| 2020 | 0 | 309 | 309 | 555 | 0 |
| 2021 | 0 | 308 | 308 | 556 | 0 |
| 2022 | 0 | 301 | 301 | 563 | 0 |
| 2023 | 0 | 304 | 304 | 560 | 0 |
| 2024 | 0 | 298 | 298 | 566 | 0 |
| 2025 | 0 | 301 | 301 | 563 | 0 |

### pack_type

| Year | Blanks before | Dashes before | Missing after | Valid after | Failures |
| --- | --- | --- | --- | --- | --- |
| 2015 | 0 | 14 | 14 | 516 | 0 |
| 2016 | 0 | 13 | 13 | 517 | 0 |
| 2017 | 0 | 11 | 11 | 519 | 0 |
| 2018 | 0 | 8 | 8 | 522 | 0 |
| 2019 | 0 | 8 | 8 | 522 | 0 |
| 2020 | 0 | 8 | 8 | 522 | 0 |
| 2021 | 0 | 5 | 5 | 525 | 0 |
| 2022 | 0 | 5 | 5 | 525 | 0 |
| 2023 | 0 | 8 | 8 | 522 | 0 |
| 2024 | 0 | 8 | 8 | 522 | 0 |
| 2025 | 0 | 8 | 8 | 522 | 0 |

### pack_size

| Year | Blanks before | Dashes before | Missing after | Valid after | Failures |
| --- | --- | --- | --- | --- | --- |
| 2015 | 0 | 411 | 411 | 6798 | 0 |
| 2016 | 0 | 329 | 329 | 6880 | 0 |
| 2017 | 0 | 303 | 303 | 6906 | 0 |
| 2018 | 0 | 264 | 264 | 6945 | 0 |
| 2019 | 0 | 218 | 218 | 6991 | 0 |
| 2020 | 0 | 216 | 216 | 6993 | 0 |
| 2021 | 0 | 197 | 197 | 7012 | 0 |
| 2022 | 0 | 197 | 197 | 7012 | 0 |
| 2023 | 0 | 207 | 207 | 7002 | 0 |
| 2024 | 0 | 207 | 207 | 7002 | 0 |
| 2025 | 0 | 209 | 209 | 7000 | 0 |

## Embedded evidence C: Source identity and reproducibility

**market_sizes:** coffee_market_sizes_2015_2025.xls

Date Exported (GMT): 9/20/2026 11:17:37 PM

SHA-256: 59b9fc4d303afc574511f7dcc0afa05492fad2018710af013871639fcd725610

**retail_channels:** coffee_retail_channels_2015_2025.xls

Date Exported (GMT): 10/1/2026 7:02:34 AM

SHA-256: e89b35df48517582555a4d4b5c536596455fb381fb2afa98300469b54d7c036b

**pack_type:** coffee_pack_type_2015_2025.xls

Date Exported (GMT): 10/1/2026 7:05:16 AM

SHA-256: 3f5eb428ce383f559065f8e46213c849e25f0355dbfd5f81d09043a57eec3248

**pack_size:** coffee_pack_size_2015_2025.xls

Date Exported (GMT): 10/1/2026 7:07:44 AM

SHA-256: cbd41411e801df73685710bc8ba814359bde9a5f75569492392cd99d917807ba

Command: `python validate_cleaning.py --reproduce`. A new Python process reproduced all checked CSV/audit files byte-for-byte and the original workbook hashes were unchanged. The notebook was also restarted and run from top to bottom. Python 3.14.7; pandas 3.0.6; xlrd 2.0.2.

## Sample selection and instructor access

The branch includes 40 explicitly synthetic cleaned-schema examples under submission/samples/, ten per dataset. They were constructed to illustrate valid numbers, missing years, all-missing records, explicit zero, large changes, geography levels, channel totals, package size totals and normalized labels. They include all cleaned columns plus Sample Type and Case. No sample row is a real Passport observation, and no validation claim or market conclusion is derived from these examples. The generator does not read original data.

The actual local sample selection starts with planned record-check cases, adds missing/all-missing/zero/whitespace examples where available, then fills in source order to ten rows per table. All data checks use the full real dataset, not either sample. Real local data remains under data/.

README lists USC Passport access links via project-start.md, filenames, export versions, dependencies, exact run commands and expected outputs. An instructor with authorized source access can rerun the workflow. Wendy can arrange review of the exact originals and local outputs through a course-approved channel; no such access approval is claimed here. Repository visibility and instructor access should be confirmed before submission. The original local evidence files can be regenerated using the documented commands; essential counts and five record checks are embedded in this PDF so they do not depend on local paths.
