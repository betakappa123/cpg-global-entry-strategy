"""Reproduce four independent Passport cleaning outputs from original workbooks.

Run from the repository root: python clean_coffee.py
Rules and analytical boundaries: plan.md. All audit files are local under data/.
"""
from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
YEARS = [str(year) for year in range(2015, 2026)]
KEYS = {
    "market_sizes": ["Geography", "Category", "Data Type", "Unit", "Current Constant"],
    "retail_channels": ["Geography", "Category", "Outlet Type", "Data Type"],
    "pack_type": ["Geography", "Category", "Packaging Class", "Pack Type", "Data Type", "Unit"],
    "pack_size": ["Geography", "Category", "Packaging Class", "Pack Type", "Pack Size", "Data Type", "Unit"],
}
COUNTRIES = {"China", "India", "Japan", "Thailand", "Australia", "Brazil", "USA", "France", "Germany", "United Kingdom"}
REGIONS = {"Asia Pacific", "Australasia", "Eastern Europe", "Latin America", "Middle East and Africa", "North America", "Western Europe"}
EXPECTED = {"market_sizes": (79, 72), "retail_channels": (871, 864), "pack_type": (536, 530), "pack_size": (7215, 7209)}


def fingerprint(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_csv(frame, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, encoding="utf-8-sig", na_rep="", lineterminator="\n")


def to_long(clean, dataset):
    """Optional analytical view; it neither merges tables nor drops missing values."""
    labels = [column for column in clean.columns if column not in YEARS]
    long = clean.melt(id_vars=labels, value_vars=YEARS, var_name="Year", value_name="Value")
    long["Year"] = long["Year"].astype(int)
    unknown = set(long["Geography"]) - COUNTRIES - REGIONS - {"World"}
    if unknown:
        raise ValueError(f"Review unknown geographies before classifying them: {unknown}")
    long["Geography Level"] = long["Geography"].map(
        lambda name: "Country" if name in COUNTRIES else "World" if name == "World" else "Region")
    long["Market Role"] = long["Geography"].map(
        lambda name: "Domestic benchmark" if name == "China" else "Foreign candidate" if name in COUNTRIES else "Context only")
    if dataset == "pack_size":
        parts = long["Pack Size"].str.extract(r"^(\d+(?:\.\d+)?) (g|ml)$")
        long["Is Size Total"] = long["Pack Size"].eq("Total")
        unexpected = parts[0].isna() & ~long["Is Size Total"]
        if unexpected.any():
            raise ValueError(f"Unrecognized size labels: {long.loc[unexpected, 'Pack Size'].unique()}")
        long["Size Value"] = pd.to_numeric(parts[0])
        long["Size Unit"] = parts[1]
        assert (long.loc[~long["Is Size Total"], "Size Value"] > 0).all()
    assert not long.duplicated(KEYS[dataset] + ["Year"]).any()
    assert len(long) == len(clean) * len(YEARS)
    return long


def record_checks(raw, clean, dataset):
    """Fixed, manually selected source examples, including difficult cases."""
    cases = {
        "market_sizes": [
            ({"Geography": "China", "Category": "Coffee", "Data Type": "Retail Volume"}, "2025", 61314.5),
            ({"Geography": "Japan", "Category": "Coffee", "Data Type": "Retail Value RSP"}, "2025", 461.1),
            ({"Geography": "India", "Category": "RTD Coffee", "Data Type": "Off-trade Volume"}, "2015", None),
            ({"Geography": "India", "Category": "RTD Coffee", "Data Type": "Off-trade Value RSP"}, "2025", None),
            ({"Geography": "World", "Category": "Coffee", "Data Type": "Retail Volume"}, "2025", 6175791.8),
        ],
        "retail_channels": [({"Geography": "World", "Category": "Coffee", "Outlet Type": outlet}, "2015", value)
                            for outlet, value in [("Retail Channels", 100), ("Retail Offline", 97.8), ("Retail E-Commerce", 2.2), ("Apparel and Footwear Specialists", None), ("Total", 100)]],
        "pack_type": [
            ({"Geography": "Western Europe", "Category": "Coffee", "Pack Type": "Total Packaging"}, "2015", 9598.9),
            ({"Geography": "Latin America", "Category": "Coffee", "Pack Type": "Flexible Aluminium/Paper"}, "2015", None),
            ({"Geography": "Latin America", "Category": "Coffee", "Pack Type": "Flexible Aluminium/Paper"}, "2025", 0.1),
            ({"Geography": "Thailand", "Category": "Coffee", "Pack Type": "PET Jars"}, "2025", 24.2),
            ({"Geography": "Thailand", "Category": "RTD Coffee", "Pack Type": "Other Packaging"}, "2025", 10),
        ],
        "pack_size": [
            ({"Geography": "World", "Category": "Coffee", "Pack Type": "Total Packaging", "Pack Size": "100 g"}, "2025", 3774.2),
            ({"Geography": "China", "Category": "Coffee", "Pack Type": "Total Packaging", "Pack Size": "1000 g"}, "2015", None),
            ({"Geography": "North America", "Category": "Coffee", "Pack Type": "Total Packaging", "Pack Size": "Total"}, "2025", 3314.5),
            ({"Geography": "Western Europe", "Category": "Coffee", "Pack Type": "PET Jars", "Pack Size": "100 g"}, "2025", 0.1),
            ({"Geography": "World", "Category": "RTD Coffee", "Pack Type": "Total Packaging", "Pack Size": "250 ml"}, "2025", 2508.1),
        ],
    }
    records = []
    for selector, year, expected in cases[dataset]:
        mask = pd.Series(True, index=clean.index)
        for field, value in selector.items():
            mask &= clean[field].eq(value)
        assert mask.sum() == 1, selector
        index = clean.index[mask][0]
        actual = clean.at[index, year]
        matches = bool(pd.isna(actual)) if expected is None else bool(actual == expected)
        assert matches, (selector, actual, expected)
        records.append({"Dataset": dataset, "Source Excel Row": int(index + 7),
                        "Selection": json.dumps(selector, sort_keys=True), "Year": year,
                        "Original Value": raw.at[index, year], "Expected Value": expected,
                        "Actual Value": actual, "Match": matches,
                        "Reason": "Preserve unavailable observation, not zero" if expected is None else "Preserve reported number, original unit, and row identity"})
    return pd.DataFrame(records)


def clean_dataset(dataset, data_dir=None):
    data_dir = ROOT / "data" if data_dir is None else Path(data_dir)
    source = data_dir / f"coffee_{dataset}_2015_2025.xls"
    audit_dir = data_dir / "quality" / dataset
    source_hash = fingerprint(source)
    raw = pd.read_excel(source, sheet_name="Statistics Data", header=5)
    keys = KEYS[dataset]
    assert list(raw.columns) == keys + YEARS, "Source schema changed; inspect before cleaning."
    source_title = str(pd.read_excel(source, sheet_name="Statistics Data", header=None).iloc[4, 0])
    data_mask = raw["Category"].notna()
    excluded = raw.loc[~data_mask].copy()
    allowed_notes = ("Research Sources:", "Hot Drinks:", "Soft Drinks:", "Packaging - Beverages:", "Date Exported (GMT):", "© Euromonitor International")
    assert excluded.drop(columns="Geography").isna().all().all(), "Unexpected non-data row contents."
    assert excluded["Geography"].map(lambda value: pd.isna(value) or str(value).strip().startswith(allowed_notes)).all()
    clean = raw.loc[data_mask].copy()
    assert (len(raw), len(clean)) == EXPECTED[dataset], "Source version changed; review counts."
    excluded.insert(0, "Source Excel Row", excluded.index + 7)
    save_csv(excluded, audit_dir / "excluded_rows.csv")

    text_changes, categories = [], []
    for field in keys:
        before = clean[field].astype("string")
        after = before.str.strip()
        assert after.notna().all() and after.ne("").all(), f"Missing key: {field}"
        for index in clean.index[before.ne(after)]:
            text_changes.append({"Source Excel Row": int(index + 7), "Column": field,
                                 "Before": before.at[index], "After": after.at[index]})
        for stage, series in [("Before", before), ("After", after)]:
            for label, count in series.value_counts(dropna=False).sort_index().items():
                categories.append({"Column": field, "Stage": stage, "Label": label, "Count": int(count)})
        clean[field] = after
    text_changes = pd.DataFrame(text_changes, columns=["Source Excel Row", "Column", "Before", "After"])
    save_csv(text_changes, audit_dir / "text_changes.csv")
    save_csv(pd.DataFrame(categories), audit_dir / "categories.csv")

    missing_rows = []
    for year in YEARS:
        before = clean[year].astype("string").str.strip()
        dash = before.eq("-").fillna(False)
        blank = before.isna() | before.eq("").fillna(False)
        numeric = pd.to_numeric(before.mask(dash | blank), errors="coerce").astype("float64")
        failed = numeric.isna() & ~(dash | blank)
        if failed.any():
            raise ValueError(f"Unexpected annual text in {dataset}/{year}: {before[failed].tolist()}")
        clean[year] = numeric
        missing_rows.append({"Year": year, "Before dtype": str(raw[year].dtype), "After dtype": str(numeric.dtype),
                             "Original blanks": int(blank.sum()), "Original dashes": int(dash.sum()),
                             "Missing after": int(numeric.isna().sum()), "Valid after": int(numeric.notna().sum()), "Conversion failures": int(failed.sum())})
    missing = pd.DataFrame(missing_rows)
    save_csv(missing, audit_dir / "missingness_and_types.csv")
    if dataset == "retail_channels":
        assert "% breakdown" in source_title
        clean.insert(len(keys), "Unit", pd.Series("%", index=clean.index, dtype="string"))
    duplicate_counts = {"exact_before": int(raw.loc[data_mask].duplicated().sum()),
                        "key_before": int(raw.loc[data_mask].duplicated(keys).sum()),
                        "exact_after": int(clean.duplicated().sum()), "key_after": int(clean.duplicated(keys).sum())}
    assert not any(duplicate_counts.values()), f"Investigate duplicates: {duplicate_counts}"

    # Flag unusual values; retain them and their original source-row identities.
    flags = []
    def add_flags(mask, year, reason, prior=None):
        for index in clean.index[mask]:
            flags.append({"Source Excel Row": int(index + 7), **clean.loc[index, keys].to_dict(),
                          "Year": year, "Value": clean.at[index, year],
                          "Previous Value": clean.at[index, prior] if prior else None, "Reason": reason, "Action": "Retained; investigate before interpretation"})
    for position, year in enumerate(YEARS):
        values = clean[year]
        add_flags(values.lt(0) | (values.notna() & ~np.isfinite(values)), year, "Negative or non-finite")
        if dataset == "retail_channels":
            add_flags(values.gt(100), year, "Channel share above 100 percent")
        if position:
            prior = YEARS[position - 1]
            previous = clean[prior]
            if dataset == "retail_channels":
                add_flags((values - previous).abs().gt(10), year, "Adjacent change greater than 10 percentage points", prior)
            else:
                add_flags(previous.gt(0) & ((values / previous - 1).abs().gt(0.5)), year, "Adjacent relative change greater than 50 percent", prior)
                add_flags(previous.eq(0) & values.notna() & values.ne(0), year, "Nonzero value after zero; relative growth undefined", prior)
    flags = pd.DataFrame(flags, columns=["Source Excel Row", *keys, "Year", "Value", "Previous Value", "Reason", "Action"])
    save_csv(flags, audit_dir / "flags.csv")

    long = to_long(clean, dataset)
    groups = [field for field in keys if field != "Geography"] + ["Geography Level", "Year"]
    # Group counts measure coverage. No totals are calculated across overlapping hierarchy levels.
    profile = long.groupby(groups, dropna=False, observed=True)["Value"].agg(
        rows="size", valid="count", minimum="min", q25=lambda x: x.quantile(0.25),
        median="median", q75=lambda x: x.quantile(0.75), maximum="max").reset_index()
    profile["missing"] = profile["rows"] - profile["valid"]
    save_csv(profile, audit_dir / "numeric_profile.csv")
    checks = record_checks(raw, clean, dataset)
    save_csv(checks, audit_dir / "record_checks.csv")

    output = data_dir / f"{dataset}_clean.csv"
    save_csv(clean, output)
    descriptors = {column: "string" for column in clean.columns if column not in YEARS}
    reloaded = pd.read_csv(output, dtype={**descriptors, **{year: "float64" for year in YEARS}})
    pd.testing.assert_frame_equal(clean.reset_index(drop=True), reloaded, check_exact=True)
    assert fingerprint(source) == source_hash, "Source changed."
    summary = {"dataset": dataset, "source": source.name, "source_sha256": source_hash,
               "source_title": source_title, "source_export": next(str(x).strip() for x in excluded.Geography.dropna() if str(x).strip().startswith("Date Exported")),
               "output": output.name, "output_sha256": fingerprint(output),
               "imported_rows": len(raw), "cleaned_rows": len(clean), "excluded_rows": len(excluded),
               "annual_observations": len(long), "valid_values": int(clean[YEARS].notna().sum().sum()),
               "missing_values": int(clean[YEARS].isna().sum().sum()), "zero_values": int(clean[YEARS].eq(0).sum().sum()),
               "text_cells_trimmed": len(text_changes), "flagged_observations": len(flags),
               "conversion_failures": int(missing["Conversion failures"].sum()), **duplicate_counts,
               "record_checks_passed": int(checks.Match.sum()), "csv_reload_matches": True}
    (audit_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    # At most ten actual cleaned records per dataset, including review cases.
    sample_indices = list(dict.fromkeys((checks["Source Excel Row"] - 7).tolist()))
    for mask in [clean[YEARS].isna().any(axis=1), clean[YEARS].isna().all(axis=1), clean[YEARS].eq(0).any(axis=1)]:
        candidates = clean.index[mask].tolist()
        if candidates:
            sample_indices.append(candidates[0])
    sample_indices.extend((text_changes["Source Excel Row"] - 7).head(1).tolist())
    sample_indices.extend(clean.index.tolist())
    sample_indices = list(dict.fromkeys(sample_indices))[:10]
    sample = clean.loc[sample_indices].copy()
    sample.insert(0, "Source Excel Row", sample.index + 7)
    save_csv(sample, data_dir / "samples" / f"{dataset}_sample.csv")
    return {"clean": clean, "summary": summary, "missingness": missing, "flags": flags,
            "checks": checks, "text_changes": text_changes}


def country_screen(market):
    """Descriptive screen, not an entry recommendation or combined score."""
    mask = market.Geography.isin(COUNTRIES) & (
        (market.Category.eq("Coffee") & market["Data Type"].eq("Retail Volume") & market.Unit.eq("Tonnes")) |
        (market.Category.eq("RTD Coffee") & market["Data Type"].eq("Off-trade Volume") & market.Unit.eq("million litres")))
    selected = market.loc[mask].copy()
    assert not selected.duplicated(["Geography", "Category"]).any()
    result = selected[["Geography", "Category", "Data Type", "Unit", "2015", "2025"]].copy()
    result["Market Role"] = np.where(result.Geography.eq("China"), "Domestic benchmark", "Foreign candidate")
    result["Available Years"] = selected[YEARS].notna().sum(axis=1)
    valid = selected["2015"].gt(0) & selected["2025"].ge(0) & np.isfinite(selected["2015"]) & np.isfinite(selected["2025"])
    result["CAGR 2015-2025 (%)"] = np.nan
    result.loc[valid, "CAGR 2015-2025 (%)"] = ((selected.loc[valid, "2025"] / selected.loc[valid, "2015"]) ** (1 / 10) - 1) * 100
    result["Growth Status"] = np.where(valid, "Both endpoints available; positive baseline", "Unavailable: missing, non-finite, or invalid endpoint/baseline")
    return result.sort_values(["Category", "Geography"]).reset_index(drop=True)


def run_all(data_dir=None):
    data_dir = ROOT / "data" if data_dir is None else Path(data_dir)
    results = {dataset: clean_dataset(dataset, data_dir) for dataset in KEYS}
    summary = pd.DataFrame([result["summary"] for result in results.values()])
    save_csv(summary, data_dir / "quality" / "summary.csv")
    save_csv(country_screen(results["market_sizes"]["clean"]), data_dir / "coffee_country_screening.csv")
    save_csv(pd.concat([r["checks"] for r in results.values()], ignore_index=True), data_dir / "quality" / "record_checks.csv")
    return results


if __name__ == "__main__":
    results = run_all()
    print(pd.DataFrame([r["summary"] for r in results.values()])[
        ["dataset", "cleaned_rows", "missing_values", "text_cells_trimmed", "flagged_observations", "record_checks_passed"]].to_string(index=False))
