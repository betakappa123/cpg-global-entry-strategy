# Coffee Data Cleaning: Individual Evidence and Checklist

**Project:** Yunnan Coffee Overseas-Entry Strategy  
**Individual workspace:** Wendy  
**Prepared:** October 2, 2026  
**Status:** Local implementation and validation evidence; team reconciliation and student review remain outstanding. This is not a completed group submission.

## Vision and analytical purpose

Prepare four Passport datasets to investigate: (1) country-level Coffee and RTD Coffee demand scale and historical volume growth, (2) retail-channel patterns, and (3) packaging formats and sizes. Market Sizes enables a descriptive 2015–2025 volume screen; channel and packaging tables support subsequent country-specific investigation. A broad category's historical performance is not a direct estimate of demand for a Yunnan company's particular product.

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

| Decision | Reason | Implemented result / boundary |
| --- | --- | --- |
| Preserve sources and clean separately | Reproducibility and different row definitions | Four untouched XLS sources and four independent wide CSVs; hashes recorded |
| Exclude verified footer/blank rows only | Notes are not market records | 26 non-data rows excluded; an unexpected footer value stops the run |
| Trim surrounding descriptor whitespace | Fix observed formatting without recategorizing | 65 `PET Jars ` labels become `PET Jars`; internal spaces and other labels remain |
| Convert annual numbers; annual dash becomes missing | Unavailable quantities must not become zero | 6,260 missing observations retained; unknown text stops the run |
| Preserve `Current Constant = -` | It is a volume-row descriptor, not an annual value | No descriptor-to-missing conversion |
| Add `%` to Channels | Source title explicitly states percentage breakdown | Scale stays 0–100; no numeric changes |
| Preserve original unit/currency/category boundaries | Avoid invalid comparisons | No FX, scale, price-basis, mass, or volume conversion |
| Keep hierarchy and total labels | Parents and children can overlap | No automatic summation or total removal |
| Flag, do not erase, unusual changes | A large change need not be an error | Threshold flags retained with source row, year, value, and previous value |
| Add optional analytical views | Make subsequent country/year/size filtering explicit | Geography level and market role in long views; pack size numeric/unit fields preserve original labels |
| Derive country volume screen | Provide a narrow, reproducible starting comparison | Separate categories; 19 valid growth estimates out of 20 country-category rows |
| Defer cross-table merge and shares | Grain and denominators require confirmation | No multiplied rows, inferred hierarchy shares, or manufactured regional percentages |

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

## Individual checklist for team reconciliation

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

## Codex verification response

The implementation was checked against the documented rules. An independent validator reads original workbook cells with xlrd, without importing the cleaning functions to calculate expected values. It verified all 89,165 available annual values, 6,260 missing observations, and 57,459 original descriptor cells against the CSVs. The channel unit is separately checked. Twenty illustrative record checks passed, as did the country-growth calculations and CSV reload checks. A fresh Python process reproduced identical generated data and audit files, and all four original workbook hashes stayed unchanged. Tested versions and the verification command are recorded in `data/quality/independent_validation.json`.

This evidence supports faithful, reproducible cleaning for the stated initial comparisons. It does not validate Passport's missing-value meanings, the causes of flagged changes, company-product fit, or the feasibility of entering a country. Student review and independent team reconciliation have not been performed by Codex.

The 33-cell notebook was also executed from a fresh `coffee-market` kernel, with all 16 code cells completed and outputs saved. A structural scan found no error outputs or Chinese text. A rendered HTML preview was generated for presentation review, but browser policy blocked opening the local file; visual layout has not been verified in a notebook viewer. Open `DataClean.ipynb` in VS Code to review the saved presentation.

## Limitations and next evidence

1. **Missing-value meaning:** dash markers might reflect unavailable, non-applicable, or suppressed observations. Preserve them until source definitions are confirmed; never interpret them as zero demand.
2. **Category fit:** Coffee is broader than a particular Yunnan product. It does not isolate specialty beans, origin preference, café demand, or all possible import opportunities. RTD is a separate business model.
3. **Coverage:** nine foreign countries plus China are observed, not an exhaustive candidate universe. Countries absent from the export cannot be rejected based on this dataset.
4. **Measures:** Coffee retail volume, RTD off-trade volume, channel percentages, packaging counts, and nominal local-currency values have different meanings. Currency, scale, inflation, population, and channel-coverage differences require additional work where relevant.
5. **Hierarchies:** region/world, channel, pack-type, and size totals overlap with components. Definitions and complete non-overlapping coverage must be verified before adding detail or calculating new shares.
6. **Source precision and unusual changes:** rounded values and small baselines affect rates. Flags have been retained and traced; business causes remain unknown. A clean file is not necessarily an error-free source.
7. **Strategy:** competition, import access, logistics, duties, landed cost, margins, consumer preferences, and company capacity/budget are missing. These can reverse a volume-based preference.
8. **Submission:** local real-data samples total forty rows. They are not a substitute for full checks or evidence of redistribution permission. Use licensed/approved review access or a clearly labeled synthetic sample if actual redistribution is prohibited. The group's final PDF/checklist needs reconciliation with teammates' independent results.
