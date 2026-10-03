# cpg-global-entry-strategy

DSO 576 individual data-cleaning deliverable: reproducible cleaning and validation of beverage-market data for international market prioritization.

## Data sources and versions

- **Commercial source data:** Euromonitor International, Passport exports supplied for this project. The exports cover 2015–2025 and were downloaded on the dates recorded in their footer: Market Sizes (2026-09-20); Pack Size, Pack type, and Retail channels (2026-10-01). The exports do not identify a separate Passport release/version number. These licensed source files are retained in `data/`; confirm course/license terms before sharing them outside the course.
- **Foreign exchange rates:** World Bank indicator `PA.NUS.FCRF`, *Official exchange rate (LCU per US$, period average)*, annual 2015–2025 values. The rates used are pinned in `datacleaning.py` for reproducibility; source and retrieval metadata are documented in the notebook.
- **Small data sample:** `data/sample/` contains selected source rows from all four exports. Regenerate the samples with `python create_data_sample.py`.

## Setup and run

From this project directory, install the pinned dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the cleaner:

```powershell
python datacleaning.py
```

Or open `datacleaning.ipynb` and run all cells from top to bottom. It reports the cleaning summary, validates output constraints, checks five source records against independently calculated expected values, and confirms the source files were not modified.

To regenerate the sample CSVs:

```powershell
python create_data_sample.py
```

## Expected output files

`python datacleaning.py` writes:

- `data/cleaned/Market Sizes.csv`
- `data/cleaned/Pack Size.csv`
- `data/cleaned/Pack type.csv`
- `data/cleaned/Retail channels.csv`

`python create_data_sample.py` writes:

- `data/sample/Market Sizes.csv`
- `data/sample/Pack Size.csv`
- `data/sample/Pack type.csv`
- `data/sample/Retail channels.csv`

The individual report is `cleaning_report.pdf`. The notebook is the executable analysis record; it is not a substitute for the PDF report.

## Cleaning and validation

The cleaner reads, but does not modify, the four original exports. It removes recognized export footers and fully unavailable records, converts local-currency market values to USD million using the pinned annual-average exchange rates, and standardizes units without combining unlike physical dimensions. Remaining annual numeric gaps use row-wise cubic-spline interpolation when at least four observed values bracket the missing years; unsupported, invalid, or out-of-bounds spline estimates use linear interpolation. The notebook documents the 14-item checklist, decision log, record checks, and limitations.
