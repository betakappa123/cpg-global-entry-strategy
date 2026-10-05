"""
DSO 576 Module 6: Project Data Cleaning Script
CPG Global Entry Strategy — Coffee Market Prioritization & Expansion
Author: Benjamin (Ru Yi) Cai (GitHub: betakappa123)
Team: Wendy S (WendyS-28) & Benjamin Cai (betakappa123)

This script executes the complete data cleaning, auditing, and reconciliation pipeline
for Euromonitor Passport market intelligence data.
"""

import os
import sys
import xlrd
import numpy as np
import pandas as pd

def get_data_dir():
    # Look for DATA folder relative to script location or current directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "DATA"),
        os.path.join(os.getcwd(), "DATA"),
        os.path.join(base_dir, "..", "DATA")
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return os.path.join(base_dir, "DATA")

def inspect_and_load_source(filepath):
    """
    Non-destructively loads Euromonitor Passport .xls files.
    Dynamically identifies Geography header row and isolates data rows from footer notes.
    """
    wb = xlrd.open_workbook(filepath)
    sh = wb.sheet_by_name(wb.sheet_names()[0])
    
    header_idx = None
    for r in range(min(15, sh.nrows)):
        row_vals = [str(sh.cell_value(r, c)).strip() for c in range(sh.ncols)]
        if "Geography" in row_vals:
            header_idx = r
            break
    if header_idx is None:
        raise ValueError(f"Could not locate 'Geography' header row in {filepath}")
    
    headers = [str(sh.cell_value(header_idx, c)).strip() for c in range(sh.ncols)]
    
    footer_idx = sh.nrows
    for r in range(header_idx + 1, sh.nrows):
        val0 = str(sh.cell_value(r, 0)).strip()
        val1 = str(sh.cell_value(r, 1)).strip() if sh.ncols > 1 else ""
        if val0 == "" and (val1 == "" or "Research" in val1):
            footer_idx = r
            break
        if any(keyword in val0 for keyword in ["Research Sources", "Euromonitor", "Date Exported"]):
            footer_idx = r
            break
            
    data_rows = [[sh.cell_value(r, c) for c in range(sh.ncols)] for r in range(header_idx + 1, footer_idx)]
    df = pd.DataFrame(data_rows, columns=headers)
    return df, header_idx, footer_idx, sh.nrows

