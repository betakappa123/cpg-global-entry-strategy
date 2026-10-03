
from __future__ import annotations

import re
from decimal import Decimal
from math import isfinite
from pathlib import Path
from typing import Any

import pandas as pd
from scipy.interpolate import CubicSpline


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = DATA_DIR / "cleaned"
EXPORT_HEADER_ROWS = 5
YEARS = [str(year) for year in range(2015, 2026)]

# World Bank indicator PA.NUS.FCRF: official exchange rate, local currency
# units per US dollar, annual period average. Values are pinned for reproducibility.
FX_RATES_LCU_PER_USD: dict[str, dict[int, float]] = {
    "AUS": {
        2015: 1.33109026, 2016: 1.34521398, 2017: 1.30475808,
        2018: 1.33841215, 2019: 1.43850654, 2020: 1.45308512,
        2021: 1.33122426, 2022: 1.44166446, 2023: 1.50519107,
        2024: 1.51535804, 2025: 1.55199789,
    },
    "BRA": {
        2015: 3.32690438, 2016: 3.49131342, 2017: 3.19138945,
        2018: 3.65382536, 2019: 3.94447110, 2020: 5.15517879,
        2021: 5.39440079, 2022: 5.16397029, 2023: 4.99437976,
        2024: 5.38893491, 2025: 5.58728624,
    },
    "CHN": {
        2015: 6.22748867, 2016: 6.64447783, 2017: 6.75875509,
        2018: 6.61595718, 2019: 6.90838501, 2020: 6.90076727,
        2021: 6.44897518, 2022: 6.73715811, 2023: 7.08399842,
        2024: 7.19749111, 2025: 7.18984737,
    },
    "DEU": {
        2015: 0.90129642, 2016: 0.90342144, 2017: 0.88520551,
        2018: 0.84677267, 2019: 0.89327626, 2020: 0.87550640,
        2021: 0.84549414, 2022: 0.94962375, 2023: 0.92483956,
        2024: 0.92388955, 2025: 0.88496896,
    },
    "FRA": {
        2015: 0.90129642, 2016: 0.90342144, 2017: 0.88520551,
        2018: 0.84677267, 2019: 0.89327626, 2020: 0.87550640,
        2021: 0.84549414, 2022: 0.94962375, 2023: 0.92483956,
        2024: 0.92388955, 2025: 0.88496896,
    },
    "GBR": {
        2015: 0.65454548, 2016: 0.74063446, 2017: 0.77697668,
        2018: 0.74953154, 2019: 0.78344511, 2020: 0.77999958,
        2021: 0.72706494, 2022: 0.81130172, 2023: 0.80453891,
        2024: 0.78241458, 2025: 0.75947396,
    },
    "IND": {
        2015: 64.15194446, 2016: 67.19531281, 2017: 65.12156865,
        2018: 68.38946709, 2019: 70.42034054, 2020: 74.09956688,
        2021: 73.91801282, 2022: 78.60449058, 2023: 82.59927645,
        2024: 83.66928158, 2025: 87.15844835,
    },
    "JPN": {
        2015: 121.04402568, 2016: 108.79290005, 2017: 112.16614108,
        2018: 110.42317934, 2019: 109.00966590, 2020: 106.77458226,
        2021: 109.75432384, 2022: 131.49814044, 2023: 140.49110006,
        2024: 151.36629130, 2025: 149.65792689,
    },
    "THA": {
        2015: 34.24771667, 2016: 35.29638333, 2017: 33.93981106,
        2018: 32.31022574, 2019: 31.04760578, 2020: 31.29367321,
        2021: 31.97709344, 2022: 35.06135021, 2023: 34.80218858,
        2024: 35.29353808, 2025: 32.88280925,
    },
}

GEOGRAPHY_TO_CURRENCY = {
    "Australia": ("AUS", "AUD"),
    "Brazil": ("BRA", "BRL"),
    "China": ("CHN", "CNY"),
    "France": ("FRA", "EUR"),
    "Germany": ("DEU", "EUR"),
    "India": ("IND", "INR"),
    "Japan": ("JPN", "JPY"),
    "Thailand": ("THA", "THB"),
    "United Kingdom": ("GBR", "GBP"),
}

