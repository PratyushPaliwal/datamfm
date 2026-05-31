"""
Local scorer for Track 2 — uses actual GT format from challenge.

GT format (from ground_truth_sample_partial):
  CSV:     {"imagename": "...", "csv": "..."}        ← key is "csv" not "gt_csv"
  Summary: {"imagename": "...", "summary": "..."}    ← key is "summary" not "gt_summary"

Prediction format:
  CSV:     {"imagename": "...", "predicted_csv": "..."}
  Summary: {"imagename": "...", "predicted_summary": "..."}

Usage:
    # Score against provided GT samples
    python -m evaluation.score_track2 \
        --predictions submission/track2_sample \
        --ground_truth datamfm_submission_format_examples/chart_understanding/ground_truth_sample_partial \
        --split real

    # Inspect predictions only (no GT needed)
    python -m evaluation.score_track2 \
        --predictions submission/track2_sample \
        --split real \
        --show_only
"""

import argparse
import csv
import io
import json
import re
from pathlib import Path
from collections import defaultdict


# ── Metric implementations ───────────────────────────────────────────────────

def extract_numbers(text: str) -> list[float]:
    """Extract numbers handling CSV commas correctly."""
    cleaned = re.sub(r'(?<!\d),(?!\d)', ' ', text)
    nums = []
    for r in re.findall(r'-?\d+\.?\d*', cleaned):
        try:
            nums.append(float(r))
        except ValueError:
            pass
    return nums


def numbers_match(a: float, b: float, tol: float = 0.01) -> bool:
    if b == 0:
        return abs(a) < 1e-9
    return abs(a - b) / abs(b) <= tol


def csv_numeric_f1(pred: str, gt: str) -> float:
    pred_nums = extract_numbers(pred)
    gt_nums   = extract_numbers(gt)
    if not gt_nums:
        return 1.0 if not pred_nums else 0.0
    gt_matched   = [False] * len(gt_nums)
    pred_matched = [False] * len(pred_nums)
    for i, g in enumerate(gt_nums):
        for j, p in enumerate(pred_nums):
            if not pred_matched[j] and numbers_match(p, g):
                gt_matched[i] = pred_matched[j] = True
                break
    tp = sum(gt_matched)
    precision = tp / len(pred_nums) if pred_nums else 0.0
    recall    = tp / len(gt_nums)
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 4)


def csv_structural_score(pred: str, gt: str) -> float:
    def parse(text):
        try:
            return list(csv.reader(io.StringIO(text.strip())))
        except Exception:
            return []

    pred_rows = parse(pred)
    gt_rows   = parse(gt)

    if not gt_rows:
        return 1.0 if not pred_rows else 0.0
    if not pred_rows:
        return 0.0

    score = 0.0
    gt_cols   = len(gt_rows[0])
    pred_cols = len(pred_rows[0]) if pred_rows else 0
    score += 0.4 * (1.0 if gt_cols == pred_cols
                    else max(0, 1 - abs(gt_cols - pred_cols) / gt_cols))

    gt_rows_n   = max(len(gt_rows) - 1, 1)
    pred_rows_n = max(len(pred_rows) - 1, 0)
    score += 0.3 * max(0, 1 - abs(gt_rows_n - pred_rows_n) / gt_rows_n)

    if gt_rows and pred_rows:
        gt_h   = {h.strip().lower() for h in gt_rows[0]}
        pred_h = {h.strip().lower() for h in pred_rows[0]}
        if gt_h:
            score += 0.3 * len(gt_h & pred_h) / len(gt_h)

    return round(score, 4)


def lcs(a: list, b: list) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(2)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i%2][j] = dp[(i-1)%2][j-1] + 1
            else:
                dp[i%2][j] = max(dp[(i-1)%2][j], dp[i%2][j-1])
    return dp[m%2][n]


def rouge_l(pred: str, gt: str) -> float:
    pt = pred.lower().split()
    gt_t = gt.lower().split()
    if not gt_t:
        return 1.0 if not pt else 0.0
    if not pt:
        return 0.0
    l = lcs(pt, gt_t)
    p = l / len(pt)
    r = l / len(gt_t)
    if p + r == 0:
        return 0.0
    return round(2 * p * r / (p + r), 4)


def numeric_fact_f1(pred: str, gt: str) -> float:
    return csv_numeric_f1(pred, gt)


# ── Loaders ──────────────────────────────────────────────────────────────────

def load_jsonl(path: Path, value_key: str) -> dict[str, str]:
    """Load JSONL, return {imagename: value}. Handles multiple key aliases."""
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
                name = (obj.get("imagename") or obj.get("image_name")
                        or obj.get("filename") or obj.get("id", ""))
                # Try multiple key aliases for the value
                aliases = [value_key, "prediction", "output",
                           "csv", "summary", "predicted_csv",
                           "predicted_summary"]
                val = next((obj[k] for k in aliases if k in obj), "")
                records[name] = val
            except Exception:
                pass
    return records


# ── Scoring ──────────────────────────────────────────────────────────────────

