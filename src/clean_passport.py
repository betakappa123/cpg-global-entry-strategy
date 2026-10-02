"""
DSO 576 - Module 6 Project Data Cleaning
Project: cpg-global-entry-strategy (Vision A: Yunnan coffee overseas expansion)

Cleans four Euromonitor Passport exports (Coffee + RTD Coffee, 2015-2025):
    data/raw/Market_Sizes.xls
    data/raw/Retail_channels.xls
    data/raw/Pack_type.xls
    data/raw/Pack_Size.xls

The raw files are NEVER modified. Everything is written to output/, reports/, sample/.

Run from the repository root:
    python src/clean_passport.py
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "output" / "clean"
REPORTS = ROOT / "reports"
SAMPLE = ROOT / "sample"

RAW_FILES = {
    "market_sizes": "Market_Sizes.xls",
    "retail_channels": "Retail_channels.xls",
    "pack_type": "Pack_type.xls",
    "pack_size": "Pack_Size.xls",
}

YEARS = [str(y) for y in range(2015, 2026)]
HEADER_ROW = 5          # Passport puts 5 title/blank rows above the real header
MISSING_MARKER = "-"    # Passport writes "-" when data is not available

# ---------------------------------------------------------------------------
# Lookup tables (cleaning rules written down BEFORE applying them)
# ---------------------------------------------------------------------------
REGIONS = {
    "Asia Pacific", "Australasia", "Eastern Europe", "Latin America",
    "Middle East and Africa", "North America", "Western Europe",
}
COUNTRY_TO_REGION = {
    "China": "Asia Pacific", "India": "Asia Pacific", "Japan": "Asia Pacific",
    "Thailand": "Asia Pacific", "Australia": "Australasia", "Brazil": "Latin America",
    "USA": "North America", "France": "Western Europe", "Germany": "Western Europe",
    "United Kingdom": "Western Europe",
}

# Retail channel tree: child -> parent  (shares are % of total retail volume)
CHANNEL_PARENT = {
    "Retail Channels": None,
    "Retail Offline": "Retail Channels",
    "Retail E-Commerce": "Retail Channels",
    "Grocery Retailers": "Retail Offline",
    "Non-Grocery Retailers": "Retail Offline",
    "Vending": "Retail Offline",
    "Direct Selling": "Retail Offline",
    "Convenience Retailers": "Grocery Retailers",
    "Supermarkets": "Grocery Retailers",
    "Hypermarkets": "Grocery Retailers",
    "Discounters": "Grocery Retailers",
    "Warehouse Clubs": "Grocery Retailers",
    "Food/drink/tobacco specialists": "Grocery Retailers",
    "Small Local Grocers": "Grocery Retailers",
    "Convenience Stores": "Convenience Retailers",
    "Forecourt Retailers": "Convenience Retailers",
    "General Merchandise Stores": "Non-Grocery Retailers",
    "Apparel and Footwear Specialists": "Non-Grocery Retailers",
    "Appliances and Electronics Specialists": "Non-Grocery Retailers",
    "Home Products Specialists": "Non-Grocery Retailers",
    "Health and Beauty Specialists": "Non-Grocery Retailers",
    "Leisure and Personal Goods Specialists": "Non-Grocery Retailers",
    "Other Non-Grocery Retailers": "Non-Grocery Retailers",
}

# Pack type tree: child -> parent. Built from the Euromonitor labels and then
# CONFIRMED with the add-up check in step 4 (children must sum to parent).
PACK_PARENT = {
    "Total Packaging": None,
    "Flexible Packaging": "Total Packaging", "Glass": "Total Packaging",
    "Metal": "Total Packaging", "Paper-based Containers": "Total Packaging",
    "Rigid Plastic": "Total Packaging", "Liquid Cartons": "Total Packaging",
    "Other Packaging": "Total Packaging",
    "Flexible Aluminium/Paper": "Flexible Packaging",
    "Flexible Aluminium/Plastic": "Flexible Packaging",
    "Flexible Paper": "Flexible Packaging", "Flexible Paper/Plastic": "Flexible Packaging",
    "Flexible Plastic": "Flexible Packaging",
    "Stand-Up Pouches": "Flexible Packaging",
    "Aluminium /Plastic Pouches": "Stand-Up Pouches",
    "Plastic Pouches": "Stand-Up Pouches",
    "Glass Jars": "Glass", "Glass Bottles": "Glass",
    "Aluminium Trays": "Metal", "Metal Tins": "Metal", "Other Metal": "Metal",
    "Metal Beverage Cans": "Metal", "Metal Bottles": "Metal",
    "Board Tubs": "Paper-based Containers", "Composite Containers": "Paper-based Containers",
    "Folding Cartons": "Paper-based Containers",
    "Brick Liquid Cartons": "Liquid Cartons", "Gable Top Liquid Cartons": "Liquid Cartons",
    "Shaped Liquid Cartons": "Liquid Cartons",
    "PET Jars": "Rigid Plastic", "Thin Wall Plastic Containers": "Rigid Plastic",
    "Other Plastic Jars": "Rigid Plastic", "HDPE Bottles": "Rigid Plastic",
    "PET Bottles": "Rigid Plastic", "Other Plastic Bottles": "Rigid Plastic",
    "Other Rigid Containers": "Rigid Plastic", "Bag In Box": "Other Packaging",
}

# Report is collected here and written to reports/cleaning_report.md at the end
REPORT: list[str] = []


def log(line: str = "") -> None:
    print(line)
    REPORT.append(line)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def level_of(chain: dict, name: str) -> int:
    level = 0
    while chain.get(name):
        name = chain[name]
        level += 1
    return level


# ---------------------------------------------------------------------------
# Step 1: load a raw file exactly as exported (everything as text)
# ---------------------------------------------------------------------------
def load_raw(key: str) -> tuple[pd.DataFrame, dict]:
    path = RAW / RAW_FILES[key]
    df = pd.read_excel(path, header=HEADER_ROW, dtype=str, engine="xlrd")
    df.columns = [str(c).strip() for c in df.columns]

    # Footer rows (source notes, export date, copyright) have no Category
    footer = df[df["Category"].isna()]
    footer_text = footer["Geography"].dropna().tolist()
    export_date = next((t.split(":", 1)[1].strip() for t in footer_text
                        if t.startswith("Date Exported")), "unknown")

    meta = {
        "file": RAW_FILES[key],
        "sha256": sha256(path),
        "export_date_gmt": export_date,
        "rows_read": len(df),
        "footer_rows": len(footer),
        "footer_text": footer_text,
    }
    data = df[df["Category"].notna()].copy().reset_index(drop=True)
    meta["data_rows"] = len(data)
    return data, meta


# ---------------------------------------------------------------------------
# Step 2: generic cleaning applied to every file
# ---------------------------------------------------------------------------
def standardize_text(df: pd.DataFrame, key: str) -> pd.DataFrame:
    id_cols = [c for c in df.columns if c not in YEARS]
    for col in id_cols:
        before = df[col].copy()
        df[col] = df[col].str.strip()
        changed = before[before != df[col]]
        if len(changed):
            examples = sorted({repr(v) for v in changed})[:3]
            log(f"- `{key}.{col}`: stripped whitespace in {len(changed)} cells, "
                f"e.g. {', '.join(examples)} -> {repr(changed.iloc[0].strip())}")
    return df


def convert_years(df: pd.DataFrame, key: str) -> tuple[pd.DataFrame, dict]:
    stats = {"dash": 0, "blank": 0, "failed": 0, "zeros": 0}
    for y in YEARS:
        raw = df[y]
        stats["dash"] += int((raw == MISSING_MARKER).sum())
        stats["blank"] += int(raw.isna().sum())
        cleaned = raw.replace(MISSING_MARKER, np.nan)
        num = pd.to_numeric(cleaned, errors="coerce")
        failed = cleaned.notna() & num.isna()
        stats["failed"] += int(failed.sum())
        if failed.any():
            log(f"  !! `{key}.{y}` unexpected text values: {cleaned[failed].unique()[:5]}")
        df[y] = num.astype(float)
        stats["zeros"] += int((df[y] == 0).sum())
    return df, stats


def to_long(df: pd.DataFrame) -> pd.DataFrame:
    id_cols = [c for c in df.columns if c not in YEARS]
    long = df.melt(id_vars=id_cols, value_vars=YEARS, var_name="year", value_name="value")
    long["year"] = long["year"].astype(int)
    long["is_missing"] = long["value"].isna()
    return long


def add_geo(df: pd.DataFrame) -> pd.DataFrame:
    df["geo_level"] = np.where(
        df["geography"] == "World", "World",
        np.where(df["geography"].isin(REGIONS), "Region", "Country"))
    df["parent_region"] = df["geography"].map(COUNTRY_TO_REGION)
    unknown = set(df.loc[(df.geo_level == "Country") & df.parent_region.isna(), "geography"])
    if unknown:
        log(f"  !! geographies not in lookup table: {unknown}")
    return df


def snake(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [re.sub(r"[^a-z0-9]+", "_", c.lower()).strip("_") for c in df.columns]
    return df


# ---------------------------------------------------------------------------
# Step 3: file-specific rules
# ---------------------------------------------------------------------------
def clean_market_sizes(df: pd.DataFrame) -> pd.DataFrame:
    df = snake(df).rename(columns={"current_constant": "price_basis"})
    # "-" in Current/Constant means "not applicable" for volume rows
    df["price_basis"] = df["price_basis"].replace(MISSING_MARKER, "Not applicable (volume)")
    df["unit_original"] = df["unit"]
    is_value = df["data_type"].str.contains("Value")
    df["measure"] = np.where(is_value, "value", "volume")
    df["currency"] = np.where(is_value, df["unit"].str.split().str[0], None)
    # Rule: put every value row on the same scale (millions). Only JPY is in billions.
    billions = df["unit"].str.endswith("billion")
    df.loc[billions, "value"] = df.loc[billions, "value"] * 1000
    df.loc[billions, "unit"] = df.loc[billions, "unit"].str.replace("billion", "million")
    log(f"- market_sizes: rescaled {int(billions.sum())} long rows from `billion` to `million` "
        f"(x1000): units {sorted(df.loc[billions, 'unit_original'].unique())}")
    return df


def clean_retail_channels(df: pd.DataFrame) -> pd.DataFrame:
    df = snake(df)
    # "Total" and "Retail Channels" both = 100% for every row. Keep one.
    piv = df.pivot_table(index=["geography", "category", "data_type", "year"],
                         columns="outlet_type", values="value", dropna=False)
    diff = (piv["Total"] - piv["Retail Channels"]).abs()
    log(f"- retail_channels: `Total` vs `Retail Channels` max abs difference = {diff.max():.2f} "
        f"across {diff.notna().sum()} comparisons -> `Total` rows are redundant")
    n_before = len(df)
    df = df[df["outlet_type"] != "Total"].copy()
    log(f"- retail_channels: dropped {n_before - len(df)} long rows where outlet_type == 'Total'")
    df["unit"] = "% share of " + df["data_type"].str.lower()
    df["channel_parent"] = df["outlet_type"].map(CHANNEL_PARENT)
    df["channel_level"] = df["outlet_type"].map(lambda n: level_of(CHANNEL_PARENT, n))
    unknown = set(df["outlet_type"]) - set(CHANNEL_PARENT)
    if unknown:
        log(f"  !! outlet types missing from tree: {unknown}")
    return df


def clean_pack_type(df: pd.DataFrame) -> pd.DataFrame:
    df = snake(df)
    df["pack_parent"] = df["pack_type"].map(PACK_PARENT)
    df["pack_level"] = df["pack_type"].map(lambda n: level_of(PACK_PARENT, n))
    unknown = set(df["pack_type"]) - set(PACK_PARENT)
    if unknown:
        log(f"  !! pack types missing from tree: {unknown}")
    return df


def clean_pack_size(df: pd.DataFrame) -> pd.DataFrame:
    df = snake(df)
    parts = df["pack_size"].str.extract(r"^(\d+(?:\.\d+)?)\s*([a-zA-Z]+)$")
    df["size_value"] = pd.to_numeric(parts[0], errors="coerce")
    df["size_unit"] = parts[1]
    df["is_total_row"] = df["pack_size"].eq("Total")
    bad = df[df["size_value"].isna() & ~df["is_total_row"]]
    log(f"- pack_size: parsed `pack_size` into size_value + size_unit; "
        f"unparsed non-Total labels = {bad['pack_size'].nunique()}")
    units = df[~df.is_total_row].groupby("category")["size_unit"].unique()
    for cat, u in units.items():
        log(f"  - {cat}: size units {sorted(u)}")
    return df


# ---------------------------------------------------------------------------
# Step 4: validation helpers
# ---------------------------------------------------------------------------
def hierarchy_check(df, label_col, parent_map, keys, tol, exclude=frozenset()):
    """Compare each parent with the sum of its (non-excluded) children."""
    rows = []
    wide = df.pivot_table(index=keys, columns=label_col, values="value", dropna=False)
    parents = {p for p in parent_map.values() if p}
    for parent in sorted(parents):
        kids = [c for c, p in parent_map.items() if p == parent and c not in exclude
                and c in wide.columns]
        if parent not in wide.columns or not kids:
            continue
        kid_sum = wide[kids].sum(axis=1, min_count=1)
        d = (kid_sum - wide[parent]).abs()
        rows.append({
            "parent": parent, "children": len(kids),
            "comparisons": int(d.notna().sum()),
            "max_abs_diff": round(float(d.max()), 3) if d.notna().any() else np.nan,
            f"over_tol_{tol}": int((d > tol).sum()),
        })
    return pd.DataFrame(rows)


def md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_(none)_"
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in r) + " |")
    return "\n".join(out)


def write_csv(df: pd.DataFrame, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    df.to_csv(path, index=False, float_format="%.4f", lineterminator="\n")
    return path


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main() -> dict:
    REPORT.clear()
    for d in (OUT, REPORTS, SAMPLE):
        d.mkdir(parents=True, exist_ok=True)

    log("# Cleaning report (auto-generated by src/clean_passport.py)")
    log("")
    log("Do not edit by hand. Re-run the script to regenerate.")
    log("")

    raw, meta, conv, clean = {}, {}, {}, {}

    # ---- Load + source version (checklist item 3)
    log("## Item 3: Source files and version")
    log("")
    log("| file | export date (GMT) | rows read | footer rows | data rows | sha256 (first 12) |")
    log("|---|---|---|---|---|---|")
    for key in RAW_FILES:
        raw[key], meta[key] = load_raw(key)
        m = meta[key]
        log(f"| {m['file']} | {m['export_date_gmt']} | {m['rows_read']} | {m['footer_rows']} | "
            f"{m['data_rows']} | {m['sha256'][:12]} |")
    log("")

    # ---- Text standardization (item 5)
    log("## Item 5: Text standardization")
    log("")
    for key in RAW_FILES:
        raw[key] = standardize_text(raw[key], key)
    log("")

    # ---- Duplicates on the raw wide rows (item 6)
    log("## Item 6: Duplicates (raw wide rows, after whitespace strip)")
    log("")
    log("| file | key columns | exact duplicate rows | repeated keys |")
    log("|---|---|---|---|")
    for key, df in raw.items():
        id_cols = [c for c in df.columns if c not in YEARS]
        log(f"| {key} | {' + '.join(id_cols)} | {int(df.duplicated().sum())} | "
            f"{int(df.duplicated(id_cols).sum())} |")
    log("")

    # ---- Type conversion (item 4) + missing before (item 7)
    log("## Item 4: Type conversion of year columns (text -> float)")
    log("")
    log("| file | '-' cells -> NaN | blank cells | failed conversions | true zeros kept |")
    log("|---|---|---|---|---|")
    for key in RAW_FILES:
        raw[key], conv[key] = convert_years(raw[key], key)
        s = conv[key]
        log(f"| {key} | {s['dash']} | {s['blank']} | {s['failed']} | {s['zeros']} |")
    log("")

    # ---- Reshape + file rules
    log("## Cleaning rules applied")
    log("")
    long = {}
    for key, df in raw.items():
        lf = to_long(df)
        lf.columns = [c if c in ("year", "value", "is_missing") else c for c in lf.columns]
        long[key] = lf
    rows_long_start = {k: len(v) for k, v in long.items()}

    ms = add_geo(clean_market_sizes(long["market_sizes"].copy()))
    rc = add_geo(clean_retail_channels(long["retail_channels"].copy()))
    pt = add_geo(clean_pack_type(long["pack_type"].copy()))
    ps_all = add_geo(clean_pack_size(long["pack_size"].copy()))
    log("")

    # ---- Merge 1: Pack_Size 'Total' rows vs Pack_type (item 9)
    log("## Item 9: Merges")
    log("")
    k = ["geography", "category", "pack_type", "year"]
    tot = ps_all[ps_all.is_total_row][k + ["value"]]
    m1 = pt[k + ["value"]].merge(tot, on=k, how="outer", suffixes=("_pack_type", "_size_total"),
                                 indicator=True, validate="one_to_one")
    both = m1[m1["_merge"] == "both"]
    vdiff = (both["value_pack_type"] - both["value_size_total"]).abs()
    log("**Merge 1** - pack_type <-> pack_size 'Total' rows on geography+category+pack_type+year "
        "(expected 1:1)")
    log(f"- rows: pack_type {len(pt)}, pack_size Total {len(tot)}, merged {len(m1)}")
    log(f"- matched {int((m1._merge == 'both').sum())}, left only "
        f"{int((m1._merge == 'left_only').sum())}, right only "
        f"{int((m1._merge == 'right_only').sum())}")
    log(f"- max abs value difference on matched rows: {vdiff.max():.4f}; "
        f"missing-pattern mismatches: "
        f"{int((both.value_pack_type.isna() != both.value_size_total.isna()).sum())}")
    log("- decision: pack_size 'Total' rows duplicate pack_type exactly, so they are dropped from "
        "the clean pack_size file (pack_type is the source for totals)")
    ps = ps_all[~ps_all.is_total_row].copy()
    log(f"- pack_size rows: {len(ps_all)} -> {len(ps)} (dropped {len(ps_all) - len(ps)} Total rows)")
    log("")

    # ---- Merge 2: channel share x market volume -> channel volume
    vol = ms[ms.measure == "volume"][["geography", "category", "data_type", "year", "value", "unit"]]
    vol = vol.rename(columns={"value": "market_volume", "unit": "market_volume_unit"})
    k2 = ["geography", "category", "data_type", "year"]
    before = len(rc)
    m2 = rc.merge(vol, on=k2, how="left", indicator=True, validate="many_to_one")
    unmatched = m2[m2["_merge"] != "both"]
    log("**Merge 2** - retail_channels (share %) -> market_sizes volume rows on "
        "geography+category+data_type+year (expected many:1)")
    log(f"- market volume rows available: {len(vol)}; distinct keys in retail_channels: "
        f"{rc[k2].drop_duplicates().shape[0]}")
    log(f"- rows before {before}, after {len(m2)}, extra rows created {len(m2) - before}")
    log(f"- unmatched channel rows: {len(unmatched)}")
    m2["channel_volume"] = m2["value"] / 100 * m2["market_volume"]
    m2 = m2.drop(columns="_merge")
    n_cv = int(m2["channel_volume"].notna().sum())
    log(f"- channel_volume computable for {n_cv} of {len(m2)} rows "
        f"(NaN when share or market volume is missing)")
    log("")

    # ---- Hierarchy / add-up checks (item 8)
    log("## Item 8: Suspicious values and internal consistency")
    log("")
    log("**Channel tree: children sum vs parent (tolerance 0.5 percentage points)**")
    log("")
    hc = hierarchy_check(rc, "outlet_type", CHANNEL_PARENT,
                         ["geography", "category", "data_type", "year"], 0.5)
    log(md_table(hc))
    log("")
    log("**Pack type tree: children sum vs parent (tolerance 1.0 million units)**")
    log("")
    hp = hierarchy_check(pt, "pack_type", PACK_PARENT, ["geography", "category", "year"], 1.0)
    log(md_table(hp))
    log("")
    log("Note: `Other Packaging` only lists `Bag In Box` as a child; the remainder is "
        "unclassified 'other' packaging that Passport does not break out, so a gap there is "
        "expected and not treated as an error.")
    log("")
    leaf = ps.groupby(["geography", "category", "pack_type", "year"])["value"].sum(min_count=1)
    tot_i = tot.set_index(["geography", "category", "pack_type", "year"])["value"]
    d = (leaf - tot_i.reindex(leaf.index)).abs()
    log(f"**Pack sizes sum to pack-type total:** {int(d.notna().sum())} comparisons, "
        f"max abs diff {d.max():.2f}, over 1.0: {int((d > 1).sum())}")
    log("")
    # Impossible values
    log("**Impossible values**")
    log(f"- negative values: market {int((ms.value < 0).sum())}, channels "
        f"{int((rc.value < 0).sum())}, pack type {int((pt.value < 0).sum())}, "
        f"pack size {int((ps.value < 0).sum())}")
    log(f"- channel shares outside 0-100: {int(((rc.value < 0) | (rc.value > 100.05)).sum())}")
    log(f"- years outside 2015-2025: "
        f"{int(sum((~df.year.between(2015, 2025)).sum() for df in (ms, rc, pt, ps)))}")
    log("")
    # Fully missing series
    log("**Series with no data in any year (kept, flagged as unusable)**")
    for name, df, keys in [
        ("market_sizes", ms, ["geography", "category", "data_type"]),
        ("pack_type", pt, ["geography", "category", "pack_type"]),
    ]:
        allm = df.groupby(keys)["is_missing"].all()
        for idx in allm[allm].index:
            log(f"- {name}: {' / '.join(idx)}")
    n_rc_allm = int(rc.groupby(["geography", "category", "data_type", "outlet_type"])
                    ["is_missing"].all().sum())
    n_ps_allm = int(ps.groupby(["geography", "category", "pack_type", "pack_size"])
                    ["is_missing"].all().sum())
    log(f"- retail_channels: {n_rc_allm} channel series fully missing (channel not tracked)")
    log(f"- pack_size: {n_ps_allm} size series fully missing")
    rtd_geo = set(ms.geography) - set(pt[pt.category == "RTD Coffee"].geography)
    log(f"- geographies with no RTD Coffee rows in pack files at all: {sorted(rtd_geo)}")
    log("")
    # Unusual year-over-year jumps in market sizes
    ms_sorted = ms.sort_values(["geography", "category", "data_type", "year"])
    ms_sorted["yoy"] = ms_sorted.groupby(["geography", "category", "data_type"])["value"] \
        .pct_change(fill_method=None)
    jumps = ms_sorted[ms_sorted.yoy.abs() > 0.30][["geography", "category", "data_type",
                                                   "year", "yoy"]].copy()
    jumps["yoy"] = (jumps["yoy"] * 100).round(1).astype(str) + "%"
    log(f"**Market-size year-over-year changes above +/-30% ({len(jumps)} rows, kept - "
        "unusual is not necessarily wrong)**")
    log("")
    log(md_table(jumps.head(25)))
    log("")

    # ---- Missing before/after (item 7)
    log("## Item 7: Missing values before and after")
    log("")
    log("| file | missing cells in raw wide data ('-' + blank) | missing in clean long data "
        "| rows dropped that were missing | missing filled |")
    log("|---|---|---|---|---|")
    final = {"market_sizes": ms, "retail_channels": rc, "pack_type": pt, "pack_size": ps}
    for key in RAW_FILES:
        before_m = conv[key]["dash"] + conv[key]["blank"]
        after_m = int(final[key]["is_missing"].sum())
        dropped_df = {"retail_channels": long["retail_channels"][
            long["retail_channels"]["Outlet Type"] == "Total"],
            "pack_size": ps_all[ps_all.is_total_row]}.get(key)
        dropped_m = int(dropped_df["is_missing"].sum()) if dropped_df is not None else 0
        log(f"| {key} | {before_m} | {after_m} | {dropped_m} | 0 |")
    log("")

    # ---- Reconciliation (item 10)
    log("## Item 10: Row counts and totals reconciliation")
    log("")
    log("| file | raw rows read | footer dropped | wide data rows | x11 years = long rows "
        "| rows dropped by rules | final rows |")
    log("|---|---|---|---|---|---|---|")
    for key in RAW_FILES:
        m_ = meta[key]
        start = rows_long_start[key]
        fin = len(final[key])
        log(f"| {key} | {m_['rows_read']} | {m_['footer_rows']} | {m_['data_rows']} | {start} | "
            f"{start - fin} | {fin} |")
    log("")
    # totals of a key measure: world coffee retail volume, unchanged by cleaning
    raw_ms = long["market_sizes"]
    sel = (raw_ms["Data Type"] == "Retail Volume")
    log(f"- Sum of all Retail Volume (tonnes) cells, raw vs clean: "
        f"{raw_ms.loc[sel, 'value'].sum():,.1f} vs "
        f"{ms.loc[ms.data_type == 'Retail Volume', 'value'].sum():,.1f}")
    jp_raw = raw_ms.loc[raw_ms.Unit == "JPY billion", "value"].sum()
    jp_cln = ms.loc[ms.unit_original == "JPY billion", "value"].sum()
    log(f"- Sum of JPY value cells: raw {jp_raw:,.1f} (billion) vs clean {jp_cln:,.1f} (million) "
        f"= ratio {jp_cln / jp_raw:.0f}")
    log(f"- Sum of pack_type unit volume, raw vs clean: {long['pack_type']['value'].sum():,.1f} vs "
        f"{pt['value'].sum():,.1f}")
    ps_raw_leaf = long["pack_size"].loc[long["pack_size"]["Pack Size"] != "Total", "value"].sum()
    log(f"- Sum of pack_size non-Total cells, raw vs clean: {ps_raw_leaf:,.1f} vs "
        f"{ps['value'].sum():,.1f}")
    log("")

    # ---- Analysis metric: CAGR 2020-2025 (item 11)
    g = ms.set_index(["geography", "geo_level", "category", "data_type", "unit", "year"])[
        "value"].unstack("year").reset_index()
    g = g.rename(columns={2020: "value_2020", 2025: "value_2025"})
    ok = (g.value_2020 > 0) & (g.value_2025 > 0)
    g["cagr_2020_2025"] = np.where(ok, (g.value_2025 / g.value_2020) ** (1 / 5) - 1, np.nan)
    g["n_years_with_data"] = ms.groupby(["geography", "category", "data_type"])["value"] \
        .count().reindex(pd.MultiIndex.from_frame(g[["geography", "category", "data_type"]])) \
        .values
    growth = g[["geography", "geo_level", "category", "data_type", "unit", "value_2020",
                "value_2025", "cagr_2020_2025", "n_years_with_data"]]
    log("## Item 11: Calculation check - CAGR 2020-2025 (main comparison metric)")
    log("")
    log(f"- series: {len(growth)}; CAGR computed: {int(growth.cagr_2020_2025.notna().sum())}; "
        f"not computed (missing/zero endpoint): {int(growth.cagr_2020_2025.isna().sum())}")
    log("- CAGR is computed within each series in its own unit, so local-currency value "
        "growth is valid without FX conversion; absolute values in different currencies "
        "are never summed or ranked together.")
    log(f"- missing group keys (geography/category/data_type blank) in clean files: "
        f"{int(sum(df[['geography', 'category', 'data_type']].isna().sum().sum() for df in final.values()))}")
    log("")

    # ---- Unique key checks on final tables (item 2)
    log("## Item 2: Unique keys of the clean tables")
    log("")
    keys = {
        "market_sizes": ["geography", "category", "data_type", "year"],
        "retail_channels": ["geography", "category", "data_type", "outlet_type", "year"],
        "pack_type": ["geography", "category", "pack_type", "year"],
        "pack_size": ["geography", "category", "pack_type", "pack_size", "year"],
    }
    for key, cols in keys.items():
        log(f"- {key}: key = {' + '.join(cols)}; duplicated keys = "
            f"{int(final[key].duplicated(cols).sum())}; rows = {len(final[key])}")
    log("")

    # ---- Write outputs (sorted for reproducible files)
    written = []
    for key, cols in keys.items():
        df = final[key].sort_values(cols).reset_index(drop=True)
        written.append(write_csv(df, f"{key}_clean.csv"))
    written.append(write_csv(
        m2.sort_values(keys["retail_channels"]).reset_index(drop=True), "channel_volume.csv"))
    written.append(write_csv(
        growth.sort_values(["category", "data_type", "geography"]).reset_index(drop=True),
        "market_growth_2020_2025.csv"))

    # ---- 50-row sample (real, local only) + synthetic sample (safe to share)
    real_sample = build_sample(ms, rc, pt, ps)
    real_sample.to_csv(ROOT / "output" / "sample_50_real.csv", index=False,
                       float_format="%.4f", lineterminator="\n")
    synth = make_synthetic(real_sample)
    synth.to_csv(SAMPLE / "synthetic_sample_50.csv", index=False,
                 float_format="%.4f", lineterminator="\n")

    # ---- Reproducibility fingerprints (item 13)
    log("## Item 13: Output fingerprints (compare between runs)")
    log("")
    hashes = []
    for p in written + [SAMPLE / "synthetic_sample_50.csv"]:
        h = sha256(p)
        hashes.append(f"{h}  {p.relative_to(ROOT).as_posix()}")
        log(f"- `{p.relative_to(ROOT).as_posix()}`: {h[:16]}")
    (REPORTS / "output_hashes.txt").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    log("")

    (REPORTS / "cleaning_report.md").write_text("\n".join(REPORT) + "\n", encoding="utf-8")
    print(f"\nDone. Report: {REPORTS / 'cleaning_report.md'}")
    return {"market_sizes": ms, "retail_channels": rc, "pack_type": pt, "pack_size": ps,
            "channel_volume": m2, "growth": growth, "meta": meta}


# ---------------------------------------------------------------------------
# Sample selection: difficult cases first, then random ordinary rows
# ---------------------------------------------------------------------------
def build_sample(ms, rc, pt, ps) -> pd.DataFrame:
    def pick(df, mask, dataset, why, n=None):
        s = df[mask].copy()
        if n is not None:
            s = s.head(n)
        s = s.assign(dataset=dataset, why_selected=why)
        label = (s.get("outlet_type", pd.Series(index=s.index, dtype=object))
                 .fillna(s.get("pack_type", pd.Series(index=s.index, dtype=object))))
        if "pack_size" in s:
            label = label + " | " + s["pack_size"]
        s["segment"] = label
        return s[["dataset", "geography", "category", "data_type", "segment", "year",
                  "value", "is_missing", "why_selected"]]

    parts = [
        pick(ms, (ms.geography == "India") & (ms.category == "RTD Coffee") & ms.year.isin([2015, 2025]),
             "market_sizes", "Whole series is '-' in source; kept as NaN, not 0"),
        pick(ms, (ms.unit_original == "JPY billion") & (ms.category == "Coffee") & ms.year.isin([2020, 2025]),
             "market_sizes", "Unit rescaled JPY billion -> JPY million (x1000)"),
        pick(ms, (ms.geography == "China") & (ms.data_type == "Retail Value RSP") & ms.year.isin([2020, 2025]),
             "market_sizes", "Local currency (CNY); cannot be compared to USD rows"),
        pick(ms, (ms.geography == "United Kingdom") & (ms.category == "RTD Coffee")
             & (ms.data_type == "Off-trade Value RSP") & ms.year.isin([2015, 2016]),
             "market_sizes", "Very large YoY growth; unusual but kept"),
        pick(ms, (ms.geography == "World") & (ms.data_type == "Retail Volume") & ms.year.isin([2025]),
             "market_sizes", "Ordinary World total row (control case)"),
        pick(pt, (pt.pack_type == "PET Jars") & (pt.geography == "World") & (pt.year == 2025),
             "pack_type", "Label had trailing space 'PET Jars ' in source"),
        pick(pt, (pt.geography == "United Kingdom") & (pt.pack_type == "Flexible Paper/Plastic")
             & (pt.category == "Coffee") & pt.year.isin([2015, 2025]),
             "pack_type", "Series entirely '-' in source"),
        pick(pt, (pt.geography == "China") & (pt.category == "RTD Coffee")
             & (pt.pack_type == "Brick Liquid Cartons") & pt.year.isin([2025]),
             "pack_type", "Series entirely '-' in source"),
        pick(pt, (pt.geography == "World") & (pt.category == "RTD Coffee")
             & (pt.pack_type == "Stand-Up Pouches") & (pt.year == 2025),
             "pack_type", "Nested level: Stand-Up Pouches sits inside Flexible Packaging (do not add both)"),
        pick(rc, (rc.geography == "World") & (rc.category == "RTD Coffee")
             & rc.outlet_type.isin(["Apparel and Footwear Specialists", "Direct Selling",
                                    "Food/drink/tobacco specialists"]) & (rc.year == 2015),
             "retail_channels", "'-' (not tracked) vs true 0 share - kept distinct"),
        pick(rc, (rc.geography == "Japan") & (rc.category == "RTD Coffee")
             & rc.outlet_type.isin(["Vending", "Retail E-Commerce"]) & rc.year.isin([2025]),
             "retail_channels", "Key channels for Japan RTD"),
        pick(ps, (ps.geography == "Eastern Europe") & (ps.pack_size == "10 g")
             & (ps.pack_type == "Total Packaging") & (ps.category == "Coffee")
             & ps.year.isin([2015, 2025]),
             "pack_size", "Sharp decline 2015 -> 2025; unusual but kept"),
        pick(ps, (ps.category == "RTD Coffee") & (ps.geography == "Japan")
             & (ps.pack_type == "Metal Beverage Cans") & (ps.year == 2025) & ps.value.gt(0),
             "pack_size", "RTD sizes are in ml (Coffee in g) - parsed separately", n=3),
    ]
    sample = pd.concat(parts, ignore_index=True)
    # top up with ordinary rows chosen at random (fixed seed => reproducible)
    rng_rows = pd.concat([
        pick(ms, ms.value.notna(), "market_sizes", "Random ordinary row (seed 576)"),
        pick(rc, rc.value.gt(0), "retail_channels", "Random ordinary row (seed 576)"),
        pick(pt, pt.value.gt(0), "pack_type", "Random ordinary row (seed 576)"),
        pick(ps, ps.value.gt(0), "pack_size", "Random ordinary row (seed 576)"),
    ], ignore_index=True)
    need = max(0, 50 - len(sample))
    sample = pd.concat([sample, rng_rows.sample(n=need, random_state=576)], ignore_index=True)
    return sample.head(50)


def make_synthetic(sample: pd.DataFrame) -> pd.DataFrame:
    """Same structure and missing pattern, but every number is invented."""
    rng = np.random.default_rng(576)
    synth = sample.copy()
    fake = np.round(rng.uniform(1, 1000, len(synth)), 1)
    synth["value"] = np.where(synth["is_missing"], np.nan,
                              np.where(sample["value"].eq(0), 0.0, fake))
    synth.insert(0, "SYNTHETIC_DATA", "YES - values are random, not Euromonitor data")
    return synth


if __name__ == "__main__":
    main()