TABLES: dict[str, dict[str, Any]] = {
    "Market Sizes.csv": {
        "key_columns": ["Geography", "Category", "Data Type"],
        "business_key": [
            "Geography", "Category", "Data Type", "Current Constant",
        ],
    },
    "Pack Size.csv": {
        "key_columns": [
            "Geography", "Category", "Packaging Class", "Pack Type",
            "Pack Size", "Data Type",
        ],
        "business_key": [
            "Geography", "Category", "Packaging Class", "Pack Type",
            "Pack Size", "Data Type",
        ],
    },
    "Pack type.csv": {
        "key_columns": [
            "Geography", "Category", "Packaging Class", "Pack Type", "Data Type",
        ],
        "business_key": [
            "Geography", "Category", "Packaging Class", "Pack Type", "Data Type",
        ],
    },
    "Retail channels.csv": {
        "key_columns": ["Geography", "Category", "Outlet Type", "Data Type"],
        "business_key": ["Geography", "Category", "Outlet Type", "Data Type"],
    },
}

FOOTER_PREFIXES = (
    "Research Sources:",
    "Hot Drinks:",
    "Soft Drinks:",
    "Packaging - Beverages:",
    "Date Exported (GMT):",
    "© Euromonitor International",
)
PACK_SIZE_PATTERN = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(g|ml)\s*$", re.IGNORECASE)


def _interpolate_year_series(
    series: pd.Series,
    maximum: float | None = None,
) -> tuple[pd.Series, str | None]:
    """Use cubic spline for supported interior gaps, otherwise linear interpolation."""
    missing = series.isna()
    if not missing.any():
        return series, None

    observed_positions = [
        position for position, value in enumerate(series) if pd.notna(value)
    ]
    missing_positions = [
        position for position, is_missing in enumerate(missing) if is_missing
    ]
    has_interior_support = (
        len(observed_positions) >= 4
        and observed_positions[0] == 0
        and observed_positions[-1] == len(series) - 1
    )

    if has_interior_support:
        try:
            spline = CubicSpline(
                observed_positions,
                [float(series.iloc[position]) for position in observed_positions],
            )
            estimates = [
                float(spline(position)) for position in missing_positions
            ]
        except (ValueError, FloatingPointError):
            estimates = []
        else:
            estimates_are_valid = all(isfinite(value) for value in estimates)
            if series.dropna().ge(0).all():
                estimates_are_valid = estimates_are_valid and all(
                    value >= 0 for value in estimates
                )
            if maximum is not None:
                estimates_are_valid = estimates_are_valid and all(
                    value <= maximum for value in estimates
                )
            if estimates_are_valid:
                result = series.copy()
                result.iloc[missing_positions] = estimates
                return result, "cubic_spline"

    return (
        series.interpolate(method="linear", limit_direction="both"),
        "linear_fallback",
    )


def _read_export(path: Path) -> tuple[pd.DataFrame, int, int]:
    """Read the tabular section and remove only known export footer rows."""
    frame = pd.read_csv(
        path,
        skiprows=EXPORT_HEADER_ROWS,
        dtype="string",
        keep_default_na=False,
        encoding="utf-8-sig",
    )
    frame = frame.apply(lambda column: column.str.strip())
    frame = frame.loc[frame.ne("").any(axis=1)].copy()
    input_rows = len(frame)

    geography = frame["Geography"].fillna("")
    footer_mask = geography.str.startswith(FOOTER_PREFIXES)
    footer_rows = int(footer_mask.sum())
    frame = frame.loc[~footer_mask].copy()

    if frame.empty:
        raise ValueError(f"No business records found in {path.name}.")
    return frame, input_rows, footer_rows


def _parse_pack_size(value: str) -> str:
    """Standardize numeric pack sizes to a number followed by g or ml."""
    if value.casefold() == "total":
        return "Total"
    match = PACK_SIZE_PATTERN.fullmatch(value)
    if match is None:
        raise ValueError(f"Unrecognized pack size: {value!r}")
    amount = Decimal(match.group(1))
    amount_text = format(amount.normalize(), "f")
    unit = match.group(2).lower()
    return f"{amount_text} {unit}"


