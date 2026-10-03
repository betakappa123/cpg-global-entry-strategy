# cpg-global-entry-strategy
DSO 576 Project: Decision-support analytics for international market prioritization and category growth using Passport market intelligence.

## Cleaning objective

Prepare data for a Yunnan coffee company's overseas-entry strategy: investigate country demand, retail routes, packaging formats, and package sizes. The cleaned data supports initial screening, not a complete feasibility or profitability recommendation. Coffee and RTD Coffee remain separate. China is a domestic benchmark; nine other observed countries are potential research candidates. Region/world aggregates remain contextual.

## Start here

- `plan.md`: original per-column proposals and the October 2, 2026 implementation revision.
- `DataClean.ipynb`: one executed notebook with four dataset sections, short explanations, checks, and a descriptive country screen.
- `clean_coffee.py`: reusable cleaning and audit functions, also callable from the command line.
- `validate_cleaning.py`: independent Excel-cell validation and fresh-process reproducibility check.
- `cleaning-report.md`: individual checklist, decision log, student review of a Codex suggestion, and limitations. The final personal report is submitted as a PDF.
- `requirements-cleaning.txt`: tested dependency versions.

## Source and access

Source: USC Passport / Euromonitor International. Dataset access links are in `project-start.md`; sign in through USC's licensed access. Use the same original exports, worksheet `Statistics Data`, header on Excel row 6:

| Required local file under `data/` | Export timestamp (GMT), as recorded in workbook |
| --- | --- |
| `coffee_market_sizes_2015_2025.xls` | September 20, 2026, 23:17:37 |
| `coffee_retail_channels_2015_2025.xls` | October 1, 2026, 07:02:34 |
| `coffee_pack_type_2015_2025.xls` | October 1, 2026, 07:05:16 |
| `coffee_pack_size_2015_2025.xls` | October 1, 2026, 07:07:44 |

These are export timestamps, not claimed download dates. All cover 2015–2025. Exact SHA-256 fingerprints and source notes are recorded in `data/quality/summary.csv` and each dataset's audit directory. Originals are read only. If a new export changes the schema or record count, the pipeline stops for inspection rather than silently applying old assumptions.

Downloaded and cleaned data remain ignored by Git under the existing `.gitignore`. Cloning this repository alone does not provide the licensed workbooks. Obtain the exports through authorized access or the team's approved data-sharing channel and place them at the paths above.

## Environment and exact commands

Tested with Python 3.14.7. From the repository root, use the existing `.venv`, or create a local environment if it does not exist:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-cleaning.txt
.venv/bin/python clean_coffee.py
.venv/bin/python validate_cleaning.py --reproduce
.venv/bin/python verify_missing_rule.py
```

For Jupyter / VS Code:

```bash
.venv/bin/python -m ipykernel install --user --name coffee-market --display-name "coffee market"
```

Open `DataClean.ipynb`, choose **coffee market**, use **Restart Kernel**, then **Run All**. The first cell checks that the kernel's working directory is the project root. Do not assume the terminal directory determines the notebook directory. The notebook uses the same Python module and writes the same files as the command-line run.

## Outputs

| Output | Purpose |
| --- | --- |
| `data/market_sizes_clean.csv` | 72 wide records; 22 missing annual observations |
| `data/retail_channels_clean.csv` | 864 wide records; 3,384 missing annual observations; explicit `%` unit |
| `data/pack_type_clean.csv` | 530 wide records; 96 missing annual observations |
| `data/pack_size_clean.csv` | 7,209 wide records; 2,758 missing annual observations |
| `data/coffee_country_screening.csv` | 20 country-category rows; separate volume metrics, coverage, and endpoint CAGR |
| `data/quality/summary.csv` | Counts, transformations, source/output fingerprints, and duplicate checks |
| `data/quality/<dataset>/` | Excluded rows, missingness/types, categories, text changes, flags, grouped numeric profiles, and record checks |
| `data/quality/record_checks.csv` | Twenty illustrative original-to-cleaned checks, five per dataset |
| `data/quality/independent_validation.json` | Full-data Excel-cell comparisons and fresh-process rerun outcome |
| `data/samples/*_sample.csv` | Forty actual cleaned records across four inspection samples |

CSV missing numeric observations are empty fields, which pandas normally reads as missing values. Explicit zeros remain zero. `Current Constant = -` is an original descriptor and remains unchanged. Optional `to_long()` views add year/value, geographic level, market role, and parsed package size without changing the saved wide schemas.

## Sample selection and submission preparation

The four local inspection samples contain ten rows each, all cleaned columns, and an added source Excel row reference. Selection is deterministic: start with the five record-check cases, include missing observations, all-missing rows where available, explicit zeros where available, and whitespace corrections, then fill from source order. These are illustrative cases, not a random or representative analytical sample. Every validation check runs on the full data.

These actual samples are **not certified for public redistribution**. Use them only through a permitted review channel. If source data cannot be shared for submission, provide a clearly labeled synthetic sample and explain how the instructor can access the actual results through approved access. Do not force-add ignored downloaded files to Git.

The updated Module 6 instructions require **one PDF per student on Gradescope**, with no group submission or ZIP. Submit scripts, notebook, a sample, dependencies, and README on the student's own branch. The individual report includes all 14 checklist items, a rule/reason/check log, original/expected/actual record checks, and the student's review of a Codex suggestion.

## Individual submission

Student: **Wendy Sun**. Branch: **Wendy**.
Branch URL: https://github.com/betakappa123/cpg-global-entry-strategy/tree/Wendy
Submitted implementation commit: `22722b9b5fc136c01b9d2cebea9dc6f000623aa4`

The implementation commit identifies the submitted code, notebook and sample. A later documentation-only commit records that immutable ID in this README and the report, avoiding a self-referential Git hash. Repository visibility was checked as public on October 3, 2026; the instructor can view the branch without a private-repository invitation.

Gradescope file: `output/pdf/Wendy_Sun_Module_6_Data_Cleaning.pdf`.

### Public sample and actual-data review

`submission/samples/` contains **40 clearly labeled synthetic rows**, ten for each cleaned table, with the same cleaned data columns plus `Sample Type` and `Case`. These are invented examples, not Passport observations, and do not support any reported analytical result. They demonstrate numeric values, missing years, an all-missing record, explicit zero, a large movement, country/region/world labels, retained price-basis dashes, channel totals, and package sizes/totals. Regenerate them with `.venv/bin/python make_submission_samples.py`.

Actual local inspection samples remain under `data/samples/`, and full checks use the real workbooks. Synthetic examples are provided while public redistribution of source-derived rows is unconfirmed; this does not assert that educational use is prohibited. An instructor with authorized USC Passport access can retrieve the listed exports and rerun the scripts. For the exact export version, Wendy can arrange review of the unchanged originals and local results through a course-approved channel; access has not been granted or certified by the script. Workbook fingerprints appear in the report.

### Rebuild the report

After running the cleaning and verification commands, install the optional `requirements-report.txt` and run:

```bash
python build_submission_report.py --commit IMPLEMENTATION_COMMIT
```

This reads local evidence and renders `cleaning-report.md` and the personal PDF. It does not modify original data or submit to Gradescope.


## Interpretation boundaries

Do not combine local currencies, Coffee tonnes with RTD litres, or packaging-unit counts with product mass. Do not sum countries with their regions/world, or all channel/packaging hierarchy levels. Missing entries and absent countries do not mean zero demand. Large-change flags are retained observations, not confirmed errors. Confirm source definitions, the company's product and budget, competition, import access, logistics, costs, margins, and customer fit before recommending entry. The existing dashboard prototype is not a verified data source for these outputs.
