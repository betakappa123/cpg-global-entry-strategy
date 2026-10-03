"""Build the individual report from real local audit evidence.

Run after clean_coffee.py and validate_cleaning.py --reproduce.
Requires the optional requirements-report.txt dependency.
"""
import argparse
import csv
import html
import json
import re
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent
NAMES = ['market_sizes', 'retail_channels', 'pack_type', 'pack_size']

def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))

def md_table(headers, rows):
    def safe(value):
        return str(value).replace('|', '/').replace('\n', ' ')
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                       '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(map(safe, row)) + ' |' for row in rows])

def report_text(commit):
    text = (ROOT / 'submission/report-template.md').read_text()
    text = text.replace('**Individual workspace:** Wendy', '**Student:** Wendy Sun')
    text = text.replace('**Prepared:** October 2, 2026', '**Prepared:** October 3, 2026')
    text = text.replace('**Status:** Local implementation and validation evidence; team reconciliation and student review remain outstanding. This is not a completed group submission.',
        '**Status:** Individual submission under the updated Module 6 instructions. No group submission or ZIP is required.\n\n'
        '**Branch:** Wendy\n\n**Branch URL:** https://github.com/betakappa123/cpg-global-entry-strategy/tree/Wendy\n\n'
        f'**Submitted implementation commit:** {commit}\n\n'
        'This immutable commit identifies the submitted code, notebook and demonstration sample. A later documentation-only commit adds its ID to the report and README. Instructor repository access must be available; a URL does not grant private-repository access.')
    text = text.replace('## Individual checklist for team reconciliation', '## Individual 14-item checklist')
    text = text.replace('Student review and independent team reconciliation have not been performed by Codex.',
        'Student review is described below from the actual discussion; no manual source-workbook audit by the student is claimed. Team reconciliation is not required by the updated assignment.')
    text = text.replace("The group's final PDF/checklist needs reconciliation with teammates' independent results.",
        'The updated assignment requires this personal PDF on Gradescope and the accompanying materials on the individual branch.')
    text = text.replace('A rendered HTML preview was generated for presentation review, but browser policy blocked opening the local file; visual layout has not been verified in a notebook viewer. Open `DataClean.ipynb` in VS Code to review the saved presentation.',
        'The student reviewed the saved notebook output during the discussion. PDF presentation is checked separately before delivery.')
    text = text.replace('## Codex verification response', '''## How I checked one Codex suggestion

Codex suggested converting annual dash markers to missing numeric values while retaining the affected records rather than filling them with zero or deleting them. I inspected the notebook's before/after missingness table and questioned why every year still had two missing values, what the columns meant, and why keeping the incomplete records was useful. I also asked why dashes remained in Current Constant and learned that descriptor markers and annual observations require different rules.

For Market Sizes, the displayed evidence was 72 records per year = 70 available numeric values + 2 missing values, with zero unexpected conversion failures. The same two India RTD records have unavailable annual observations throughout the period. This count reconciliation, together with the distinction between unknown quantities and confirmed zero sales, supported retaining the records and excluding unavailable growth estimates from calculation. I accepted that decision after the explanation. Source definitions remain a limitation.

This was a review of displayed results and the reasoning behind the suggestion. I did not personally verify every Excel cell or independently establish Passport's business meaning for the dash. Codex performed the separate full-source comparison described below. This distinction preserves an accurate account of my role.

## Automated verification evidence''')
    # Explicit checks accompany every rule instead of relying on general assurances.
    checks = [
        'Original XLS SHA-256 hashes unchanged; separate CSV paths and row counts verified.',
        'Excluded rows must have missing non-Geography fields and recognized note/blank labels; 26 rows logged.',
        'Text-change log records 65 corrections; key collisions remain zero; all descriptors independently compared.',
        'Per-column before/after missing counts reconcile; conversion failures zero; every numeric/missing cell checked.',
        'Independent descriptor comparison confirms the source dash is retained on the same records.',
        'Source title contains % breakdown; validator checks the added unit on every channel record.',
        'Independent comparison verifies every original unit/category and available number unchanged.',
        'Composite keys and source labels preserved; no totals calculated across hierarchy levels.',
        'Complete flag lists saved; all flagged cells included in source comparisons; zero negative/non-finite values.',
        'Long row count equals wide rows times 11; long keys unique; all non-total sizes parse as positive g/ml.',
        'Independent recalculation matches all 19 computable CAGRs; India RTD remains uncomputable.',
        'No cross-table analytical joins; each table independently reconciles its source/output row counts.'
    ]
    start = text.index('| Decision | Reason |'); end = text.index('\n\n**Workflow history:**', start)
    lines = text[start:end].splitlines()
    rows = [[x.strip() for x in line.strip('|').split('|')] for line in lines[2:]]
    text = text[:start] + md_table(['Rule', 'Reason', 'Check and result'],
        [[row[0], row[1], check] for row, check in zip(rows, checks)]) + text[end:]

    text += '\n\n## Additional source-based check of the Codex suggestion\n\n'
    text += (ROOT / 'submission/missing-rule-review.md').read_text().replace('# Source-based review of a Codex suggestion', '').replace('## ', '### ')
    text += '\n\n## Embedded evidence A: Five original-to-cleaned record checks\n\n'
    text += ('Expected rules and selected cases were documented in plan.md before the four-table implementation; '
             'the earlier Market Sizes draft is explicitly disclosed in the workflow history. '
             'These five cases cover all four datasets and include missing values and whitespace correction. '
             'They supplement, rather than replace, the full-data validation.\n\n')
    records = read_csv(ROOT / 'data/quality/record_checks.csv')
    chosen = [records[0], records[2], records[6], records[13], records[19]]
    for i, row in enumerate(chosen, 1):
        keys = json.loads(row['Selection'])
        text += f"### Record {i}: {row['Dataset']}\n\n"
        text += '; '.join(f'{k}: {v}' for k, v in keys.items()) + '.\n\n'
        expected = row['Expected Value'] or 'Missing (NaN)'
        actual = row['Actual Value'] or 'Missing (NaN)'
        original = row['Original Value']
        reason = row['Reason']
        if row['Dataset'] == 'pack_type':
            original = 'PET Jars [trailing space]; ' + original
            expected = 'PET Jars; ' + expected; actual = 'PET Jars; ' + actual
            reason += '; trim the observed trailing space without changing category meaning'
        text += md_table(['Excel row', 'Year', 'Original', 'Expected', 'Actual', 'Match'],
                         [[row['Source Excel Row'], row['Year'], original, expected, actual, row['Match']]])
        text += '\n\nReason: ' + reason + '.\n\n'

    text += '## Embedded evidence B: Missingness and types by year column\n\n'
    text += ('All affected year columns are shown. Before types are object; after types are float64. '
             'Original blanks exclude the separately logged footer rows. A dash is not an original blank, '
             'but becomes a missing numeric observation. Descriptor fields have zero missing/empty keys after trimming.\n\n')
    for name in NAMES:
        rows = read_csv(ROOT / f'data/quality/{name}/missingness_and_types.csv')
        text += f'### {name}\n\n' + md_table(['Year', 'Blanks before', 'Dashes before', 'Missing after', 'Valid after', 'Failures'],
            [[r[k] for k in ['Year', 'Original blanks', 'Original dashes', 'Missing after', 'Valid after', 'Conversion failures']] for r in rows]) + '\n\n'

    text += '## Embedded evidence C: Source identity and reproducibility\n\n'
    for name in NAMES:
        summary = json.loads((ROOT / f'data/quality/{name}/summary.json').read_text())
        text += f"**{name}:** {summary['source']}\n\n{summary['source_export']}\n\nSHA-256: {summary['source_sha256']}\n\n"
    validation = json.loads((ROOT / 'data/quality/independent_validation.json').read_text())
    if not validation['fresh_process_outputs_identical']:
        raise RuntimeError('Complete a successful --reproduce validation before generating the report.')
    text += ('Command: `python validate_cleaning.py --reproduce`. A new Python process reproduced all checked CSV/audit files '
             'byte-for-byte and the original workbook hashes were unchanged. The notebook was also restarted and run from top to bottom. '
             'Python ' + validation['python'] + '; pandas ' + validation['pandas'] + '; xlrd ' + validation['xlrd'] + '.\n\n')
    text += '''## Sample selection and instructor access

The branch includes 40 explicitly synthetic cleaned-schema examples under submission/samples/, ten per dataset. They were constructed to illustrate valid numbers, missing years, all-missing records, explicit zero, large changes, geography levels, channel totals, package size totals and normalized labels. They include all cleaned columns plus Sample Type and Case. No sample row is a real Passport observation, and no validation claim or market conclusion is derived from these examples. The generator does not read original data.

The actual local sample selection starts with planned record-check cases, adds missing/all-missing/zero/whitespace examples where available, then fills in source order to ten rows per table. All data checks use the full real dataset, not either sample. Real local data remains under data/.

README lists USC Passport access links via project-start.md, filenames, export versions, dependencies, exact run commands and expected outputs. An instructor with authorized source access can rerun the workflow. Wendy can arrange review of the exact originals and local outputs through a course-approved channel; no such access approval is claimed here. Repository visibility and instructor access should be confirmed before submission. The original local evidence files can be regenerated using the documented commands; essential counts and five record checks are embedded in this PDF so they do not depend on local paths.
'''
    # ASCII punctuation avoids unsupported glyphs in the portable PDF fonts.
    return text.replace('\u2013', '-').replace('\u2014', '-').replace('\u2019', "'").replace('\u2011', '-')

