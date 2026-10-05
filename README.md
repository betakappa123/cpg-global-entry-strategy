# cpg-global-entry-strategy

**DSO 576 — Decision-Support Analytics & CPG Global Entry Strategy**  
**Module 6 Deliverable: Project Data Cleaning Assignment**  
**Student Name:** Benjamin (Ru Yi) Cai (`betakappa123`)  
**Team Members:** Wendy S (`WendyS-28`) & Benjamin Cai (`betakappa123`)  

---

## Submission Details & GitHub Branch
- **Branch:** `Ben`
- **Branch URL:** [https://github.com/betakappa123/cpg-global-entry-strategy/tree/Ben](https://github.com/betakappa123/cpg-global-entry-strategy/tree/Ben)
- **Commit ID:** `88820b5` (`88820b5ad3fa8f6823a98e5ab7ce4f4a8f674d49`)
- **Gradescope Deliverable:** Individual 14-item checklist PDF (`Inspect_and_clean_the_data.pdf`) submitted directly to Gradescope.

---

## Data Source & Version Details
All market data was sourced from **Euromonitor International via USC Libraries Passport database subscription** (`Hot Drinks`, `Soft Drinks`, and `Beverage Packaging` modules). The data covers 18 geographies (8 regional aggregates + 10 focal countries) across an 11-year annual horizon (2015–2023 historical, 2024–2025 forecast).

1. `Market Sizes.xls` (Exported GMT 9/20/2026 11:17:37 PM, 72 data rows): Category volume (Tonnes for Coffee, Million Litres for RTD Coffee) and retail value RSP (Local currency / USD million).
2. `Retail channels.xls` (Exported GMT 10/1/2026 7:02:34 AM, 864 data rows): Off-trade volume percentage distribution across 24 retail outlet types.
3. `Pack type.xls` (Exported GMT 10/1/2026 7:05:16 AM, 530 data rows): Packaging container format unit volume in million units.
4. `Pack Size.xls` (Exported GMT 10/1/2026 7:07:44 AM, 7,209 data rows): Granular package capacity/size unit volume in million units.

*(Note: In accordance with course guidelines and Euromonitor redistribution licenses, proprietary raw data files are preserved locally and excluded from public git commits. A representative 50-row cleaned sample is provided in `sample/cleaned_sample_50.csv`.)*

---

## Instructions to Run Code from Original Data
Ensure Python 3.10+ is installed with the required dependencies listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### Option A: Run the standalone cleaning script (.py)
To execute the complete cleaning, text standardization, duplicate investigation, and volume-channel merge:
```powershell
python clean_data.py
```

### Option B: Run the Jupyter Notebook (.ipynb)
To execute the interactive inspection and cleaning walkthrough:
```powershell
python -m jupyter nbconvert --to notebook --execute Datacleaner.ipynb --output Datacleaner.ipynb
```
Or open `Datacleaner.ipynb` in VS Code / JupyterLab and execute **Run All Cells**.

---

## Expected Output Files
Running `clean_data.py` or `Datacleaner.ipynb` generates the following clean, standardized datasets in `DATA/clean/` and `sample/`:
- `sample/cleaned_sample_50.csv`: Representative 50-row sample covering strategic target markets, channel breakdowns, and difficult unobserved cases.
- `DATA/clean/clean_market_channels_merged.csv`: Relational merge between Market Sizes Volume and Retail Channels Share %, computing physical channel volume (`Total_Market_Volume * Channel_Share_Pct / 100`).
- `DATA/clean/clean_market_sizes_tidy.csv`: Reshaped tidy long format of market sizes.
- `DATA/clean/clean_market_sizes_wide.csv`: Clean wide format with year columns converted to numeric floats.
- `DATA/clean/clean_retail_channels_tidy.csv`: Reshaped tidy format of retail channel shares with redundant 'Total' removed.
- `DATA/clean/clean_retail_channels_wide.csv`: Clean wide format of retail channels.
- `DATA/clean/clean_pack_type_tidy.csv`: Reshaped tidy format of packaging formats with whitespace cleaned.
