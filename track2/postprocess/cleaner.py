"""Track 2 post-processing — validate and clean model outputs."""

import csv
import io
import re


def clean_csv(raw: str, config: dict) -> str:
    """Validate and normalise CSV output."""
    text = raw.strip()
    # Strip markdown code fences
    text = re.sub(r"^```(?:csv)?\s*\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()

    # Check it parses as valid CSV
    try:
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
        if not rows:
            return ""
        # Re-serialise to ensure consistent formatting
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerows(rows)
        return out.getvalue().strip()
    except Exception:
        # Return raw if we can't parse it
        return text


def clean_summary(raw: str, config: dict) -> str:
    """Clean summary output."""
    text = raw.strip()
    # Strip markdown fences
    text = re.sub(r"^```\w*\s*\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()

    # Check minimum numeric content for Numeric Fact F1
    numbers_found = re.findall(r"\b\d+(?:[.,]\d+)*\b", text)
    min_required = config.get("postprocess", {}).get("min_numbers_in_summary", 3)
    if len(numbers_found) < min_required:
        # Log warning but don't modify — the model may have seen a chart with few numbers
        pass

    return text
