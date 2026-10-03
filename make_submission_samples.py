"""Publish the 40 selected real cleaned rows; verify every field before copying.

Run clean_coffee.py first to regenerate the deterministic local samples.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAMES = ['market_sizes', 'retail_channels', 'pack_type', 'pack_size']

def read(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader=csv.DictReader(stream)
        return reader.fieldnames, list(reader)

def generate():
    destination=ROOT/'submission/samples'
    destination.mkdir(parents=True,exist_ok=True)
    count=0
    for name in NAMES:
        source=ROOT/f'data/samples/{name}_sample.csv'
        columns, sample=read(source)
        clean_columns, cleaned=read(ROOT/f'data/{name}_clean.csv')
        assert columns==['Source Excel Row']+clean_columns
        assert len(sample)==10
        for row in sample:
            # The retained records are contiguous from Excel row 7 in these exports.
            expected=cleaned[int(row['Source Excel Row'])-7]
            assert {column:row[column] for column in clean_columns}==expected
        (destination/f'{name}_sample.csv').write_bytes(source.read_bytes())
        count+=len(sample)
    assert count==40
    print('Copied 40 real cleaned rows; all fields match the full cleaned tables.')

if __name__=='__main__':
    generate()