def render_pdf(text, destination):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='BodyReport', fontName='Helvetica', fontSize=9, leading=12.5, spaceAfter=7))
    styles.add(ParagraphStyle(name='TableReport', fontName='Helvetica', fontSize=7.6, leading=10))
    styles['Heading1'].fontSize=17; styles['Heading1'].leading=21
    styles['Heading2'].fontSize=12; styles['Heading2'].leading=15
    styles['Heading2'].textColor=colors.HexColor('#14566a')
    for heading in ['Heading1', 'Heading2', 'Heading3']:
        styles[heading].keepWithNext = True
    def fmt(value):
        value=html.escape(value)
        value=re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', value)
        value=re.sub(r'`([^`]+)`', r'\1', value)
        return value
    story=[]; lines=text.splitlines(); i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line.startswith('|'):
            tablelines=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                tablelines.append(lines[i].strip());i+=1
            rows=[]
            for t in tablelines:
                cells=[v.strip() for v in t.strip('|').split('|')]
                if all(re.fullmatch(r'[-: ]+', v) for v in cells):continue
                rows.append([Paragraph(fmt(v),styles['TableReport']) for v in cells])
            count=len(rows[0]); widths=[524/count]*count
            if count==3: widths=[125,155,244]
            table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5f0f3')),
                ('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#cbd5df')),
                ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
                ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            story.extend([table,Spacer(1,9)]);continue
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#'))
            story.append(Paragraph(fmt(line[level:].strip()),styles[f'Heading{min(level,3)}']))
        else:
            paragraph = [line]
            while i+1 < len(lines) and lines[i+1].strip() and not lines[i+1].strip().startswith(('#', '|', '- ', '**')) and not re.match(r'^\d+\.', lines[i+1].strip()) and not line.startswith(('- ', '**')) and not re.match(r'^\d+\.', line):
                i += 1
                paragraph.append(lines[i].strip())
            para = Paragraph(fmt(' '.join(paragraph)),styles['BodyReport'])
            if line.startswith('Category:'):
                para.keepWithNext = True
            story.append(para)
        i+=1
    def footer(canvas,doc):
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#64748b'))
        canvas.drawString(44,24,'Wendy Sun | DSO 576 Module 6 | Individual submission')
        canvas.drawRightString(568,24,f'Page {doc.page}')
    destination.parent.mkdir(parents=True,exist_ok=True)
    SimpleDocTemplate(str(destination),pagesize=letter,rightMargin=44,leftMargin=44,
        topMargin=38,bottomMargin=42,title='Wendy Sun - Module 6 Data Cleaning',author='Wendy Sun').build(story,onFirstPage=footer,onLaterPages=footer)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--commit',required=True);args=parser.parse_args()
    commit=subprocess.check_output(['git','rev-parse',args.commit],cwd=ROOT,text=True).strip()
    text=report_text(commit)
    (ROOT/'cleaning-report.md').write_text(text)
    path=ROOT/'output/pdf/Wendy_Sun_Module_6_Data_Cleaning.pdf'
    render_pdf(text,path)
    print(path)
