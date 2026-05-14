"""
Local scorer for Track 2 — Chart Understanding.

Computes all 4 official metrics against ground-truth JSONL files:
  - CSV Numeric F1
  - CSV Structural Score
  - Summary ROUGE-L
  - Summary Numeric Fact F1

Usage:
    python evaluation/score_track2.py \
        --predictions  submission/track2_sample \
        --ground_truth data/charts_gt \
        --split        real

Ground-truth JSONL format (same keys as predictions):
    {"imagename": "chart1.png", "gt_csv": "Year,Value\n2020,100", "gt_summary": "The bar chart..."}

If you don't have ground truth yet, run with --show_only to just print
your predictions and visually inspect them.
"""

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path
from collections import defaultdict


# ─── CSV metrics ────────────────────────────────────────────────────────────

def extract_numbers(text: str) -> list[float]:
    """Pull all numbers out of a string, handling CSV comma separators."""
    # Replace commas that are CSV delimiters (between non-digit chars) with spaces
    # but keep commas that are part of numbers like 1,247
    cleaned = re.sub(r"(?<!\d),(?!\d)", " ", text)
    raw = re.findall(r"-?\d+(?:\.\d+)?", cleaned)
    nums = []
    for r in raw:
        try:
            nums.append(float(r))
        except ValueError:
            pass
    return nums


def numbers_match(a: float, b: float, tol: float = 0.01) -> bool:
    """Two numbers match if they're within 1% of each other."""
    if b == 0:
        return a == 0
    return abs(a - b) / abs(b) <= tol


def csv_numeric_f1(pred_csv: str, gt_csv: str) -> float:
    """
    F1 on numeric values. Each number in GT must be matched by a number in pred.
    Tolerance: 1%.
    """
    pred_nums = extract_numbers(pred_csv)
    gt_nums   = extract_numbers(gt_csv)

    if not gt_nums:
        return 1.0 if not pred_nums else 0.0

    gt_matched   = [False] * len(gt_nums)
    pred_matched = [False] * len(pred_nums)

    for i, g in enumerate(gt_nums):
        for j, p in enumerate(pred_nums):
            if not pred_matched[j] and numbers_match(p, g):
                gt_matched[i]   = True
                pred_matched[j] = True
                break

    tp = sum(gt_matched)
    precision = tp / len(pred_nums) if pred_nums else 0.0
    recall    = tp / len(gt_nums)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def csv_structural_score(pred_csv: str, gt_csv: str) -> float:
    """
    Score based on structural match: correct number of columns, rows,
    and header names.
    """
    def parse(text):
        try:
            rows = list(csv.reader(io.StringIO(text.strip())))
            return rows
        except Exception:
            return []

    pred_rows = parse(pred_csv)
    gt_rows   = parse(gt_csv)

    if not gt_rows:
        return 1.0 if not pred_rows else 0.0
    if not pred_rows:
        return 0.0

    score = 0.0

    # Column count match (40% weight)
    gt_cols   = len(gt_rows[0])
    pred_cols = len(pred_rows[0]) if pred_rows else 0
    score += 0.4 * (1.0 if gt_cols == pred_cols else max(0, 1 - abs(gt_cols - pred_cols) / gt_cols))

    # Row count match (30% weight)
    gt_data_rows   = len(gt_rows) - 1
    pred_data_rows = len(pred_rows) - 1 if len(pred_rows) > 1 else 0
    if gt_data_rows > 0:
        score += 0.3 * max(0, 1 - abs(gt_data_rows - pred_data_rows) / gt_data_rows)
    else:
        score += 0.3

    # Header overlap (30% weight)
    if gt_rows and pred_rows:
        gt_headers   = {h.strip().lower() for h in gt_rows[0]}
        pred_headers = {h.strip().lower() for h in pred_rows[0]}
        if gt_headers:
            overlap = len(gt_headers & pred_headers) / len(gt_headers)
            score += 0.3 * overlap

    return round(score, 4)


# ─── Summary metrics ─────────────────────────────────────────────────────────

def lcs_length(a: list, b: list) -> int:
    """Longest common subsequence length."""
    if not a or not b:
        return 0
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(2)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i % 2][j] = dp[(i-1) % 2][j-1] + 1
            else:
                dp[i % 2][j] = max(dp[(i-1) % 2][j], dp[i % 2][j-1])
    return dp[m % 2][n]


def rouge_l(pred: str, gt: str) -> float:
    """ROUGE-L F1 score."""
    pred_tokens = pred.lower().split()
    gt_tokens   = gt.lower().split()
    if not gt_tokens:
        return 1.0 if not pred_tokens else 0.0
    if not pred_tokens:
        return 0.0
    lcs = lcs_length(pred_tokens, gt_tokens)
    precision = lcs / len(pred_tokens)
    recall    = lcs / len(gt_tokens)
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 4)


def numeric_fact_f1(pred: str, gt: str) -> float:
    """F1 on numbers appearing in the summary text."""
    return csv_numeric_f1(pred, gt)


# ─── Loading helpers ─────────────────────────────────────────────────────────

def load_jsonl(path: Path) -> dict[str, dict]:
    """Load a JSONL file as {imagename: record}."""
    records = {}
    if not path.exists():
        return records
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                records[obj["imagename"]] = obj
            except Exception as e:
                print(f"  Warning: skipping malformed line in {path.name}: {e}")
    return records


# ─── Main ────────────────────────────────────────────────────────────────────

