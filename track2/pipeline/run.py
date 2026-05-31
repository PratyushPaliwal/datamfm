"""
Track 2 — Chart Understanding Pipeline (optimised)

Two-step architecture:
  Step 1: image → CSV
  Step 2: image + CSV → grounded summary

Output format exactly matches challenge submission spec:
  real/chart2csv_predictions.jsonl
  real/chart2summary_predictions.jsonl
  synthetic/chart2csv_predictions.jsonl
  synthetic/chart2summary_predictions.jsonl

Usage:
    python -m track2.pipeline.run \
        --input_dir /path/to/charts \
        --output_dir submission/track2 \
        --split real \
        --limit 5
"""

import argparse
import json
import os
import time
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from dotenv import load_dotenv

from track2.pipeline.model_runner import extract_csv, generate_summary
from track2.postprocess.cleaner import clean_csv, clean_summary, verify_numbers_in_summary


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def find_images_dir(base: Path, split: str) -> Path | None:
    """Auto-detect where images actually live."""
    image_ext = {".jpg", ".jpeg", ".png", ".webp"}

    def has_images(d: Path) -> bool:
        return d.exists() and any(
            f.suffix.lower() in image_ext
            for f in d.iterdir() if f.is_file()
        )

    for candidate in [base / split, base / split / "images",
                      base / "images", base]:
        if has_images(candidate):
            return candidate
    return None


def process_chart(image_path: Path, config: dict) -> dict:
    """
    Two-step processing per chart:
    1. Extract CSV from image
    2. Generate grounded summary using image + CSV
    """
    try:
        # Step 1 — CSV extraction
        raw_csv = extract_csv(image_path, config)
        clean_csv_text = clean_csv(raw_csv, config)

        # Step 2 — Grounded summary (uses CSV for numeric accuracy)
        raw_summary = generate_summary(image_path, config,
                                       csv_text=clean_csv_text)
        clean_summary_text = clean_summary(raw_summary, config)

        # Quality check — how many CSV numbers appear in summary
        quality = verify_numbers_in_summary(clean_summary_text, clean_csv_text)

        return {
            "imagename": image_path.name,
            "predicted_csv": clean_csv_text,
            "predicted_summary": clean_summary_text,
            "status": "ok",
            "numeric_coverage": quality["coverage"],
        }
    except Exception as e:
        return {
            "imagename": image_path.name,
            "predicted_csv": "",
            "predicted_summary": "",
            "status": "error",
            "error": str(e),
        }


def run_split(split_dir: Path, split_name: str, output_dir: Path,
              config: dict, limit: int = None, verbose: bool = False):
    out_dir = output_dir / split_name
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path     = out_dir / "chart2csv_predictions.jsonl"
    summary_path = out_dir / "chart2summary_predictions.jsonl"

    image_ext = {".jpg", ".jpeg", ".png", ".webp"}
    images = sorted([p for p in split_dir.iterdir()
                     if p.suffix.lower() in image_ext])

    # Resume support
    done_csv, done_sum = set(), set()
    if csv_path.exists():
        with open(csv_path) as f:
            done_csv = {json.loads(l)["imagename"] for l in f if l.strip()}
    if summary_path.exists():
        with open(summary_path) as f:
            done_sum = {json.loads(l)["imagename"] for l in f if l.strip()}

    todo = [img for img in images
            if img.name not in done_csv or img.name not in done_sum]
    if limit:
        todo = todo[:limit]

    if not todo:
        print(f"  {split_name}: all done, skipping.")
        return

    print(f"\n  {split_name}: {len(todo)} images to process")
    print(f"  Images dir: {split_dir}")

    max_workers = config["pipeline"].get("max_workers", 1)
    errors = 0
    low_coverage = 0
    start = time.time()

    with open(csv_path, "a") as csv_f, open(summary_path, "a") as sum_f:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_chart, img, config): img
                       for img in todo}

            for i, future in enumerate(tqdm(
                    as_completed(futures), total=len(futures),
                    desc=f"  {split_name}")):
                result = future.result()
                name = result["imagename"]

                if name not in done_csv:
                    csv_f.write(json.dumps({
                        "imagename": name,
                        "predicted_csv": result["predicted_csv"],
                    }) + "\n")
                    csv_f.flush()

                if name not in done_sum:
                    sum_f.write(json.dumps({
                        "imagename": name,
                        "predicted_summary": result["predicted_summary"],
                    }) + "\n")
                    sum_f.flush()

                if result["status"] == "error":
                    errors += 1
                    if verbose:
                        print(f"\n  ERROR {name}: {result.get('error','')[:80]}")

                # Warn on low numeric coverage
                cov = result.get("numeric_coverage", 1.0)
                if cov < 0.5 and result["status"] == "ok":
                    low_coverage += 1
                    if verbose:
                        print(f"\n  LOW COVERAGE ({cov:.0%}) {name}")

    elapsed = time.time() - start
    rate = len(todo) / elapsed if elapsed > 0 else 0
    print(f"\n  Done: {len(todo)} imgs in {elapsed/60:.1f}min "
          f"({rate:.1f} img/s) | errors: {errors} | low_coverage: {low_coverage}")


def main():
    load_dotenv("configs/secrets.env")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir",  type=Path, required=True)
    parser.add_argument("--output_dir", type=Path, required=True)
    parser.add_argument("--config",     type=str,
                        default="configs/track2.yaml")
    parser.add_argument("--split",      type=str, default=None,
                        help="real | synthetic | both (default: both)")
    parser.add_argument("--limit",      type=int, default=None)
    parser.add_argument("--workers",    type=int, default=None)
    parser.add_argument("--verbose",    action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.workers:
        config["pipeline"]["max_workers"] = args.workers

    splits = [args.split] if args.split and args.split != "both" \
        else config["pipeline"].get("splits", ["real", "synthetic"])

    for split in splits:
        images_dir = find_images_dir(args.input_dir, split)
        if images_dir is None:
            print(f"Could not find images for '{split}' under {args.input_dir}")
            continue
        print(f"\nProcessing: {split}"
              + (f" [limit={args.limit}]" if args.limit else ""))
        run_split(images_dir, split, args.output_dir, config,
                  limit=args.limit, verbose=args.verbose)

    print(f"\nAll done. Output: {args.output_dir}")


if __name__ == "__main__":
    main()
