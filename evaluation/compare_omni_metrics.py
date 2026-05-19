import re
from pathlib import Path
from difflib import SequenceMatcher
from html.parser import HTMLParser


PRED_DIR = Path("submission/track1_omni_test")
GT_DIR = Path("evaluation/omni_ground_truth_md")


def levenshtein(a: str, b: str) -> int:
    """
    Compute Levenshtein edit distance.
    """
    if a == b:
        return 0

    if len(a) < len(b):
        a, b = b, a

    previous = list(range(len(b) + 1))

    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            insert = current[j - 1] + 1
            delete = previous[j] + 1
            replace = previous[j - 1] + (ca != cb)
            current.append(min(insert, delete, replace))
        previous = current

    return previous[-1]


def normalized_edit_distance(pred: str, gt: str) -> float:
    """
    Text ED. Lower is better.
    """
    pred = normalize_text(pred)
    gt = normalize_text(gt)

    if not gt:
        return 0.0 if not pred else 1.0

    return levenshtein(pred, gt) / max(len(gt), 1)


def normalize_text(text: str) -> str:
    """
    Normalize text for fairer comparison.
    """
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)  # remove markdown images
    text = re.sub(r"<[^>]+>", " ", text)         # remove HTML tags
    text = re.sub(r"\$+", " ", text)             # remove formula delimiters
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_tables(md: str) -> list[str]:
    """
    Extract HTML table blocks.
    """
    return re.findall(r"<table.*?</table>", md, flags=re.DOTALL | re.IGNORECASE)


def extract_formulas(md: str) -> list[str]:
    """
    Extract display formulas inside $$...$$.
    """
    return re.findall(r"\$\$(.*?)\$\$", md, flags=re.DOTALL)


class SimpleHTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens = []

    def handle_starttag(self, tag, attrs):
        if tag in {"table", "tr", "td", "th"}:
            self.tokens.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in {"table", "tr", "td", "th"}:
            self.tokens.append(f"</{tag}>")

    def handle_data(self, data):
        data = data.strip()
        if data:
            self.tokens.append(data)


def table_to_tokens(table_html: str) -> str:
    """
    Convert table HTML into a token sequence.
    This is a simple approximation of TEDS.
    """
    parser = SimpleHTMLTextExtractor()
    parser.feed(table_html)
    return " ".join(parser.tokens)


def table_teds_approx(pred_md: str, gt_md: str) -> float:
    """
    Approximate Table TEDS. Higher is better.

    Official TEDS uses tree edit distance.
    This approximation compares simplified HTML tree/token sequences.
    """
    pred_tables = extract_tables(pred_md)
    gt_tables = extract_tables(gt_md)

    if not gt_tables:
        return 1.0 if not pred_tables else 0.0

    if not pred_tables:
        return 0.0

    scores = []

    for gt_table in gt_tables:
        gt_tokens = table_to_tokens(gt_table)

        best = 0.0
        for pred_table in pred_tables:
            pred_tokens = table_to_tokens(pred_table)
            score = SequenceMatcher(None, pred_tokens, gt_tokens).ratio()
            best = max(best, score)

        scores.append(best)

    return sum(scores) / len(scores)


def char_f1(pred: str, gt: str) -> float:
    """
    Character-level F1 used as an approximation for Formula CDM.
    Higher is better.
    """
    pred = re.sub(r"\s+", "", pred)
    gt = re.sub(r"\s+", "", gt)

    if not gt:
        return 1.0 if not pred else 0.0

    pred_chars = list(pred)
    gt_chars = list(gt)

    matched = 0
    used = [False] * len(gt_chars)

    for pc in pred_chars:
        for i, gc in enumerate(gt_chars):
            if not used[i] and pc == gc:
                matched += 1
                used[i] = True
                break

    precision = matched / len(pred_chars) if pred_chars else 0.0
    recall = matched / len(gt_chars) if gt_chars else 0.0

    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


