"""Independently compare CSVs with Excel cells; optionally rerun in a fresh process.

Usage: python validate_cleaning.py --reproduce
This module does not import the cleaning functions to reconstruct expected values.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import subprocess
import sys

import pandas as pd
import xlrd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATASETS = ["market_sizes", "retail_channels", "pack_type", "pack_size"]


def hashes(paths):
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths)}


def validate():
    checks = []
    for name in DATASETS:
        book = xlrd.open_workbook(str(DATA / f"coffee_{name}_2015_2025.xls"))
        sheet = book.sheet_by_name("Statistics Data")
        columns = [str(value) for value in sheet.row_values(5)]
        output = pd.read_csv(DATA / f"{name}_clean.csv", keep_default_na=False)
        source_rows = [row for row in range(6, sheet.nrows) if sheet.cell_value(row, 1) != ""]
        assert len(output) == len(source_rows)
        expected_columns = columns[:4] + ["Unit"] + columns[4:] if name == "retail_channels" else columns
        assert list(output.columns) == expected_columns
        numeric_checks = descriptor_checks = missing_checks = 0
        for position, row in enumerate(source_rows):
            for column_index, column in enumerate(columns):
                original = sheet.cell_value(row, column_index)
                actual = output.iloc[position][column]
                if column.isdigit():
                    if str(original).strip() in {"", "-"}:
                        assert actual == "", (name, row + 1, column, actual)
                        missing_checks += 1
                    else:
                        assert float(actual) == float(original), (name, row + 1, column)
                        numeric_checks += 1
                else:
                    assert actual == str(original).strip(), (name, row + 1, column)
                    descriptor_checks += 1
            if name == "retail_channels":
                assert output.iloc[position]["Unit"] == "%"
        checks.append({"dataset": name, "rows_verified": len(source_rows), "numeric_cells_verified": numeric_checks,
                       "missing_cells_verified": missing_checks, "descriptor_cells_verified": descriptor_checks})
    examples = pd.read_csv(DATA / "quality" / "record_checks.csv")
    assert len(examples) == 20 and examples.Match.all()
    screen = pd.read_csv(DATA / "coffee_country_screening.csv")
    assert len(screen) == 20 and not screen.duplicated(["Geography", "Category"]).any()
    assert screen.groupby("Category").size().eq(10).all()
    for _, row in screen.iterrows():
        if pd.isna(row["2015"]) or pd.isna(row["2025"]) or row["2015"] <= 0:
            assert pd.isna(row["CAGR 2015-2025 (%)"])
        else:
            expected = (math.pow(row["2025"] / row["2015"], 0.1) - 1) * 100
            assert math.isclose(row["CAGR 2015-2025 (%)"], expected, rel_tol=1e-12, abs_tol=1e-12)
    samples = [pd.read_csv(path) for path in sorted((DATA / "samples").glob("*_sample.csv"))]
    assert len(samples) == 4 and sum(map(len, samples)) <= 50
    return checks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reproduce", action="store_true")
    args = parser.parse_args()
    results = validate()
    reproduced = False
    if args.reproduce:
        sources = hashes(DATA.glob("*_2015_2025.xls"))
        paths = list(DATA.rglob("*.csv")) + list((DATA / "quality").glob("*/summary.json"))
        before = hashes(paths)
        subprocess.run([sys.executable, str(ROOT / "clean_coffee.py")], cwd=ROOT, check=True)
        assert before == hashes(paths), "Fresh process produced different data or audit files."
        assert sources == hashes(DATA.glob("*_2015_2025.xls")), "Original workbook changed."
        validate()
        reproduced = True
    report = {"independent_excel_cell_checks": results, "fresh_process_outputs_identical": reproduced,
              "command": "python validate_cleaning.py" + (" --reproduce" if args.reproduce else ""),
              "python": sys.version.split()[0], "pandas": pd.__version__, "xlrd": xlrd.__version__}
    (DATA / "quality" / "independent_validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
