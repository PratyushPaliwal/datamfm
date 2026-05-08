"""
Track 1 — Document Parsing Pipeline
Usage:
    python track1/pipeline/run.py \
        --input_dir data/doc_pages \
        --output_dir submission/track1 \
        --config configs/track1.yaml
"""

import argparse
import os
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from dotenv import load_dotenv

from track1.pipeline.model_router import route_page
from track1.postprocess.cleaner import clean_markdown


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def process_page(image_path: Path, output_dir: Path, config: dict) -> dict:
    """Process a single page image → .md file."""
    out_folder = output_dir / image_path.parent.name
    out_folder.mkdir(parents=True, exist_ok=True)
    out_path = out_folder / (image_path.stem + ".md")

    if out_path.exists():
        return {"status": "skipped", "file": str(out_path)}

    try:
        raw_md = route_page(image_path, config)
        clean_md = clean_markdown(raw_md, config)
        out_path.write_text(clean_md, encoding="utf-8")
        return {"status": "ok", "file": str(out_path)}
    except Exception as e:
        error_md = f"<!-- ERROR processing {image_path.name}: {e} -->\n"
        out_path.write_text(error_md, encoding="utf-8")
        return {"status": "error", "file": str(out_path), "error": str(e)}


def main():
    load_dotenv("configs/secrets.env")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=Path, required=True)
    parser.add_argument("--output_dir", type=Path, required=True)
    parser.add_argument("--config", type=str, default="configs/track1.yaml")
    parser.add_argument("--workers", type=int, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    image_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    all_images = sorted([
        p for p in args.input_dir.rglob("*")
        if p.suffix.lower() in image_extensions
    ])

    if not all_images:
        print(f"No images found in {args.input_dir}")
        return

    print(f"Found {len(all_images)} page images across "
          f"{len(set(p.parent for p in all_images))} folders")

    max_workers = args.workers or config["pipeline"].get("max_workers", 4)
    results = {"ok": 0, "skipped": 0, "error": 0}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_page, img, args.output_dir, config): img
            for img in all_images
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Parsing pages"):
            result = future.result()
            results[result["status"]] += 1
            if result["status"] == "error":
                print(f"\n  Error on {futures[future].name}: {result.get('error')}")

    print(f"\nDone. OK: {results['ok']} | Skipped: {results['skipped']} | Errors: {results['error']}")
    print(f"Output: {args.output_dir}")


if __name__ == "__main__":
    main()
