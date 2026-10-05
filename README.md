# cpg-global-entry-strategy

**DSO 576 — Decision-Support Analytics & CPG Global Entry Strategy**  
**Module 6 Deliverable: Project Data Cleaning Assignment**  
**Student Name:** Benjamin (Ru Yi) Cai (`betakappa123`)  
**Team Members:** Wendy S (`WendyS-28`) & Benjamin Cai (`betakappa123`)  

---

## Submission Details & GitHub Branch
- **Which branch did you push to GitHub?** `cleaning-ben`
- **Branch URL:** [https://github.com/betakappa123/cpg-global-entry-strategy/tree/cleaning-ben](https://github.com/betakappa123/cpg-global-entry-strategy/tree/cleaning-ben)
- **Commit ID:** `2aed78ef9d47b90312ded60227b5c897ee439f74` (or current submitted commit on `cleaning-ben`)
- **Gradescope Submission Document:** [`Inspect_and_clean_the_data.pdf`](Inspect_and_clean_the_data.pdf) (also available in [`Inspect_and_clean_the_data.docx`](Inspect_and_clean_the_data.docx) and [`data-cleaning.md`](data-cleaning.md))

---

## Data Source & Version Details
All data was extracted from **Euromonitor International via USC Libraries Passport database subscription** covering 18 geographies (8 regional aggregates + 10 focal countries) across an 11-year annual horizon (2015–2023 historical, 2024–2025 forecast).

1. `DATA/Market Sizes.xls` (Exported GMT 9/20/2026 11:17:37 PM, 72 data rows): Category volume (Tonnes / Million Litres) and retail value RSP (Local currency / USD million).
2. `DATA/Retail channels.xls` (Exported GMT 10/1/2026 7:02:34 AM, 864 data rows): Off-trade volume percentage distribution across 24 retail outlet types.
3. `DATA/Pack type.xls` (Exported GMT 10/1/2026 7:05:16 AM, 530 data rows): Packaging container format unit volume in million units.
4. `DATA/Pack Size.xls` (Exported GMT 10/1/2026 7:07:44 AM, 7,209 data rows): Granular package capacity/size unit volume in million units.

---

## Instructions to Run Code from Original Data
Ensure Python 3.10+ is installed with the required dependencies:
```powershell
pip install pandas numpy xlrd openpyxl nbformat nbclient
```

To execute the entire data inspection, cleaning, and reconciliation pipeline non-interactively:
```powershell
python -m jupyter nbconvert --to notebook --execute DATA/Datacleaner.ipynb --output DATA/Datacleaner.ipynb
```
Alternatively, open `DATA/Datacleaner.ipynb` in VS Code / JupyterLab and execute **Run All Cells**.

---

## Expected Output Files
The pipeline automatically outputs clean, standardized CSV files into `DATA/clean/`:
- `clean_market_channels_merged.csv` (858 KB): Relational merge between Market Sizes Volume and Retail Channels Share %, computing physical channel volume (`Total_Market_Volume * Channel_Share_Pct / 100`).
- `clean_market_sizes_tidy.csv` (23 KB): Reshaped tidy long format of market sizes.
- `clean_market_sizes_wide.csv` (10 KB): Clean wide format with year columns converted to numeric floats.
- `clean_retail_channels_tidy.csv` (611 KB): Reshaped tidy format of retail channel shares with redundant 'Total' removed.
- `clean_retail_channels_wide.csv` (85 KB): Clean wide format of retail channels.
- `clean_pack_type_tidy.csv` (561 KB): Reshaped tidy format of packaging formats with whitespace cleaned.
- `cleaned_sample_50.csv` (5 KB): 50-row representative sample including difficult cases and strategic markets.
