import shutil
from pathlib import Path

SRC_DIR = Path("data/document_parsing_download/images")
DST_DIR = Path("data/doc_pages_78")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

def main():
    if not SRC_DIR.exists():
        raise FileNotFoundError(f"Source folder not found: {SRC_DIR}")

    DST_DIR.mkdir(parents=True, exist_ok=True)

    images = sorted(
        p for p in SRC_DIR.rglob("*")
        if p.suffix.lower() in IMAGE_EXTS
    )

    if not images:
        raise RuntimeError(f"No images found in {SRC_DIR}")

    for img in images:
        doc_id = img.stem
        out_dir = DST_DIR / doc_id
        out_dir.mkdir(parents=True, exist_ok=True)

        out_img = out_dir / img.name
        if not out_img.exists():
            shutil.copy2(img, out_img)

    print(f"Prepared {len(images)} document folders in {DST_DIR}")

if __name__ == "__main__":
    main()