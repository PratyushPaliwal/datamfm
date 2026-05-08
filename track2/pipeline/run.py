"""
Track 2 — Chart Understanding Pipeline
Usage:
    python track2/pipeline/run.py \
        --input_dir data/charts \
        --output_dir submission/track2 \
        --config configs/track2.yaml
"""

import argparse
import json
import os
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from dotenv import load_dotenv

from track2.pipeline.model_runner import extract_csv, generate_summary
from track2.postprocess.cleaner import clean_csv, clean_summary


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def process_chart(image_path: Path, config: dict) -> dict:
    """Process one chart image → (csv_result, summary_result)."""
    try:
        raw_csv = extract_csv(image_path, config)
        raw_summary = generate_summary(image_path, config)

        csv_out = clean_csv(raw_csv, config)
        summary_out = clean_summary(raw_summary, config)

        return {
            "imagename": image_path.name,
            "predicted_csv": csv_out,
            "predicted_summary": summary_out,
            "status": "ok",
        }
    except Exception as e:
        return {
            "imagename": image_path.name,
            "predicted_csv": "",
            "predicted_summary": f"ERROR: {e}",
            "status": "error",
            "error": str(e),
        }


def run_split(split_dir: Path, output_dir: Path, config: dict):
    split_name = split_dir.name
    out_split_dir = output_dir / split_name
    out_split_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_split_dir / config["output"]["csv_file"]
    summary_path = out_split_dir / config["output"]["summary_file"]

    image_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    images = sorted([p for p in split_dir.iterdir()
                     if p.suffix.lower() in image_extensions])

    # Resume support — skip already processed images
    done_csv, done_summary = set(), set()
    if csv_path.exists():
        with open(csv_path) as f:
            done_csv = {json.loads(l)["imagename"] for l in f if l.strip()}
    if summary_path.exists():
        with open(summary_path) as f:
            done_summary = {json.loads(l)["imagename"] for l in f if l.strip()}

    todo = [img for img in images
            if img.name not in done_csv or img.name not in done_summary]

    if not todo:
        print(f"  {split_name}: all {len(images)} images already processed, skipping.")
        return

    print(f"  {split_name}: {len(todo)} images to process ({len(images) - len(todo)} cached)")
    max_workers = config["pipeline"].get("max_workers", 4)

    with open(csv_path, "a") as csv_f, open(summary_path, "a") as sum_f:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_chart, img, config): img for img in todo}

            for future in tqdm(as_completed(futures), total=len(futures), desc=f"  {split_name}"):
                result = future.result()
                img_name = result["imagename"]

                if img_name not in done_csv:
                    csv_f.write(json.dumps({
                        "imagename": img_name,
                        "predicted_csv": result["predicted_csv"],
                    }) + "\n")
                    csv_f.flush()

                if img_name not in done_summary:
                    sum_f.write(json.dumps({
                        "imagename": img_name,
                        "predicted_summary": result["predicted_summary"],
                    }) + "\n")
                    sum_f.flush()

                if result["status"] == "error":
                    print(f"\n  Error on {img_name}: {result.get('error')}")


def main():
    load_dotenv("configs/secrets.env")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=Path, required=True)
    parser.add_argument("--output_dir", type=Path, required=True)
    parser.add_argument("--config", type=str, default="configs/track2.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    splits = config["pipeline"].get("splits", ["real", "synthetic"])
    for split in splits:
        split_dir = args.input_dir / split
        if not split_dir.exists():
            print(f"Split directory not found: {split_dir} — skipping")
            continue
        print(f"\nProcessing split: {split}")
        run_split(split_dir, args.output_dir, config)

    print(f"\nDone. Output: {args.output_dir}")


if __name__ == "__main__":
    main()
