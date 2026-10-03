# Coffee Project Data Cleaning Plan

**Status:** Implementation authorized on October 2, 2026; domain uncertainties remain documented.
**Prepared:** October 2, 2026.
**Scope:** Four datasets, cleaned separately and reviewed one at a time. No merge is proposed in this first pass.

## Contents

- [A. Market Sizes](#a-market-sizes)
- [B. Retail Channels](#b-retail-channels)
- [C. Pack Type](#c-pack-type)
- [D. Pack Size](#d-pack-size)
- [Shared workflow and review status](#shared-workflow-and-review-status)

All plans and assignment artifacts use English. All source workbooks remain unchanged. The original proposals below are retained as workflow history; the implementation revision below takes precedence over their earlier pending-review labels.

## Implementation revision — October 2, 2026

The student requested implementation for all four datasets and clarified the objective: support an overseas-entry strategy for a Yunnan coffee company. This authorizes the conservative cleaning rules below; it does not establish the meaning of Passport's missing markers or approve a final market recommendation. The first Market Sizes draft predates this plan; this revision precedes the four-dataset implementation.

- Keep four separate wide cleaned CSVs and one notebook with four sections. Put reusable processing in `clean_coffee.py` and independent verification in `validate_cleaning.py`.
- Apply the original column rules, with no imputation, currency conversion, category merging, data-row deletion, or cross-table merge. Add `%` only to the channel table, supported by its title.
- Preserve original labels and years in the CSVs. Provide an optional in-memory long view with explicit integer `Year`, numeric `Value`, `Geography Level`, and `Market Role`. Classify the ten observed countries explicitly; China is a domestic benchmark, the other nine are observed foreign candidates. The seven named regions and World remain contextual aggregates. Unknown geographies stop the run for review.
- Revise D2's deferred size parsing: the optional long view additionally exposes `Size Value`, `Size Unit`, and `Is Size Total`, preserving `Pack Size`. This supports numeric size sorting. `Total` has no numeric size or size unit. Do not convert grams to millilitres or package counts to product volume. Unexpected formats stop for review.
- Export a descriptive country screen using only Coffee / Retail Volume / Tonnes and RTD Coffee / Off-trade Volume / million litres. Keep categories separate. Show 2015 and 2025 values, available-year counts, and 10-year CAGR only when both endpoints exist and the starting value is positive. Keep uncomputable growth missing and explain why. Do not rank countries, combine indicators into a score, or use monetary rows for international value comparisons.
- Record full-data missingness, types, text changes, categories, duplicates, numeric distributions within compatible groups, and every suspicious-value flag. Use >50% adjacent-year relative movement for absolute quantities and >10 percentage points for channel shares, as review thresholds rather than error classifications. Flag nonzero movement from zero separately. Retain flagged numbers unchanged.
- Keep source hashes and original Excel row references in audit outputs. Verify all numeric observations and descriptors against the source, plus five illustrative checks per dataset. Reload exports and rerun in a fresh Python process and notebook kernel.
- Produce local English evidence and an individual checklist draft. Student review of unresolved definitions and individual submission remain separate tasks; no Git commit, push, or submission is part of this implementation.

### Purpose and remaining evidence needs

Market Sizes supports demand scale and historical volume growth; Retail Channels supports route-to-market investigation; Pack Type and Pack Size support format and size investigation. Coffee is a broad category, not a confirmed measure of demand for Yunnan specialty beans. RTD is retained as a separate possible product path. Company product, budget, capacity, price tier, competition, import access, logistics, duties, margins, and consumer preference evidence are needed before a feasible entry strategy can be recommended. Large historical markets or popular packaging alone do not prove profitability.

Treat the decision checkboxes later in this document as the original proposal history. Current execution results and remaining uncertainties belong in `cleaning-report.md` and `data/quality/`.

## A. Market Sizes

**Workflow history:** A first cleaning draft already exists in `DataClean.ipynb`, with an exported CSV. This plan was written afterward to review its decisions against the instructor's workflow. It must not be presented as a plan approved before that first implementation. Existing outputs remain provisional until the student reviews the rules and validation evidence.

### A1. Goal

Prepare the dataset for an analysis and dashboard comparing historical Coffee and RTD Coffee market trends across candidate countries.

**Proposed first question:** How did each country's sales volume change from 2015 to 2025, comparing Coffee and RTD Coffee separately?

Retain sales-value records for later use. Do not compare monetary market sizes across countries until currency and scale are consistent. Historical trends alone cannot establish whether a Yunnan coffee company should expand overseas.

### A2. Source and current findings

- Source: USC Passport / Euromonitor International.
- Original file: `data/coffee_market_sizes_2015_2025.xls`.
- Worksheet: `Statistics Data`; column names appear on Excel row 6.
- Export timestamp recorded in the file: September 20, 2026, 23:17:37 GMT.
- Read-only inspection: 79 imported rows and 16 columns.
- Of these, 72 are market records and 7 are blank or footer rows.
- The records cover 18 geographies, including countries, regional aggregates, and the world total.
- The 11 year columns contain 22 dash markers, all in India's two RTD Coffee records. Their exact source meaning is not yet verified.
- No exact duplicate market rows were found in the current inspection.

One market row represents a unique combination of `Geography`, `Category`, `Data Type`, `Unit`, and `Current Constant`. The year columns contain observations for that combination.

### A3. Proposed rules for each column

| Column | Proposed action | Reason and boundary |
| --- | --- | --- |
| `Geography` | Trim surrounding spaces; keep original labels. | Countries, regions, and World are different levels. Keep them in the cleaned file, but filter to countries for country comparisons. Never add regional or world totals to their component countries. |
| `Category` | Trim surrounding spaces; retain `Coffee` and `RTD Coffee` separately. | These are distinct categories. Do not combine their volumes. |
| `Data Type` | Trim surrounding spaces; preserve all four metric labels. | Sales volume and sales value are different measures. Preserve the distinction between Retail and Off-trade. |
| `Unit` | Trim surrounding spaces; preserve original units. | Tonnes, million litres, local currencies, million, and billion are not interchangeable. No unit or currency conversion in this pass. |
| `Current Constant` | Preserve `Current Prices` and `-`, trimming surrounding spaces only. | In this export, volume rows have `-` instead of a price basis. Do not treat that marker as a missing annual observation. Confirm source definitions before changing it. |
| `2015` through `2025` | Convert available values to numeric types. Represent `-` and genuine empty values as `NaN`. | Keep unknown quantities distinct from zero. Retain affected rows; do not fill, interpolate, or silently discard unexpected text. Report conversion failures and investigate them. |

Keep the current wide format: one column per year. Reshaping into `year` and `value` columns is optional future analysis work, not required for this first cleaning pass.

### A4. Row-level and domain decisions

1. **Preserve the source.** Work on `df_clean = df.copy()`. Never overwrite the original Excel.
2. **Exclude only verified non-data rows.** Inspect rows with missing `Category`; exclude them only when the other fields confirm they are blank or recognized source, export-date, or copyright notes. Preserve their information in the original file and inspection output. Stop if an excluded row contains unexpected data.
3. **Retain missing observations.** Treat annual dash markers as unavailable numeric values pending clarification. Missing does not mean zero sales, so retain India's RTD Coffee rows.
4. **Investigate duplicates.** Count exact duplicates and repeated five-column keys separately. Repeated geographies alone are valid. If new duplicates appear, inspect them before deciding whether to remove any.
5. **Flag suspicious values first.** Check negative and non-finite values. The existing draft also flags adjacent-year changes greater than 50% in absolute magnitude. This threshold is a proposed review aid, not an instructor requirement or a deletion rule. Retain flagged values unless evidence supports a correction.
6. **Do not merge.** This table supports an initial market-trend analysis on its own. Channel and packaging tables have different row definitions and will be reviewed separately.

### A5. Implementation order after review

- [ ] Confirm the analysis question and the decisions in Section A8 with the student.
- [ ] Inspect the complete original table and record its source, shape, dtypes, category values, and missing markers.
- [ ] Revise the proposed rules if inspection or source documentation warrants a change; document the reason before implementing it.
- [ ] Create a working copy and exclude verified footer/blank rows. Display excluded rows and before/after counts.
- [ ] Trim surrounding whitespace. Report changed-cell counts and before/after examples, or state that no correction was needed.
- [ ] Convert annual values and missing markers. Report missingness by year and every failed conversion.
- [ ] Check duplicates and suspicious values. Report retained, corrected, or excluded cases with reasons.
- [ ] Complete the full-data and individual-record checks below.
- [ ] Save a separate CSV, reload it, and compare it with the in-memory result.
- [ ] Restart the kernel and run all cells from the original Excel; compare the output with the reviewed version.

The existing draft should be reconciled with the approved rules, rather than rewritten merely to create more changes.

### A6. Validation and acceptance criteria

All checks must use the full dataset. A preview or safe sample is supplementary evidence only.

| Check | Evidence to produce |
| --- | --- |
| Row reconciliation | For this source version, explain 79 imported rows = 72 retained market records + 7 excluded footer/blank rows. Stop and investigate an unexpected difference. |
| Types and missingness | Report before/after dtypes, blank counts, dash counts, and failed conversions per year. Expect 770 available annual values and 22 missing values if the proposed rules are approved. |
| Categories and keys | Compare unique labels before/after for all five descriptive columns. Preserve meaningful differences; report missing descriptors and composite-key duplicates. |
| Numeric profile | Report count, missing count, minimum, quartiles, median, and maximum by year within compatible category, metric, unit, and geographic-level groups. Inspect negative, non-finite, zero, and large-change cases; do not pool incompatible measures. |
| Numeric preservation | Compare every available annual value with its original value. No unit conversion or imputation is planned, so available numbers must remain unchanged. |
| Calculation behavior | Any later mean or growth calculation must report contributing record counts. Require both endpoints for growth; a missing or zero starting value does not yield a valid percentage growth rate. Do not bridge missing years or treat all-missing groups as zero totals. |
| Merge check | Mark assignment item 9 Not applicable for this pass and explain that no tables were merged. |
| Export and reproducibility | Reload the CSV and compare its values and missingness. Confirm the source file is unchanged and a fresh-session run reproduces the same cleaned CSV. |

Use these five original-to-cleaned record checks, documenting the source row, expected result, actual result, and match:

1. China, Coffee, Retail Volume, 2025: retain the value and Tonnes unit.
2. Japan, Coffee, Retail Value RSP, 2025: retain the value and JPY billion unit.
3. India, RTD Coffee, Off-trade Volume, 2015: annual `-` becomes missing, not zero.
4. India, RTD Coffee, Off-trade Value RSP, 2025: retain the missing observation without filling it.
5. World, Coffee, Retail Volume, 2025: retain the aggregate but do not count it as another country.

**Known draft gaps:** `DataClean.ipynb` already contains several checks, but systematic categorical before/after comparisons and grouped numeric distribution checks need review and additions after approval. Successful execution alone is not evidence that every assignment item is complete.

### A7. Files and saving

| File | Role |
| --- | --- |
| `plan.md` | Proposed decisions for review and subsequent revisions. |
| `data/coffee_market_sizes_2015_2025.xls` | Unchanged source. |
| `DataClean.ipynb` | English explanations, reproducible pandas code, and saved validation outputs. |
| `requirements-cleaning.txt` | Dependencies for reproducing the notebook environment. |
| `data/market_sizes_clean.csv` | Separate cleaned output; current draft remains provisional. |

Use `NaN` for missing annual values in pandas. Save them as empty CSV fields, omit the pandas index, and explain this convention. Do not replace missing numbers with the text `N/A` during calculation.

The current Git ignore rules exclude data files. Do not force-add, commit, or push data as part of this plan. Later submission preparation must address permitted sharing, a safe sample of up to 50 rows including difficult cases, README instructions, the required report and code artifacts, and the student's own branch.

### A8. Decisions for student review

- [ ] The proposed first question is useful for our project.
- [ ] Annual `-` values should remain missing, without zero-filling or deleting the records, while the source meaning is investigated.
- [ ] Original currencies and units should remain unchanged in this pass.
- [ ] Country, regional, and world records should remain available but be separated when analyzing or aggregating.
- [ ] The 50% annual-change threshold is acceptable as a review aid, or should be revised with a stated reason.
- [ ] Keep the year columns, do not merge, and save the result as a separate CSV.

**Approval record:** Student review pending. Writing this plan does not approve its proposed decisions or authorize further cleaning.

**Assistance disclosure:** Codex inspected the source and prepared this plan and the earlier notebook draft. The student must review and direct the decisions. The updated assignment is an individual submission.

---

## B. Retail Channels

### B1. Goal and source

**Proposed question:** How has the distribution of Coffee and RTD Coffee volume across retail channels changed within each country between 2015 and 2025?

- Source: `data/coffee_retail_channels_2015_2025.xls`, worksheet `Statistics Data`, column names on Excel row 6.
- Export timestamp: October 1, 2026, 07:02:34 GMT.
- The title on Excel row 5 explicitly states `Retail Channels | Historical | % breakdown`. Annual values are percentage shares, not tonnes or litres. Preserve the original `Data Type` labels as the basis of the percentage breakdown.
- Inspection found 871 imported rows: 864 data records and 7 footer/blank rows; 24 outlet labels; 3,384 annual dash markers; no blank annual cells, exact duplicates, composite-key duplicates, or negative numeric values before cleaning.

**One row:** `Geography` + `Category` + `Outlet Type` + `Data Type`, with one observation per year column.

### B2. Column rules

| Column | Proposed rule | Reason |
| --- | --- | --- |
| `Geography` | Trim surrounding spaces; preserve labels and separate geographic levels in analysis. | World and regional totals overlap their countries. |
| `Category` | Trim spaces; keep Coffee and RTD Coffee separate. | Their channel shares have different underlying product populations. |
| `Outlet Type` | Trim surrounding spaces; preserve all 24 labels, including `Total` and `Retail Channels`. | A total, a parent channel, and a child channel are not interchangeable or necessarily duplicate records. |
| `Data Type` | Keep `Retail Volume` and `Off-trade Volume`. | These specify the volume basis of the share; they do not make the values absolute volumes. |
| `2015`–`2025` | Convert numbers; map annual `-` to `NaN`, with no zero-fill or interpolation. Preserve the 0–100 scale. | The exact dash meaning remains unresolved. Scaling percentages to 0–1 is unnecessary for this cleaning pass. |
| New `Unit` | Add the constant `%` and document this added field. | The source header explicitly establishes percentage units even though there is no original Unit column. No numeric values change. |

### B3. Domain decisions and validation

- Exclude only the 7 verified footer/blank rows, preserving their provenance in the source and inspection output. Reconcile 871 = 864 + 7.
- Expect 9,504 annual observations: 6,120 numeric and 3,384 missing if the proposed missing-value rule is approved. Verify these counts rather than hard-coding a replacement result.
- Count exact and composite-key duplicates before and after trimming. Missing descriptors or unexpected new key collisions require investigation.
- Compare outlet, category, geography, and data-type labels before/after. Never drop an outlet just because all its annual values are missing.
- Report valid counts, missing counts, min, quartiles, median, and max by year, category, data type, and comparable geographic/channel level. Flag values below 0, above 100, and non-finite values.
- Inspect the relationship between `Retail Channels` and `Total`; keep both until source definitions establish whether they are redundant.
- Do not add every outlet row together. For example, `Grocery Retailers` includes more detailed channel categories. Verify a complete, non-overlapping set before checking whether shares sum to 100.
- Where definitions confirm the relationship and all inputs are present, compare Offline plus E-Commerce with the relevant total. For three independently rounded one-decimal values, an initial absolute tolerance of 0.15 percentage points is reasonable; document or revise it after checking source rounding. Do not fill missing inputs to force equality.
- Proposed change flag: absolute adjacent-year movement greater than 10 **percentage points**, pending student review. This is not the Market Sizes 50% relative-change threshold. Retain flagged records unless an error is supported by evidence.
- Do not average country percentages to manufacture a regional share, or multiply these shares by Market Sizes volumes, without matching definitions and denominators.

### B4. Five record checks and output

Check the following source records in the stated export, retaining their Excel row references:

1. World / Coffee / Retail Channels / 2015: retain the source total of 100.
2. World / Coffee / Retail Offline / 2015: retain 97.8; explain the percentage unit.
3. World / Coffee / Retail E-Commerce / 2015: retain 2.2 without converting it to an absolute volume.
4. World / Coffee / Apparel and Footwear Specialists / 2015, Excel row 21: `-` becomes missing, not zero.
5. World / Coffee / Total / 2015: retain the record even if its values equal another total label; investigate semantics separately.

**Planned output:** `data/retail_channels_clean.csv`, wide format, missing annual values saved as empty fields, no pandas index. Reload and compare all available values and keys; repeat from a fresh kernel.

### B5. Decisions for review

- [ ] Approve the channel-trend question and documented `%` unit field.
- [ ] Keep missing observations and all hierarchy/total labels, without pooling parent and child shares.
- [ ] Review the proposed 10-percentage-point change flag and rounding tolerance.
- [ ] Approve a separate cleaned CSV, without merges.

---

## C. Pack Type

### C1. Goal and source

**Proposed question:** How have packaging-unit volumes for different coffee packaging formats changed within candidate countries?

- Source: `data/coffee_pack_type_2015_2025.xls`, worksheet `Statistics Data`, column names on Excel row 6.
- Export timestamp: October 1, 2026, 07:05:16 GMT.
- Inspection found 536 imported rows: 530 data records and 6 footer/blank rows; 37 original pack-type labels; 96 annual dash markers; no blank annual cells, exact duplicates, composite-key duplicates, or negative numeric values before cleaning.
- All data rows use `Retail/off-trade Unit Volume` and `million units`. These are packaging-unit counts, not coffee weight, beverage litres, monetary sales, or percentage shares.

**One row:** `Geography` + `Category` + `Packaging Class` + `Pack Type` + `Data Type` + `Unit`, with annual observations.

### C2. Column rules

| Column | Proposed rule | Reason |
| --- | --- | --- |
| `Geography` | Trim surrounding spaces; retain original geographic levels. | Avoid double-counting countries and aggregate regions. |
| `Category` | Preserve Coffee and RTD Coffee separately. | Product and packaging comparisons need consistent category boundaries. |
| `Packaging Class` | Preserve `Total`, which is the only current value. | It is a source category, not missing data. Retain it for traceability and future exports. |
| `Pack Type` | Trim surrounding spaces, e.g. `PET Jars ` becomes `PET Jars`. Preserve internal spacing, spelling, and all hierarchy labels. | This fixes observed formatting without inventing category mappings. Do not automatically rewrite `Aluminium /Plastic Pouches`. |
| `Data Type` | Preserve `Retail/off-trade Unit Volume`. | Do not relabel this measure as market weight or revenue. |
| `Unit` | Retain `million units`. | No conversion to individual units or product mass is needed. |
| `2015`–`2025` | Convert numeric values; preserve annual `-` as missing, not zero. | Missing source quantities cannot be inferred solely from neighboring years. |

### C3. Domain decisions and validation

- Reconcile 536 = 530 data records + 6 verified footer/blank rows.
- Expect 5,830 annual observations: 5,734 numeric and 96 missing under the proposed rules.
- Report each changed label, changed-cell counts, and whether trimming introduces a composite-key collision. Stop for review if distinct source rows collide after normalization.
- Check exact duplicates and six-column keys. Repeated countries or pack types across categories are legitimate.
- Report counts, missingness, min, quartiles, median, and max within comparable category, pack type, unit, geographic level, and year groups. Flag negative/non-finite values and adjacent-year changes exceeding 50% as proposed review cases, not automatic errors.
- Keep `Total Packaging`, broad types such as `Flexible Packaging`, and subtypes. Do not sum all levels. Packaging counts are not restricted to 100.
- Calculate format shares only after confirming an appropriate total and mutually exclusive component types. Missing components cannot be replaced with zero to force reconciliation.
- Preserve every available annual number. A popular package format does not by itself prove higher profitability, sustainability, or suitability for the subject company.

### C4. Five record checks and output

1. Western Europe / Coffee / Total Packaging / 2015: preserve 9,598.9 million units as an aggregate.
2. Latin America / Coffee / Flexible Aluminium/Paper / 2015, Excel row 45: `-` becomes missing.
3. The same record / 2025: preserve 0.1; the missing earlier value does not justify deleting the record.
4. Thailand / Coffee / `PET Jars `, Excel row 297: trim the label to `PET Jars`; preserve 12.9 in 2015 and 24.2 in 2025.
5. Thailand / RTD Coffee / Other Packaging / 2025: preserve 10 million units and the meaningful `Other Packaging` category.

**Planned output:** `data/pack_type_clean.csv`, preserving wide format and original numeric scale. Reload, compare with the working table, and rerun from the original Excel in a fresh session.

### C5. Decisions for review

- [ ] Approve the packaging-volume question and observed whitespace correction.
- [ ] Preserve `Total` and the packaging hierarchy; do not assume all types are additive.
- [ ] Keep `million units` and unavailable values unchanged in meaning.
- [ ] Review the proposed 50% change flag and approve a separate CSV without merges.

---

## D. Pack Size

### D1. Goal and source

**Proposed question:** Within a country, coffee category, and packaging type, which package sizes account for the largest observed packaging-unit volumes, and how have those volumes changed?

- Source: `data/coffee_pack_size_2015_2025.xls`, worksheet `Statistics Data`, column names on Excel row 6.
- Export timestamp: October 1, 2026, 07:07:44 GMT.
- Inspection found 7,215 imported rows: 7,209 data records and 6 footer/blank rows; 273 size labels; 2,758 annual dash markers; no blank annual cells, exact duplicates, composite-key duplicates, or negative numeric values before cleaning.
- Observed size labels contain quantities in `g`, quantities in `ml`, and `Total`. Annual values remain `million units` of packaging, not the contents' weight or volume.

**One row:** `Geography` + `Category` + `Packaging Class` + `Pack Type` + `Pack Size` + `Data Type` + `Unit`.

### D2. Column rules

| Column | Proposed rule | Reason |
| --- | --- | --- |
| `Geography` | Trim surrounding spaces; preserve geography levels. | National records and regional/world aggregates must be distinguished. |
| `Category` | Preserve Coffee and RTD Coffee separately. | Grams of packaged coffee and millilitres of RTD beverages are not directly comparable. |
| `Packaging Class` | Retain `Total`. | It is a valid source label. |
| `Pack Type` | Trim surrounding spaces, including `PET Jars `; preserve hierarchy and internal text. | Match the Pack Type cleaning rule without collapsing categories. |
| `Pack Size` | Trim surrounding spaces; keep the original size label, including `Total`. | Size is part of the row identity. `Total` is an aggregate, not an invalid number. |
| `Data Type` | Preserve `Retail/off-trade Unit Volume`. | Annual values count packaging units. |
| `Unit` | Preserve `million units`. | This unit describes the annual observations, not the size printed on each package. |
| `2015`–`2025` | Convert numbers and represent annual `-` as missing. | Retain unknown quantities without filling or interpolation. |

**Optional later enhancement:** Split `Pack Size` into a size number and size unit for numeric sorting. Do not implement that in the first pass. If later approved, preserve the source label; mark `Total` explicitly as an aggregate with no numeric size, and report unparsed labels. Never convert grams to millilitres without justified information.

### D3. Domain decisions and validation

- Reconcile 7,215 = 7,209 data records + 6 verified footer/blank rows.
- Expect 79,299 annual observations: 76,541 numeric and 2,758 missing under the proposed rules.
- Check all seven descriptive fields for missingness and unique labels before/after trimming. Check exact duplicates and seven-column key collisions after normalization.
- Validate size labels against a positive numeric quantity followed by `g` or `ml`, or the exact aggregate label `Total`. Flag unexpected formats without deleting or guessing replacements.
- Profile annual values within comparable category, pack type, size, unit, geography level, and year groups. Report counts, missingness, min, quartiles, median, max, negative/non-finite values, and proposed >50% adjacent-year change flags.
- Keep size totals and specific sizes, but exclude the aggregate from any sum of size detail. Preserve packaging hierarchy levels; do not sum broad pack types and their children.
- Do not assume every country's unobserved size is zero or that the listed sizes form a complete breakdown. Missing rows are different from explicit zero values.
- Do not multiply `Total` by a size, convert package counts into market weight in this pass, or label a size as the largest when missing coverage could change that result without documenting the limitation.

### D4. Five record checks and output

1. World / Coffee / Total Packaging / 100 g, Excel row 14: preserve the size label and the 2025 value of 3,774.2 million units.
2. China / Coffee / Total Packaging / 1000 g, Excel row 41: map the 2015 dash to missing and preserve 0.3 in 2025.
3. North America / Coffee / Total Packaging / Total, Excel row 916: preserve `Total` and the 2025 aggregate of 3,314.5.
4. Western Europe / Coffee / `PET Jars ` / 100 g, Excel row 5468: trim the pack-type label; preserve 0.1 in both 2015 and 2025.
5. World / RTD Coffee / Total Packaging / 250 ml, Excel row 6021: preserve the size unit `ml` and the 2025 packaging count of 2,508.1 million units.

**Planned output:** `data/pack_size_clean.csv`, wide format with original size labels and missing annual values saved as empty fields. Reload and compare all source numbers, then repeat from a fresh session.

### D5. Decisions for review

- [ ] Approve the size-volume question and preservation of original size labels.
- [ ] Keep `Total` as an aggregate rather than a missing or zero size.
- [ ] Defer splitting size labels and converting units to later analysis.
- [ ] Keep unknown values, review the 50% change threshold, and approve a separate CSV without merges.

---

## Shared workflow and review status

For each dataset, follow this sequence independently:

1. Review its proposed goal, column rules, and domain decisions with the student.
2. Preserve the source and inspect all records, including the title and footer.
3. Record agreed rules before implementation; record any later revision and its reason.
4. Make a working copy, remove only verified non-data rows, standardize surrounding whitespace, and convert annual values.
5. After each transformation, report affected rows/cells, missingness, and unexpected cases. Stop and investigate unexpected conversion failures, duplicate-key collisions, or unexplained changes.
6. Run the full-data checks and five source-to-cleaned record checks for that table. Five per table is a proposed workflow choice; it exceeds the assignment's stated five-record requirement.
7. Export that table separately, read it back, and reproduce the same result from a fresh session. Never update the original Excel in place.

Keep code and explanations in English. The existing `DataClean.ipynb` may contain four clearly separated dataset sections with distinct working variables, such as `market_sizes_clean`, `retail_channels_clean`, `pack_type_clean`, and `pack_size_clean`. One shared Python environment is sufficient.

**Cross-table checks are optional future work, not automatic merges.** For example, Pack Size totals may be compared with Pack Type on Geography, Category, Packaging Class, Pack Type, Data Type, Unit, and Year, after confirming matching coverage and unique keys. Any actual join must report unmatched keys, expected cardinality, and before/after row counts. Do not join all four tables on country and year alone.

The student's final checklist should reference evidence from every dataset used. Keep current unresolved source meanings and hierarchy definitions visible. Later submission preparation must follow the assignment's instructions for individual branch work, shareable samples, code, environment, README, and report; this plan does not create or publish those deliverables.

The following table records the historical state before the student's implementation request; it is superseded by the October 2 revision above.

| Dataset | Historical state | Historical review status |
| --- | --- | --- |
| Market Sizes | Existing provisional notebook and CSV; retrospective plan review | Pending |
| Retail Channels | Read-only inspection and proposed plan only | Pending |
| Pack Type | Read-only inspection and proposed plan only | Pending |
| Pack Size | Read-only inspection and proposed plan only | Pending |

**Historical approval boundary:** At the planning-only stage, adding the three plans did not authorize execution. The student's later request to prepare all four datasets for the overseas strategy authorized the implementation revision above.

**Current implementation:** All four tables are cleaned and independently verified. Original sources remain unchanged; no datasets are merged. `DataClean.ipynb` and `cleaning-report.md` contain the execution evidence and unresolved domain questions. The updated assignment requires an individual PDF rather than team reconciliation.

## Submission revision - October 3, 2026

The updated handout supersedes the former group/ZIP submission instructions: Wendy Sun submits one personal PDF on Gradescope and code, notebook, sample, dependencies, and README on branch Wendy. The data-cleaning rules remain unchanged. A synthetic 40-row demonstration sample is provided for public sharing; all validation evidence comes from the real local data. The report describes the student's actual review of missing-value handling, not a claimed manual Excel audit.
