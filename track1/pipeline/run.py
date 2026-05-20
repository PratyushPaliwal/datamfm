"""
Track 1 — Document Parsing Pipeline

Usage for official challenge-style data:
    python -m track1.pipeline.run \
        --input_dir data/doc_pages \
        --output_dir submission/track1 \
        --config configs/track1.yaml

Usage for testing first 10 flat images:
    python -m track1.pipeline.run \
        --input_dir data/document_parsing_download/images \
        --output_dir submission/track1_test10 \
        --config configs/track1.yaml \
        --workers 1 \
        --limit 10 \
        --flat_images_as_docs

Expected official input:
    data/doc_pages/
    ├── document_001/
    │   ├── page_1.png
    │   ├── page_2.png
    │   └── page_3.png
    ├── document_002/
    │   ├── page_1.png
    │   └── page_2.png

Expected official output:
    submission/track1/
    ├── document_001.md
    ├── document_002.md

This script produces one flat Markdown file per document.
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
    Natural sorting for filenames.

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


def is_image(path: Path) -> bool:
    """
    Check whether a path is a supported image.
    """
    return path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS


def find_document_folders(input_dir: Path) -> list[Path]:
    """
    Find document folders.

    Official challenge case:
        input_dir contains folders, each folder is one document.

    Example:
        data/doc_pages/
        ├── uuid_1/
        │   ├── page_001.png
        │   └── page_002.png
        ├── uuid_2/
        │   └── page_001.png
    """
    child_dirs = [
        p for p in input_dir.iterdir()
        if p.is_dir()
    ]

    document_folders = []

    for folder in sorted(child_dirs, key=natural_sort_key):
        images = [
            p for p in folder.rglob("*")
            if is_image(p)
        ]
        if images:
            document_folders.append(folder)

    return document_folders


def find_flat_images(input_dir: Path) -> list[Path]:
    """
    Find images directly/recursively under input_dir.

    This is useful for testing when the dataset is just:
        images/
        ├── page_001.png
        ├── page_002.png
        └── ...
    """
    images = [
        p for p in input_dir.rglob("*")
        if is_image(p)
    ]

    return sorted(images, key=natural_sort_key)


def get_images_for_document(document_folder: Path) -> list[Path]:
    """
    Get all page images for one document folder, sorted in page order.
    """
    images = [
        p for p in document_folder.rglob("*")
        if is_image(p)
    ]

    return sorted(images, key=natural_sort_key)


def process_document_folder(
    document_folder: Path,
    output_dir: Path,
    config: dict,
) -> dict:
    """
    Process one document folder.

    It parses every page image, cleans the Markdown, combines all pages
    and writes one flat document-level .md file.
    """
    document_id = document_folder.name
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
        error_md = f"<!-- ERROR processing document {document_id}: {e} -->\n"
        out_path.write_text(error_md, encoding="utf-8")

        return {
            "status": "error",
            "document": document_id,
            "file": str(out_path),
            "error": str(e),
        }


def process_single_image_as_document(
    image_path: Path,
    output_dir: Path,
    config: dict,
) -> dict:
    """
    Process one standalone image as one document.

    This is useful for flat test datasets where each image should produce
    one Markdown file.
    """
    document_id = image_path.stem
    out_path = output_dir / f"{document_id}.md"

    if out_path.exists():
        return {
            "status": "skipped",
            "document": document_id,
            "file": str(out_path),
        }

    try:
        raw_md = route_page(image_path, config)
        clean_md = clean_markdown(raw_md, config)

        final_md = clean_md.strip() + "\n"
        out_path.write_text(final_md, encoding="utf-8")

        return {
            "status": "ok",
            "document": document_id,
            "file": str(out_path),
            "pages": 1,
        }

    except Exception as e:
        error_md = f"<!-- ERROR processing document {document_id}: {e} -->\n"
        out_path.write_text(error_md, encoding="utf-8")

        return {
            "status": "error",
            "document": document_id,
            "file": str(out_path),
            "error": str(e),
        }


def print_result_summary(results: dict, output_dir: Path):
    """
    Print final run summary.
    """
    print(
        f"\nDone. "
        f"OK: {results['ok']} | "
        f"Skipped: {results['skipped']} | "
        f"Errors: {results['error']}"
    )
    print(f"Output: {output_dir}")


def main():
    load_dotenv("configs/secrets.env")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=Path, required=True)
    parser.add_argument("--output_dir", type=Path, required=True)
    parser.add_argument("--config", type=str, default="configs/track1.yaml")
    parser.add_argument("--workers", type=int, default=None)

    # New: process only first N documents/images for quick tests.
    parser.add_argument("--limit", type=int, default=None)

    # New: treat each image as a separate document.
    # Use this for flat folders like data/document_parsing_download/images.
    parser.add_argument(
        "--flat_images_as_docs",
        action="store_true",
        help="Treat each image as one document. Useful for flat image folders.",
    )

    args = parser.parse_args()

    config = load_config(args.config)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    max_workers = args.workers or config.get("pipeline", {}).get("max_workers", 2)

    results = {
        "ok": 0,
        "skipped": 0,
        "error": 0,
    }

    if args.flat_images_as_docs:
        images = find_flat_images(args.input_dir)

        if not images:
            print(f"No images found in {args.input_dir}")
            return

        if args.limit is not None:
            images = images[:args.limit]

        print(f"Found {len(images)} standalone images.")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    process_single_image_as_document,
                    img,
                    args.output_dir,
                    config,
                ): img
                for img in images
            }

            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="Parsing images",
            ):
                result = future.result()
                results[result["status"]] += 1

                if result["status"] == "error":
                    print(
                        f"\nError on {result['document']}: "
                        f"{result.get('error')}"
                    )

        print_result_summary(results, args.output_dir)
        return

    document_folders = find_document_folders(args.input_dir)

    if not document_folders:
        print(f"No document folders found in {args.input_dir}")
        print(
            "If your input directory contains flat images directly, rerun with "
            "--flat_images_as_docs."
        )
        return

    if args.limit is not None:
        document_folders = document_folders[:args.limit]

    total_pages = sum(
        len(get_images_for_document(folder))
        for folder in document_folders
    )

    print(
        f"Found {len(document_folders)} documents "
        f"with {total_pages} page images."
    )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                process_document_folder,
                doc_folder,
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

    print_result_summary(results, args.output_dir)


if __name__ == "__main__":
    main()