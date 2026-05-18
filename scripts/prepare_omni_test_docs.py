import shutil
from pathlib import Path

SRC_DIR = Path("data/OmniDocBench/images")
DST_DIR = Path("data/omni_test_docs")
LIMIT = 10

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

def main():
    DST_DIR.mkdir(parents=True, exist_ok=True)

    images = sorted(
        p for p in SRC_DIR.rglob("*")
        if p.suffix.lower() in IMAGE_EXTS
    )

    if not images:
        raise RuntimeError(f"No images found in {SRC_DIR}")

    for img in images[:LIMIT]:
        doc_id = img.stem
        out_folder = DST_DIR / doc_id
        out_folder.mkdir(parents=True, exist_ok=True)

        out_img = out_folder / img.name
        if not out_img.exists():
            shutil.copy2(img, out_img)

    print(f"Prepared {min(LIMIT, len(images))} test docs in {DST_DIR}")

if __name__ == "__main__":
    main()