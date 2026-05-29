import csv
import io
import re


def clean_csv(raw: str, config: dict) -> str:
    """
    Clean model CSV output for Chart Understanding.

    Goals:
    - remove markdown/code fences
    - remove explanations
    - normalize K/M/B abbreviations
    - remove currency symbols
    - normalize row structure
    """
    text = (raw or "").strip()

    if not text:
        return ""

    # Remove code fences.
    text = re.sub(r"```(?:csv)?", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "")

    # Normalize escaped line breaks.
    text = text.replace("\\n", "\n")
    text = text.replace("<0x0A>", "\n")
    text = text.replace("<0x0a>", "\n")

    # Remove common preambles.
    text = re.sub(
        r"(?is)^.*?(csv|table)\s*[:\-]\s*",
        "",
        text,
    ).strip()

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    cleaned_lines = []

    for line in lines:
        lower = line.lower()

        # Drop natural-language lines.
        if lower.startswith(
            (
                "here is",
                "the csv",
                "csv output",
                "converted",
                "this chart",
                "the chart",
            )
        ):
            continue

        # Convert number suffixes.
        line = re.sub(
            r"(?i)(\d+(?:\.\d+)?)\s*K\b",
            lambda m: str(float(m.group(1)) * 1000).rstrip("0").rstrip("."),
            line,
        )
        line = re.sub(
            r"(?i)(\d+(?:\.\d+)?)\s*M\b",
            lambda m: str(float(m.group(1)) * 1000000).rstrip("0").rstrip("."),
            line,
        )
        line = re.sub(
            r"(?i)(\d+(?:\.\d+)?)\s*B\b",
            lambda m: str(float(m.group(1)) * 1000000000).rstrip("0").rstrip("."),
            line,
        )

        # Remove currency symbols.
        line = re.sub(r"[$€£¥]", "", line)

        # Convert pipe or tab tables to CSV-like lines.
        if "|" in line and "," not in line:
            cells = [c.strip() for c in line.split("|") if c.strip()]
        elif "\t" in line and "," not in line:
            cells = [c.strip() for c in line.split("\t") if c.strip()]
        else:
            try:
                cells = next(csv.reader([line]))
                cells = [c.strip() for c in cells]
            except Exception:
                cells = [line]

        if not cells:
            continue

        cleaned_lines.append(cells)

    if not cleaned_lines:
        return ""

    # Pick a stable column count.
    length_counts = {}
    for row in cleaned_lines:
        length_counts[len(row)] = length_counts.get(len(row), 0) + 1

    # Prefer the most common non-1 column length.
    target_len = max(length_counts, key=length_counts.get)
    if target_len == 1:
        multi_lengths = [l for l in length_counts if l > 1]
        if multi_lengths:
            target_len = max(multi_lengths, key=lambda l: length_counts[l])

    normalized_rows = []

    for row in cleaned_lines:
        if len(row) == target_len:
            normalized_rows.append(row)
        elif len(row) > target_len:
            normalized_rows.append(row[:target_len])
        elif 1 < len(row) < target_len:
            normalized_rows.append(row + [""] * (target_len - len(row)))

    if not normalized_rows:
        normalized_rows = cleaned_lines

    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerows(normalized_rows)

    return out.getvalue().strip()


def clean_summary(raw: str, config: dict) -> str:
    """
    Clean summary output.
    """
    text = (raw or "").strip()

    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = text.replace("```", "")
    text = re.sub(r"(?i)^summary\s*:\s*", "", text).strip()

    return " ".join(text.split())