def score_split(pred_dir: Path, gt_dir: Path, split: str, show_only: bool = False):
    pred_csv_path     = pred_dir / split / "chart2csv_predictions.jsonl"
    pred_summary_path = pred_dir / split / "chart2summary_predictions.jsonl"
    gt_path           = gt_dir / split / "ground_truth.jsonl"

    pred_csv     = load_jsonl(pred_csv_path)
    pred_summary = load_jsonl(pred_summary_path)
    gt           = load_jsonl(gt_path) if not show_only else {}

    if not pred_csv and not pred_summary:
        print(f"  No predictions found in {pred_dir / split}")
        return None

    all_images = sorted(set(list(pred_csv.keys()) + list(pred_summary.keys())))
    print(f"\n{'='*60}")
    print(f"Split: {split}  |  Images: {len(all_images)}")
    print(f"{'='*60}")

    if show_only:
        # Just print predictions for visual inspection
        for img in all_images[:10]:
            print(f"\n--- {img} ---")
            if img in pred_csv:
                csv_val = pred_csv[img].get("predicted_csv", "")
                print(f"CSV ({len(csv_val.splitlines())} rows):\n{csv_val[:300]}")
            if img in pred_summary:
                print(f"\nSummary:\n{pred_summary[img].get('predicted_summary', '')}")
        if len(all_images) > 10:
            print(f"\n... and {len(all_images) - 10} more images")
        return None

    # Score against ground truth
    metrics = defaultdict(list)
    results = []

    for img in all_images:
        if img not in gt:
            continue

        gt_rec  = gt[img]
        gt_csv_text  = gt_rec.get("gt_csv", "")
        gt_sum_text  = gt_rec.get("gt_summary", "")

        pred_csv_text = pred_csv.get(img, {}).get("predicted_csv", "")
        pred_sum_text = pred_summary.get(img, {}).get("predicted_summary", "")

        m_csv_num    = csv_numeric_f1(pred_csv_text, gt_csv_text)
        m_csv_struct = csv_structural_score(pred_csv_text, gt_csv_text)
        m_rouge      = rouge_l(pred_sum_text, gt_sum_text)
        m_num_fact   = numeric_fact_f1(pred_sum_text, gt_sum_text)
        m_overall    = (m_csv_num + m_csv_struct + m_rouge + m_num_fact) / 4

        metrics["csv_numeric_f1"].append(m_csv_num)
        metrics["csv_structural"].append(m_csv_struct)
        metrics["rouge_l"].append(m_rouge)
        metrics["numeric_fact_f1"].append(m_num_fact)
        metrics["overall"].append(m_overall)

        results.append({
            "image": img,
            "csv_numeric_f1": round(m_csv_num, 3),
            "csv_structural": round(m_csv_struct, 3),
            "rouge_l": round(m_rouge, 3),
            "numeric_fact_f1": round(m_num_fact, 3),
            "overall": round(m_overall, 3),
        })

    if not results:
        print("  No images matched between predictions and ground truth.")
        print("  Check that imagenames in your JSONL match the GT file.")
        return None

    # Print per-image table
    print(f"\n{'Image':<35} {'CSV-F1':>7} {'Struct':>7} {'ROUGE':>7} {'NumFact':>8} {'Overall':>8}")
    print("-" * 78)
    for r in results:
        name = r["image"][:33]
        print(f"{name:<35} {r['csv_numeric_f1']:>7.3f} {r['csv_structural']:>7.3f} "
              f"{r['rouge_l']:>7.3f} {r['numeric_fact_f1']:>8.3f} {r['overall']:>8.3f}")

    # Averages
    def avg(key): return sum(metrics[key]) / len(metrics[key])

    print("\n" + "=" * 78)
    print(f"{'AVERAGE':<35} {avg('csv_numeric_f1'):>7.3f} {avg('csv_structural'):>7.3f} "
          f"{avg('rouge_l'):>7.3f} {avg('numeric_fact_f1'):>8.3f} {avg('overall'):>8.3f}")
    print("=" * 78)

    print(f"""
Summary ({split}):
  CSV Numeric F1      : {avg('csv_numeric_f1'):.4f}   (are the numbers right?)
  CSV Structural      : {avg('csv_structural'):.4f}   (right rows/cols/headers?)
  Summary ROUGE-L     : {avg('rouge_l'):.4f}   (text overlap with reference)
  Numeric Fact F1     : {avg('numeric_fact_f1'):.4f}   (numbers in summary correct?)
  ─────────────────────────────
  Overall             : {avg('overall'):.4f}
""")
    return {k: avg(k) for k in metrics}


def main():
    parser = argparse.ArgumentParser(description="Score Track 2 predictions locally")
    parser.add_argument("--predictions",  type=Path, required=True,
                        help="Dir containing real/ and synthetic/ JSONL files")
    parser.add_argument("--ground_truth", type=Path, default=None,
                        help="Dir containing GT JSONL files (optional — omit to use --show_only)")
    parser.add_argument("--split", type=str, default=None,
                        help="Score only this split: real | synthetic")
    parser.add_argument("--show_only", action="store_true",
                        help="Print predictions without scoring (no GT needed)")
    args = parser.parse_args()

    if args.show_only or args.ground_truth is None:
        splits = [args.split] if args.split else ["real", "synthetic"]
        for split in splits:
            score_split(args.predictions, Path("."), split, show_only=True)
        return

    splits = [args.split] if args.split else ["real", "synthetic"]
    all_scores = {}
    for split in splits:
        scores = score_split(args.predictions, args.ground_truth, split)
        if scores:
            all_scores[split] = scores

    if len(all_scores) > 1:
        print("\n=== Combined average across splits ===")
        keys = list(next(iter(all_scores.values())).keys())
        for k in keys:
            avg = sum(s[k] for s in all_scores.values()) / len(all_scores)
            print(f"  {k:<25}: {avg:.4f}")


if __name__ == "__main__":
    main()
