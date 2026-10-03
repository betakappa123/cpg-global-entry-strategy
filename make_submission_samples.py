"""Create invented schema examples, never samples of Passport observations."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
YEARS = [str(y) for y in range(2015, 2026)]
KEYS = {
    'market_sizes': ['Geography', 'Category', 'Data Type', 'Unit', 'Current Constant'],
    'retail_channels': ['Geography', 'Category', 'Outlet Type', 'Data Type', 'Unit'],
    'pack_type': ['Geography', 'Category', 'Packaging Class', 'Pack Type', 'Data Type', 'Unit'],
    'pack_size': ['Geography', 'Category', 'Packaging Class', 'Pack Type', 'Pack Size', 'Data Type', 'Unit'],
}

def generate():
    folder = ROOT / 'submission/samples'
    folder.mkdir(parents=True, exist_ok=True)
    cases = ['Ordinary numeric values', 'Missing first year', 'All years missing',
             'Explicit zero retained', 'Large change retained', 'Regional context',
             'World context', 'RTD category kept separate', 'Aggregate label retained',
             'Normalized text label']
    for dataset, keys in KEYS.items():
        rows = []
        for i, case in enumerate(cases):
            rtd = i == 7
            row = {'Sample Type': 'SYNTHETIC - NOT PASSPORT DATA', 'Case': case,
                   'Geography': f'Example Country {i+1}', 'Category': 'RTD Coffee' if rtd else 'Coffee',
                   'Data Type': 'Off-trade Volume' if rtd else 'Retail Volume',
                   'Unit': 'million litres' if rtd else 'Tonnes', 'Current Constant': '-',
                   'Outlet Type': 'Retail E-Commerce', 'Packaging Class': 'Total',
                   'Pack Type': 'PET Jars' if i == 9 else 'Total Packaging',
                   'Pack Size': '250 ml' if rtd else 'Total' if i == 8 else '100 g'}
            if i in (5, 6): row['Geography'] = 'Example Region' if i == 5 else 'World'
            if dataset == 'retail_channels':
                row['Unit'] = '%'
                if i == 8: row['Outlet Type'] = 'Total'
            if dataset in ('pack_type', 'pack_size'):
                row.update({'Unit': 'million units', 'Data Type': 'Retail/off-trade Unit Volume'})
            for j, year in enumerate(YEARS):
                value = round((i+1)*2 + j*0.3, 1)
                if i == 1 and j == 0 or i == 2: value = ''
                if i == 3 and j == 0: value = 0
                if i == 4 and j > 0: value = 35
                if dataset == 'retail_channels' and i == 8: value = 100
                row[year] = value
            rows.append({key: row[key] for key in ['Sample Type', 'Case'] + keys + YEARS})
        with (folder / f'{dataset}_synthetic.csv').open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)
    print('Created 40 synthetic demonstration rows; no original data read.')

if __name__ == '__main__':
    generate()
