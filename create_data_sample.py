"""Create small, selected source-data excerpts for the project deliverable."""

from __future__ import annotations

import csv
import re
from decimal import Decimal
from itertools import islice
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
SAMPLE_DIR = DATA_DIR / "sample"
EXPORT_HEADER_ROWS = 5


def _read_business_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        rows = csv.reader(islice(source, EXPORT_HEADER_ROWS, None))
        header = next(rows)
        records = [dict(zip(header, row)) for row in rows if row and any(row)]
    return header, records


def _pack_size_is_10g(value: str) -> bool:
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(g|ml)\s*", value, re.I)
    return (
        match is not None
        and Decimal(match.group(1)) == Decimal("10")
        and match.group(2).casefold() == "g"
    )


def _select_sample(filename: str, records: list[dict[str, str]]) -> list[dict[str, str]]:
    if filename == "Market Sizes.csv":
        selectors = [
            ("Australia", "Coffee", "Retail Value RSP"),
            ("Japan", "Coffee", "Retail Value RSP"),
            ("World", "Coffee", "Retail Value RSP"),
        ]
        selected = []
        for geography, category, data_type in selectors:
            matches = [
                row for row in records
                if row["Geography"] == geography
                and row["Category"] == category
                and row["Data Type"] == data_type
            ]
            if not matches:
                raise ValueError(f"Sample record not found: {geography}/{category}/{data_type}")
            selected.append(matches[0])
        return selected

    if filename == "Pack Size.csv":
        selected = [
            row for row in records
            if row["Geography"] == "North America"
            and row["Category"] == "Coffee"
            and row["Packaging Class"] == "Total"
            and row["Pack Type"] == "Total Packaging"
            and _pack_size_is_10g(row["Pack Size"])
            and row["Data Type"] == "Retail/off-trade Unit Volume"
        ]
    elif filename == "Pack type.csv":
        selected = [
            row for row in records
            if row["Geography"] == "Eastern Europe"
            and row["Category"] == "Coffee"
            and row["Packaging Class"] == "Total"
            and row["Pack Type"] == "Total Packaging"
            and row["Data Type"] == "Retail/off-trade Unit Volume"
        ]
    elif filename == "Retail channels.csv":
        selected = [
            row for row in records
            if row["Geography"] == "World"
            and row["Category"] == "Coffee"
            and row["Outlet Type"] == "Retail Channels"
            and row["Data Type"] == "Retail Volume"
        ]
    else:
        raise ValueError(f"Unsupported source file: {filename}")

    if not selected:
        raise ValueError(f"Sample record not found in {filename}.")
    return selected[:2]


def main() -> None:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    for filename in (
        "Market Sizes.csv",
        "Pack Size.csv",
        "Pack type.csv",
        "Retail channels.csv",
    ):
        header, records = _read_business_rows(DATA_DIR / filename)
        selected = _select_sample(filename, records)
        output_path = SAMPLE_DIR / filename
        with output_path.open("w", encoding="utf-8-sig", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=header, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(selected)
        print(f"{output_path.relative_to(PROJECT_DIR)}: {len(selected)} rows")


if __name__ == "__main__":
    main()