def score_split(pred_dir: Path, gt_dir: Path, split: str,
                show_only: bool = False):
    pred_csv_path = pred_dir / split / "chart2csv_predictions.jsonl"
    pred_sum_path = pred_dir / split / "chart2summary_predictions.jsonl"
    gt_csv_path   = gt_dir  / split / "chart2csv_gt_sample.jsonl"
    gt_sum_path   = gt_dir  / split / "chart2summary_gt_sample.jsonl"

    pred_csvs  = load_jsonl(pred_csv_path,  "predicted_csv")
    pred_sums  = load_jsonl(pred_sum_path,  "predicted_summary")
    gt_csvs    = load_jsonl(gt_csv_path,    "csv")
    gt_sums    = load_jsonl(gt_sum_path,    "summary")

    all_images = sorted(set(list(pred_csvs.keys()) + list(pred_sums.keys())))
    if not all_images:
        print(f"  No predictions found in {pred_dir / split}")
        return None

    print(f"\n{'='*65}")
    print(f"Split: {split}  |  Predictions: {len(all_images)}")
    print(f"GT available: CSV={len(gt_csvs)}  Summary={len(gt_sums)}")
    print(f"{'='*65}")

    if show_only:
        for img in all_images[:5]:
            print(f"\n--- {img} ---")
            csv_val = pred_csvs.get(img, "")
            print(f"CSV ({len(csv_val.splitlines())} rows):\n{csv_val[:300]}")
            sum_val = pred_sums.get(img, "")
            print(f"\nSummary ({len(sum_val.split())} words):\n{sum_val[:400]}")
        if len(all_images) > 5:
            print(f"\n... and {len(all_images)-5} more")
        return None

    # Score against GT
    metrics = defaultdict(list)
    results = []
    no_gt = 0

    for img in all_images:
        if img not in gt_csvs and img not in gt_sums:
            no_gt += 1
            continue

        pc = pred_csvs.get(img, "")
        ps = pred_sums.get(img, "")
        gc = gt_csvs.get(img, "")
        gs = gt_sums.get(img, "")

        m1 = csv_numeric_f1(pc, gc)     if gc else None
        m2 = csv_structural_score(pc, gc) if gc else None
        m3 = rouge_l(ps, gs)            if gs else None
        m4 = numeric_fact_f1(ps, gs)    if gs else None

        scored = [m for m in [m1, m2, m3, m4] if m is not None]
        overall = sum(scored) / len(scored) if scored else 0.0

        if m1 is not None: metrics["csv_numeric_f1"].append(m1)
        if m2 is not None: metrics["csv_structural"].append(m2)
        if m3 is not None: metrics["rouge_l"].append(m3)
        if m4 is not None: metrics["numeric_fact_f1"].append(m4)
        metrics["overall"].append(overall)

        results.append({
            "image": img,
            "csv_f1": round(m1, 3) if m1 is not None else "-",
            "struct": round(m2, 3) if m2 is not None else "-",
            "rouge":  round(m3, 3) if m3 is not None else "-",
            "numfact":round(m4, 3) if m4 is not None else "-",
            "overall":round(overall, 3),
        })

    if no_gt:
        print(f"  (skipped {no_gt} images with no GT match)")

    if not results:
        print("  No images matched GT. Check imagenames align.")
        return None

    print(f"\n{'Image':<36} {'CSV-F1':>7} {'Struct':>7} "
          f"{'ROUGE':>7} {'NumFact':>8} {'Overall':>8}")
    print("-" * 78)
    for r in results:
        print(f"{r['image'][:35]:<36} {str(r['csv_f1']):>7} "
              f"{str(r['struct']):>7} {str(r['rouge']):>7} "
              f"{str(r['numfact']):>8} {str(r['overall']):>8}")

    def avg(k): return sum(metrics[k]) / len(metrics[k]) if metrics[k] else 0

    print(f"\n{'='*78}")
    print(f"{'AVERAGE':<36} {avg('csv_numeric_f1'):>7.3f} "
          f"{avg('csv_structural'):>7.3f} {avg('rouge_l'):>7.3f} "
          f"{avg('numeric_fact_f1'):>8.3f} {avg('overall'):>8.3f}")
    print(f"{'='*78}")

    print(f"""
Scores ({split}):
  CSV Numeric F1    : {avg('csv_numeric_f1'):.4f}
  CSV Structural    : {avg('csv_structural'):.4f}
  Summary ROUGE-L   : {avg('rouge_l'):.4f}
  Numeric Fact F1   : {avg('numeric_fact_f1'):.4f}
  Overall           : {avg('overall'):.4f}
""")
    return {k: avg(k) for k in metrics}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions",  type=Path, required=True)
    parser.add_argument("--ground_truth", type=Path, default=None)
    parser.add_argument("--split",        type=str,  default=None)
    parser.add_argument("--show_only",    action="store_true")
    args = parser.parse_args()

    splits = [args.split] if args.split else ["real", "synthetic"]

    if args.show_only or args.ground_truth is None:
        for split in splits:
            score_split(args.predictions, Path("."), split, show_only=True)
        return

    all_scores = {}
    for split in splits:
        s = score_split(args.predictions, args.ground_truth, split)
        if s:
            all_scores[split] = s

    if len(all_scores) > 1:
        keys = list(next(iter(all_scores.values())).keys())
        print("\n=== Combined average ===")
        for k in keys:
            avg = sum(s[k] for s in all_scores.values()) / len(all_scores)
            print(f"  {k:<25}: {avg:.4f}")


if __name__ == "__main__":
    main()