def _convert_market_values(frame: pd.DataFrame) -> tuple[int, dict[str, int]]:
    """Convert value rows to USD million and normalize comparable volume labels."""
    converted_cells = 0
    converted_geographies: dict[str, int] = {}
    value_rows = frame["Data Type"].str.contains("Value", case=False, na=False)

    for index in frame.index[value_rows]:
        unit = frame.at[index, "Unit"]
        if unit == "USD million":
            continue

        match = re.fullmatch(r"([A-Z]{3}) (million|billion)", unit)
        if match is None:
            raise ValueError(
                f"Unsupported monetary unit {unit!r} for "
                f"{frame.at[index, 'Geography']}."
            )

        currency, magnitude = match.groups()
        currency_mapping = GEOGRAPHY_TO_CURRENCY.get(frame.at[index, "Geography"])
        if currency_mapping is None:
            raise ValueError(
                "No exchange-rate mapping for "
                f"{frame.at[index, 'Geography']} ({currency})."
            )
        country_code, expected_currency = currency_mapping
        if currency != expected_currency:
            raise ValueError(
                f"Unexpected currency {currency!r} for "
                f"{frame.at[index, 'Geography']}; expected {expected_currency!r}."
            )

        scale_to_million = 1.0 if magnitude == "million" else 1000.0
        for year in YEARS:
            rate = FX_RATES_LCU_PER_USD[country_code][int(year)]
            value = float(frame.at[index, year])
            frame.at[index, year] = (
                value * scale_to_million / rate
            )
            converted_cells += 1
        frame.at[index, "Unit"] = "USD million"
        converted_geographies[frame.at[index, "Geography"]] = (
            converted_geographies.get(frame.at[index, "Geography"], 0) + 1
        )

    volume_rows = frame["Data Type"].str.contains("Volume", case=False, na=False)
    frame.loc[volume_rows & frame["Unit"].eq("Tonnes"), "Unit"] = "metric tonnes"
    frame.loc[
        volume_rows & frame["Unit"].eq("million litres"), "Unit"
    ] = "million liters"
    return converted_cells, converted_geographies


