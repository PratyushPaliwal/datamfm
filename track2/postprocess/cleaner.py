"""
Track 2 post-processing — aligned with ground truth format.

Key insight from GT analysis:
- GT CSVs preserve spaces in values ("90 % Nat." not "90%Nat.")
- GT CSVs use exact chart label text — do NOT over-normalise
- GT summaries are verbose (250-330 words) — do NOT truncate
- Numbers in summaries must match CSV exactly for Numeric Fact F1
"""

import csv
import io
import re


def clean_csv(raw: str, config: dict = None) -> str:
    """
    Clean CSV output — conservative normalisation to match GT format.
    GT preserves spaces, special chars in labels — don't over-clean.
    """
    text = raw.strip()

    # Strip markdown fences
    text = re.sub(r'^```(?:csv)?\s*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n```\s*$', '', text, flags=re.MULTILINE)
    text = text.strip()

    # Remove any "Title:" or "Source:" prefix lines the model adds
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Skip obvious non-CSV lines
        if stripped.lower().startswith(('title:', 'source:', 'note:', 'chart:')):
            continue
        cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)

    # ONLY expand K/M/B in pure numeric columns (not in label columns)
    # Conservative: only expand if the whole cell is a number+suffix
    def expand_number(m):
        val = float(m.group(1))
        suffix = m.group(2).upper()
        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        return str(int(val * multipliers[suffix]))

    # Apply only to cells that are purely numeric+suffix (not labels)
    lines = text.splitlines()
    if len(lines) > 1:
        # Detect which columns are numeric from the data rows
        processed = []
        for i, line in enumerate(lines):
            if i == 0:  # header row — never touch
                processed.append(line)
                continue
            # Only expand K/M/B in cells that are purely number+suffix
            cells = line.split(',')
            new_cells = []
            for cell in cells:
                c = cell.strip()
                match = re.match(r'^(-?\d+\.?\d*)([KMB])$', c, re.IGNORECASE)
                if match:
                    new_cells.append(expand_number(match))
                else:
                    new_cells.append(cell)
            processed.append(','.join(new_cells))
        text = '\n'.join(processed)

    # Validate it parses as CSV
    try:
        rows = list(csv.reader(io.StringIO(text)))
        if not rows:
            return text
        # Re-emit clean CSV preserving original values
        out = io.StringIO()
        writer = csv.writer(out, lineterminator='\n')
        writer.writerows(rows)
        return out.getvalue().strip()
    except Exception:
        return text


def clean_summary(raw: str, config: dict = None) -> str:
    """
    Clean summary output.
    GT summaries are 250-330 words — preserve length, don't truncate.
    """
    text = raw.strip()

    # Strip markdown fences
    text = re.sub(r'^```\w*\s*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n```\s*$', '', text, flags=re.MULTILINE)
    text = text.strip()

    # Strip common model preambles
    preambles = [
        "Here is a comprehensive description:",
        "Here is the summary:",
        "Here's the description:",
        "Sure, here is",
        "Based on the chart,",
    ]
    for p in preambles:
        if text.lower().startswith(p.lower()):
            text = text[len(p):].strip()

    return text


def extract_numbers_from_text(text: str) -> list[float]:
    """Extract all numeric values from text for Numeric Fact F1 verification."""
    raw = re.findall(r'-?\d+\.?\d*', text.replace(',', ''))
    nums = []
    for r in raw:
        try:
            nums.append(float(r))
        except ValueError:
            pass
    return nums


def verify_numbers_in_summary(summary: str, csv_text: str) -> dict:
    """
    Check how many CSV numbers appear in the summary.
    Used for quality assessment before submission.
    """
    csv_nums = set(extract_numbers_from_text(csv_text))
    summary_nums = set(extract_numbers_from_text(summary))
    overlap = csv_nums & summary_nums
    coverage = len(overlap) / len(csv_nums) if csv_nums else 1.0
    return {
        'csv_numbers': len(csv_nums),
        'summary_numbers': len(summary_nums),
        'overlap': len(overlap),
        'coverage': round(coverage, 3),
    }
