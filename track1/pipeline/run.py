"""
Track 1 — Document Parsing with MinerU

Input:
    data/doc_pages/<document_uuid>/page_*.jpg

Output:
    submission/track1/<document_uuid>.md

Usage:
    python -m track1.pipeline.run \
        --input_dir data/doc_pages \
        --output_dir submission/track1 \
        --limit 5
"""

import argparse
import re
import subprocess
import tempfile
from pathlib import Path
from tqdm import tqdm

from track1.postprocess.cleaner import clean_markdown


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def natural_page_key(path: Path):
    """
    Sort page_1, page_2, ..., page_10 correctly.
    """
    nums = re.findall(r"\d+", path.stem)
    return int(nums[-1]) if nums else path.name


def parse_page_mineru(image_path: Path, timeout: int = 180) -> str:
    """
    Run MinerU on one page image and return Markdown.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        result = subprocess.run(
            ["mineru", "-p", str(image_path), "-o", tmp_dir],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"MinerU failed on {image_path.name}\n"
                f"STDOUT:\n{result.stdout[:1000]}\n"
                f"STDERR:\n{result.stderr[:1000]}"
            )

        md_files = list(Path(tmp_dir).rglob("*.md"))

        if not md_files:
            raise RuntimeError(f"MinerU produced no Markdown for {image_path.name}")

        # Usually there is one main md file.
        return md_files[0].read_text(encoding="utf-8", errors="ignore")


def process_document(doc_dir: Path, output_dir: Path, config: dict) -> dict:
    """
    Process one document folder into one flat UUID-named Markdown file.
    """
    document_id = doc_dir.name
    out_path = output_dir / f"{document_id}.md"

    if out_path.exists():
        return {
            "document_id": document_id,
            "status": "skipped",
            "pages": 0,
        }

    page_images = sorted(
        [
            p for p in doc_dir.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        ],
        key=natural_page_key,
    )

    if not page_images:
        out_path.write_text(
            f"<!-- ERROR: no page images found in {doc_dir} -->",
            encoding="utf-8",
        )
        return {
            "document_id": document_id,
            "status": "error",
            "pages": 0,
            "error": "no page images found",
        }

    page_markdowns = []
    page_errors = []

    for page_idx, image_path in enumerate(page_images, start=1):
        try:
            raw_md = parse_page_mineru(image_path)
            clean_md = clean_markdown(raw_md, config)
            page_markdowns.append(clean_md.strip())
        except Exception as e:
            page_errors.append((image_path.name, str(e)))
            page_markdowns.append(
                f"<!-- ERROR processing page {image_path.name}: {e} -->"
            )

    # Important: one document-level markdown file.
    document_md = "\n\n".join(md for md in page_markdowns if md.strip())

    out_path.write_text(document_md, encoding="utf-8")

    if page_errors:
        return {
            "document_id": document_id,
            "status": "partial",
            "pages": len(page_images),
            "errors": len(page_errors),
        }

    return {
        "document_id": document_id,
        "status": "ok",
        "pages": len(page_images),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=Path, required=True)
    parser.add_argument("--output_dir", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    config = {
        "postprocess": {
            "normalise_text": True,
            "lint_html_tables": True,
            "validate_latex": True,
        }
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)

    doc_dirs = sorted(
        [p for p in args.input_dir.iterdir() if p.is_dir()],
        key=lambda p: p.name,
    )

    if args.limit:
        doc_dirs = doc_dirs[: args.limit]

    print(f"Found {len(doc_dirs)} documents")

    counts = {
        "ok": 0,
        "partial": 0,
        "skipped": 0,
        "error": 0,
    }

    total_pages = 0

    for doc_dir in tqdm(doc_dirs, desc="Parsing documents"):
        result = process_document(doc_dir, args.output_dir, config)
        status = result["status"]
        counts[status] = counts.get(status, 0) + 1
        total_pages += result.get("pages", 0)

        if status in {"error", "partial"}:
            print(f"\n{status.upper()} {result['document_id']}: {result}")

    print("\nDone.")
    print(f"OK: {counts.get('ok', 0)}")
    print(f"Partial: {counts.get('partial', 0)}")
    print(f"Skipped: {counts.get('skipped', 0)}")
    print(f"Errors: {counts.get('error', 0)}")
    print(f"Pages processed/reported: {total_pages}")
    print(f"Output: {args.output_dir}")


if __name__ == "__main__":
    main()