def clean_table(filename: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Clean one source export and return its cleaned rows and audit metrics."""
    if filename not in TABLES:
        raise ValueError(f"Unsupported source file: {filename}")

    source_path = DATA_DIR / filename
    if not source_path.is_file():
        raise FileNotFoundError(f"Required source file not found: {source_path}")

    frame, input_rows, footer_rows = _read_export(source_path)
    settings = TABLES[filename]
    key_columns = settings["key_columns"]

    missing_keys = frame[key_columns].eq("").any(axis=1)
    if missing_keys.any():
        examples = frame.loc[missing_keys, key_columns].head(5).to_dict("records")
        raise ValueError(
            f"{filename} contains {int(missing_keys.sum())} non-footer record(s) "
            f"with missing identifying fields: {examples}"
        )

    years = [column for column in frame.columns if column in YEARS]
    if years != YEARS:
        raise ValueError(f"{filename} must contain all year columns {YEARS}.")

    original_year_values = frame[years].copy()
    numeric_values = original_year_values.replace("-", pd.NA).apply(
        pd.to_numeric, errors="coerce"
    )
    invalid_values = (
        original_year_values.ne("")
        & original_year_values.ne("-")
        & numeric_values.isna()
    )
    if invalid_values.any().any():
        bad_cells = invalid_values.stack()
        bad_cells = bad_cells[bad_cells].index.tolist()[:5]
        raise ValueError(f"{filename} has non-numeric year values at {bad_cells}.")

    missing_before = int(numeric_values.isna().sum().sum())
    no_observation_rows = numeric_values.isna().all(axis=1)
    no_observation_rows_removed = int(no_observation_rows.sum())
    if no_observation_rows_removed:
        frame = frame.loc[~no_observation_rows].copy()
        numeric_values = numeric_values.loc[~no_observation_rows].copy()

    missing_after_empty_rows_removed = int(numeric_values.isna().sum().sum())
    interpolation_methods = {"cubic_spline": 0, "linear_fallback": 0}
    if filename == "Retail channels.csv":
        maximum_interpolated_value = 100.0
    else:
        maximum_interpolated_value = None
    for index in numeric_values.index:
        interpolated, method = _interpolate_year_series(
            numeric_values.loc[index],
            maximum=maximum_interpolated_value,
        )
        numeric_values.loc[index] = interpolated
        if method is not None:
            interpolation_methods[method] += 1

    missing_after = int(numeric_values.isna().sum().sum())
    if missing_after:
        raise ValueError(f"{filename} still has missing year values after cleaning.")
    imputed_year_cells = missing_after_empty_rows_removed - missing_after

    frame[years] = numeric_values
    frame = frame.replace("", pd.NA)

    exact_duplicates = int(frame.duplicated(keep="first").sum())
    business_key = settings["business_key"]
    repeated_business_keys = int(
        frame.duplicated(subset=business_key, keep=False).sum()
    )
    if exact_duplicates:
        frame = frame.drop_duplicates(keep="first").copy()

    currency_cells_converted = 0
    converted_geographies: dict[str, int] = {}
    if filename == "Market Sizes.csv":
        currency_cells_converted, converted_geographies = _convert_market_values(frame)
    elif filename == "Pack Size.csv":
        frame["Pack Size"] = frame["Pack Size"].map(_parse_pack_size)

    for column in frame.select_dtypes(include=["string", "object"]).columns:
        frame[column] = frame[column].str.strip()

    if frame.isna().any().any():
        missing_columns = frame.columns[frame.isna().any()].tolist()
        raise ValueError(
            f"Unexpected missing values remain in {filename}: {missing_columns}"
        )

    summary: dict[str, Any] = {
        "source_file": filename,
        "source_rows_before_footer_removal": input_rows,
        "footer_rows_removed": footer_rows,
        "no_observation_rows_removed": no_observation_rows_removed,
        "cleaned_rows": len(frame),
        "exact_duplicate_rows_found": exact_duplicates,
        "repeated_business_key_rows": repeated_business_keys,
        "missing_year_cells_before_imputation": missing_before,
        "missing_year_cells_after_imputation": missing_after,
        "missing_year_cells_imputed": imputed_year_cells,
        "cubic_spline_rows": interpolation_methods["cubic_spline"],
        "linear_fallback_rows": interpolation_methods["linear_fallback"],
        "imputation_method": (
            "row-wise cubic spline; linear fallback when cubic spline is unsupported or invalid"
            if imputed_year_cells
            else "not needed after removing fully unavailable records"
        ),
        "currency_value_cells_converted": currency_cells_converted,
        "converted_geographies": converted_geographies,
        "cleaned_file": str((OUTPUT_DIR / filename).relative_to(PROJECT_DIR)),
    }
    return frame, summary


def clean_all() -> dict[str, dict[str, Any]]:
    """Clean all source tables and write separate CSV outputs under data/cleaned/."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict[str, Any]] = {}

    for filename in TABLES:
        frame, summary = clean_table(filename)
        output_path = OUTPUT_DIR / filename
        frame.to_csv(output_path, index=False, encoding="utf-8")
        results[filename] = summary

    return results


def main() -> None:
    """Run the full cleaning workflow and print a concise audit summary."""
    results = clean_all()
    report = pd.DataFrame.from_dict(results, orient="index")
    columns = [
        "source_rows_before_footer_removal",
        "footer_rows_removed",
        "cleaned_rows",
        "exact_duplicate_rows_found",
        "repeated_business_key_rows",
        "no_observation_rows_removed",
        "missing_year_cells_before_imputation",
        "missing_year_cells_after_imputation",
        "missing_year_cells_imputed",
        "cubic_spline_rows",
        "linear_fallback_rows",
        "currency_value_cells_converted",
        "cleaned_file",
    ]
    print(report[columns].to_string())
    print(f"\nCleaned CSV files were written to: {OUTPUT_DIR}")
    print(
        "\nFX source: World Bank indicator PA.NUS.FCRF, "
        "Official exchange rate (LCU per US$, period average); "
        "annual observations 2015-2025, retrieved 2026-10-02."
    )
    print("Run this script again at any time to recreate the cleaned outputs.")


if __name__ == "__main__":
    main()