def run_cleaning_pipeline():
    data_dir = get_data_dir()
    out_dir = os.path.join(data_dir, "clean")
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(sample_dir, exist_ok=True)
    
    files = {
        "market_sizes": os.path.join(data_dir, "Market Sizes.xls"),
        "retail_channels": os.path.join(data_dir, "Retail channels.xls"),
        "pack_type": os.path.join(data_dir, "Pack type.xls"),
        "pack_size": os.path.join(data_dir, "Pack Size.xls")
    }
    
    print("=" * 70)
    print("DSO 576 MODULE 6: DATA CLEANING PIPELINE")
    print("=" * 70)
    
    # 1. Non-destructive Ingestion
    raw_dfs = {}
    for name, path in files.items():
        if not os.path.exists(path):
            print(f"Warning: {path} not found.")
            continue
        df, h, f, tot = inspect_and_load_source(path)
        raw_dfs[name] = df
        print(f"Loaded {name:<16} | Raw Sheet Rows: {tot:<5} | Data Rows: {len(df):<5} | Cols: {len(df.columns)}")
        
    years = [str(y) for y in range(2015, 2026)]
    
    # 2. Text Standardization & Whitespace Cleaning
    cleaned_dfs = {}
    for name, df in raw_dfs.items():
        clean_df = df.copy()
        text_cols = [c for c in clean_df.columns if c not in years]
        for c in text_cols:
            clean_df[c] = clean_df[c].astype(str).str.strip()
        cleaned_dfs[name] = clean_df
    print("Rule R3: Stripped leading/trailing whitespace (e.g. 'PET Jars ' -> 'PET Jars').")
    
    # 3. Market Sizes Tidy & Reshaping
    vol_mask = cleaned_dfs["market_sizes"]["Data Type"].isin(["Retail Volume", "Off-trade Volume"])
    ms_vol = cleaned_dfs["market_sizes"][vol_mask].copy()
    tidy_vol = ms_vol.melt(
        id_vars=["Geography", "Category", "Data Type", "Unit"],
        value_vars=years,
        var_name="Year",
        value_name="Total_Market_Volume"
    )
    tidy_vol["Year"] = tidy_vol["Year"].astype(int)
    # Rule R4: Preserve NaN for unobserved India RTD Coffee
    tidy_vol["Total_Market_Volume"] = pd.to_numeric(tidy_vol["Total_Market_Volume"].replace("-", np.nan), errors="coerce")
    
    # 4. Retail Channels Tidy (Rule R5: Drop redundant 'Total')
    ret_filtered = cleaned_dfs["retail_channels"][cleaned_dfs["retail_channels"]["Outlet Type"] != "Total"].copy()
    tidy_ret = ret_filtered.melt(
        id_vars=["Geography", "Category", "Outlet Type", "Data Type"],
        value_vars=years,
        var_name="Year",
        value_name="Channel_Share_Pct"
    )
    tidy_ret["Year"] = tidy_ret["Year"].astype(int)
    # Rule R4: Inactive channels treated as 0.0% share
    tidy_ret["Channel_Share_Pct"] = pd.to_numeric(tidy_ret["Channel_Share_Pct"].replace("-", 0.0), errors="coerce")
    
    # 5. Rule R8: Primary Relational Merge & Channel Volume Calculation
    merged_channels = pd.merge(
        tidy_ret,
        tidy_vol[["Geography", "Category", "Year", "Total_Market_Volume", "Unit"]],
        on=["Geography", "Category", "Year"],
        how="inner"
    )
    merged_channels["Channel_Volume"] = merged_channels["Total_Market_Volume"] * (merged_channels["Channel_Share_Pct"] / 100.0)
    print(f"Rule R8: Merged Market Sizes & Channels -> {len(merged_channels)} rows (0 unmatched keys).")
    
    # 6. Generate 50-row representative sample
    sample_rows = []
    # China Coffee & RTD Coffee key channels
    sample_rows.append(merged_channels[(merged_channels['Geography'] == 'China') & (merged_channels['Category'] == 'Coffee') & 
                       (merged_channels['Outlet Type'].isin(['Retail E-Commerce', 'Supermarkets', 'Hypermarkets', 'Convenience Stores'])) &
                       (merged_channels['Year'].isin([2015, 2020, 2025]))])
    sample_rows.append(merged_channels[(merged_channels['Geography'] == 'China') & (merged_channels['Category'] == 'RTD Coffee') & 
                       (merged_channels['Outlet Type'].isin(['Retail E-Commerce', 'Supermarkets', 'Convenience Stores'])) &
                       (merged_channels['Year'].isin([2015, 2020, 2025]))])
    # Japan & Thailand target markets
    sample_rows.append(merged_channels[(merged_channels['Geography'] == 'Japan') & 
                       (merged_channels['Outlet Type'].isin(['Convenience Stores', 'Supermarkets', 'Retail E-Commerce'])) &
                       (merged_channels['Year'].isin([2020, 2025]))])
    sample_rows.append(merged_channels[(merged_channels['Geography'] == 'Thailand') & 
                       (merged_channels['Outlet Type'].isin(['Convenience Stores', 'Supermarkets', 'Retail E-Commerce'])) &
                       (merged_channels['Year'].isin([2020, 2025]))])
    # USA benchmark & India unobserved case
    sample_rows.append(merged_channels[(merged_channels['Geography'] == 'USA') & (merged_channels['Category'] == 'Coffee') &
                       (merged_channels['Outlet Type'].isin(['Supermarkets', 'Retail E-Commerce', 'Discounters'])) &
                       (merged_channels['Year'].isin([2020, 2025]))])
    sample_rows.append(merged_channels[(merged_channels['Geography'] == 'India') & (merged_channels['Year'].isin([2020, 2025])) &
                       (merged_channels['Outlet Type'].isin(['Supermarkets', 'Small Local Grocers', 'Retail E-Commerce']))])
    
    sample_50 = pd.concat(sample_rows).drop_duplicates().head(50).copy()
    sample_50['Channel_Share_Pct'] = sample_50['Channel_Share_Pct'].round(1)
    sample_50['Total_Market_Volume'] = sample_50['Total_Market_Volume'].round(1)
    sample_50['Channel_Volume'] = sample_50['Channel_Volume'].round(1)
    
    # Save sample to both sample/ and DATA/clean/
    sample_csv_1 = os.path.join(sample_dir, "cleaned_sample_50.csv")
    sample_csv_2 = os.path.join(out_dir, "cleaned_sample_50.csv")
    sample_50.to_csv(sample_csv_1, index=False)
    sample_50.to_csv(sample_csv_2, index=False)
    print(f"Exported representative 50-row sample to {sample_csv_1}")
    
    # Export full cleaned files
    merged_channels.to_csv(os.path.join(out_dir, "clean_market_channels_merged.csv"), index=False)
    tidy_vol.to_csv(os.path.join(out_dir, "clean_market_sizes_tidy.csv"), index=False)
    tidy_ret.to_csv(os.path.join(out_dir, "clean_retail_channels_tidy.csv"), index=False)
    print("Exported clean datasets to DATA/clean/.")
    print("=" * 70)
    print("DATA CLEANING PIPELINE COMPLETED SUCCESSFULLY.")
    print("=" * 70)

if __name__ == "__main__":
    run_cleaning_pipeline()