def formula_cdm_approx(pred_md: str, gt_md: str) -> float:
    """
    Approximate Formula CDM. Higher is better.
    """
    pred_formulas = extract_formulas(pred_md)
    gt_formulas = extract_formulas(gt_md)

    if not gt_formulas:
        return 1.0 if not pred_formulas else 0.0

    if not pred_formulas:
        return 0.0

    scores = []

    for gt_formula in gt_formulas:
        best = 0.0
        for pred_formula in pred_formulas:
            best = max(best, char_f1(pred_formula, gt_formula))
        scores.append(best)

    return sum(scores) / len(scores)


def markdown_blocks(md: str) -> list[str]:
    """
    Split Markdown into rough reading-order blocks.
    """
    md = re.sub(r"!\[.*?\]\(.*?\)", "", md)
    blocks = re.split(r"\n\s*\n", md)

    clean_blocks = []
    for block in blocks:
        block = normalize_text(block)
        if block:
            clean_blocks.append(block[:80])

    return clean_blocks


def reading_order_approx(pred_md: str, gt_md: str) -> float:
    """
    Approximate reading order score. Higher is better.

    Compares the sequence of extracted Markdown blocks.
    """
    pred_blocks = markdown_blocks(pred_md)
    gt_blocks = markdown_blocks(gt_md)

    if not gt_blocks:
        return 1.0 if not pred_blocks else 0.0

    return SequenceMatcher(None, pred_blocks, gt_blocks).ratio()


def evaluate_file(pred_file: Path, gt_file: Path) -> dict:
    pred_md = pred_file.read_text(encoding="utf-8")
    gt_md = gt_file.read_text(encoding="utf-8")

    return {
        "file": pred_file.name,
        "text_ed": normalized_edit_distance(pred_md, gt_md),
        "table_teds": table_teds_approx(pred_md, gt_md),
        "formula_cdm": formula_cdm_approx(pred_md, gt_md),
        "reading_order": reading_order_approx(pred_md, gt_md),
        "pred_chars": len(pred_md),
        "gt_chars": len(gt_md),
        "pred_tables": len(extract_tables(pred_md)),
        "gt_tables": len(extract_tables(gt_md)),
        "pred_formulas": len(extract_formulas(pred_md)),
        "gt_formulas": len(extract_formulas(gt_md)),
    }


def main():
    pred_files = sorted(PRED_DIR.glob("*.md"))

    if not pred_files:
        raise RuntimeError(f"No prediction files found in {PRED_DIR}")

    rows = []

    for pred_file in pred_files:
        gt_file = GT_DIR / pred_file.name

        if not gt_file.exists():
            print(f"[MISSING GT] {pred_file.name}")
            continue

        row = evaluate_file(pred_file, gt_file)
        rows.append(row)

        print(
            f"{row['file']}: "
            f"TextED={row['text_ed']:.3f} ↓, "
            f"TableTEDS={row['table_teds']:.3f} ↑, "
            f"FormulaCDM={row['formula_cdm']:.3f} ↑, "
            f"ReadingOrder={row['reading_order']:.3f} ↑, "
            f"chars pred/gt={row['pred_chars']}/{row['gt_chars']}"
        )

    if not rows:
        return

    avg_text_ed = sum(r["text_ed"] for r in rows) / len(rows)
    avg_table_teds = sum(r["table_teds"] for r in rows) / len(rows)
    avg_formula_cdm = sum(r["formula_cdm"] for r in rows) / len(rows)
    avg_reading_order = sum(r["reading_order"] for r in rows) / len(rows)

    print("\nAverage:")
    print(f"Text ED:       {avg_text_ed:.3f} ↓")
    print(f"Table TEDS:    {avg_table_teds:.3f} ↑")
    print(f"Formula CDM:   {avg_formula_cdm:.3f} ↑")
    print(f"Reading Order: {avg_reading_order:.3f} ↑")


if __name__ == "__main__":
    main()