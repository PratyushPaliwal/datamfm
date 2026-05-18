"""
Track 1 — Document Parsing Pipeline

Usage:
    python track1/pipeline/run.py \
        --input_dir data/doc_pages \
        --output_dir submission/track1 \
        --config configs/track1.yaml

Expected input:
    data/doc_pages/
    ├── document_001/
    │   ├── page_1.png
    │   ├── page_2.png
    │   └── page_3.png
    ├── document_002/
    │   ├── page_1.png
    │   └── page_2.png

Expected output:
    submission/track1/
    ├── document_001.md
    ├── document_002.md

So this script produces one flat Markdown file per document folder.
"""

import argparse
import re
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm
from dotenv import load_dotenv

from track1.pipeline.model_router import route_page
from track1.postprocess.cleaner import clean_markdown


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_config(config_path: str) -> dict:
    """
    Load YAML config file.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def natural_sort_key(path: Path):
    """
    Natural sorting for page names.

    Example:
        page_1.png
        page_2.png
        page_10.png

    instead of:
        page_1.png
        page_10.png
        page_2.png
    """
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]


def find_document_folders(input_dir: Path) -> list[Path]:
    """
    Find document folders.

    Case 1:
        input_dir contains folders, each folder is one document.

    Case 2:
        input_dir directly contains images.
        Then input_dir itself is treated as one document.
    """
    child_dirs = [
        p for p in input_dir.iterdir()
        if p.is_dir()
    ]

    document_folders = []

    for folder in sorted(child_dirs):
        images = [
            p for p in folder.rglob("*")
            if p.suffix.lower() in IMAGE_EXTENSIONS
        ]
        if images:
            document_folders.append(folder)

    # If no child folders contain images, check if input_dir itself has images.
    if not document_folders:
        root_images = [
            p for p in input_dir.rglob("*")
            if p.suffix.lower() in IMAGE_EXTENSIONS
        ]
        if root_images:
            document_folders.append(input_dir)

    return document_folders


def get_images_for_document(document_folder: Path) -> list[Path]:
    """
    Get all page images for one document folder, sorted in page order.
    """
    images = [
        p for p in document_folder.rglob("*")
        if p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    return sorted(images, key=natural_sort_key)


def process_document(document_folder: Path, input_dir: Path, output_dir: Path, config: dict) -> dict:
    """
    Process one document folder.

    It parses every page image, cleans the Markdown, combines all pages,
    and writes one flat document-level .md file.
    """
    document_id = document_folder.name

    # If input_dir itself is treated as the document, use input_dir name.
    if document_folder == input_dir:
        document_id = input_dir.name

    out_path = output_dir / f"{document_id}.md"

    if out_path.exists():
        return {
            "status": "skipped",
            "document": document_id,
            "file": str(out_path),
        }

    images = get_images_for_document(document_folder)

    if not images:
        return {
            "status": "error",
            "document": document_id,
            "file": str(out_path),
            "error": "No page images found.",
        }

    try:
        page_markdowns = []

        for page_index, image_path in enumerate(images, start=1):
            raw_md = route_page(image_path, config)
            clean_md = clean_markdown(raw_md, config)

            if clean_md.strip():
                page_markdowns.append(clean_md.strip())

        final_md = "\n\n".join(page_markdowns).strip() + "\n"

        out_path.write_text(final_md, encoding="utf-8")

        return {
            "status": "ok",
            "document": document_id,
            "file": str(out_path),
            "pages": len(images),
        }

    except Exception as e:
        error_md = (
            f"<!-- ERROR processing document {document_id}: {e} -->\n"
        )
        out_path.write_text(error_md, encoding="utf-8")

        return {
            "status": "error",
            "document": document_id,
            "file": str(out_path),
            "error": str(e),
        }


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

    document_folders = find_document_folders(args.input_dir)

    if not document_folders:
        print(f"No document folders or images found in {args.input_dir}")
        return

    total_pages = sum(
        len(get_images_for_document(folder))
        for folder in document_folders
    )

    print(
        f"Found {len(document_folders)} documents "
        f"with {total_pages} page images."
    )

    max_workers = args.workers or config.get("pipeline", {}).get("max_workers", 2)

    results = {
        "ok": 0,
        "skipped": 0,
        "error": 0,
    }

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                process_document,
                doc_folder,
                args.input_dir,
                args.output_dir,
                config,
            ): doc_folder
            for doc_folder in document_folders
        }

        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc="Parsing documents",
        ):
            result = future.result()
            results[result["status"]] += 1

            if result["status"] == "error":
                print(
                    f"\nError on {result['document']}: "
                    f"{result.get('error')}"
                )

    print(
        f"\nDone. "
        f"OK: {results['ok']} | "
        f"Skipped: {results['skipped']} | "
        f"Errors: {results['error']}"
    )
    print(f"Output: {args.output_dir}")


if __name__ == "__main__":
    main()