# cpg-global-entry-strategy

DSO 576 Project: Decision-support analytics for international market prioritization and category growth using Passport market intelligence.

---

## Module 6: Project data cleaning (branch `[your-branch-name]`)

**Student:** Antonio
**Branch:** `[your-branch-name]`
**Branch URL:** [paste link to your branch]
**Commit ID:** [paste the commit ID you submit]

### Data source and version

| File (place in `data/raw/`) | Passport dataset | Export date (GMT) |
|---|---|---|
| `Market_Sizes.xls` | Market Sizes, Historical (Coffee, RTD Coffee) | 9/20/2026 11:17:37 PM |
| `Retail_channels.xls` | Retail Channels, Historical | 10/1/2026 7:02:34 AM |
| `Pack_type.xls` | Pack Type, Historical | 10/1/2026 7:05:16 AM |
| `Pack_Size.xls` | Pack Size, Historical | 10/1/2026 7:07:44 AM |

Source: Euromonitor International, Passport (accessed through USC Libraries). Coverage: World, 7 regions, 10 countries; Coffee and RTD Coffee; 2015-2025.

The raw files are licensed and are **not** committed to this public repository (`data/` is in `.gitignore`). The instructor can access them through USC Passport using the links in `project-start.md`, or request the exact files from me directly. SHA-256 fingerprints of the files I used are printed in `reports/cleaning_report.md` so you can confirm you have identical copies.

### How to run

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Mac:      source .venv/bin/activate
pip install -r requirements.txt
python src/clean_passport.py
```

Or open `notebooks/cleaning_walkthrough.ipynb` in VS Code, choose the `.venv` kernel, then **Restart** and **Run All**.

### Expected output files

| File | Contents | Committed? |
|---|---|---|
| `output/clean/market_sizes_clean.csv` | 792 rows, one per geography x category x data type x year | No (licensed data) |
| `output/clean/retail_channels_clean.csv` | 9,108 rows, channel share % | No |
| `output/clean/pack_type_clean.csv` | 5,830 rows | No |
| `output/clean/pack_size_clean.csv` | 73,469 rows | No |
| `output/clean/channel_volume.csv` | 9,108 rows, channel share x market volume | No |
| `output/clean/market_growth_2020_2025.csv` | 72 series with CAGR | No |
| `output/sample_50_real.csv` | 50 real cleaned rows incl. difficult cases | No |
| `sample/synthetic_sample_50.csv` | Same 50 rows with **random values** (clearly labeled) | Yes |
| `reports/cleaning_report.md` | Counts, checks, reconciliation for the 14-item checklist | Yes |
| `reports/output_hashes.txt` | SHA-256 of every output, used to confirm reproducibility | Yes |

### Data sample

The real 50-row sample cannot be shared publicly, so `sample/synthetic_sample_50.csv` keeps the same rows, columns and missing-value pattern but replaces every number with a random value. Rows were chosen as: every difficult case found during cleaning (missing series, unit rescaling, whitespace labels, redundant total rows, unusual growth, g vs ml pack sizes), then random ordinary rows (seed 576) to reach 50.
