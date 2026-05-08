"""
Build the final submission.zip for EvalAI upload.
Usage:
    python scripts/build_submission.py
"""

import zipfile
from pathlib import Path
import subprocess
import sys


def validate_first():
    """Run validation before zipping."""
    print("Running validation before building zip...\n")
    for track, output_dir in [(1, "submission/track1"), (2, "submission/track2")]:
        result = subprocess.run(
            [sys.executable, "scripts/validate.py",
             "--track", str(track), "--output_dir", output_dir],
            capture_output=False
        )
        if result.returncode != 0:
            return False
    return True


def build_zip(output_path: Path = Path("submission/submission.zip")):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    track1_dir = Path("submission/track1")
    track2_dir = Path("submission/track2")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Track 1: .md files
        if track1_dir.exists():
            files = list(track1_dir.rglob("*.md"))
            print(f"\nAdding Track 1: {len(files)} .md files")
            for f in files:
                zf.write(f, f.relative_to(track1_dir))

        # Track 2: .jsonl files
        if track2_dir.exists():
            files = list(track2_dir.rglob("*.jsonl"))
            print(f"Adding Track 2: {len(files)} .jsonl files")
            for f in files:
                zf.write(f, f.relative_to(track2_dir))

    size_mb = output_path.stat().st_size / 1_048_576
    print(f"\nSubmission zip created: {output_path} ({size_mb:.1f} MB)")
    print("Upload to: https://eval.ai/web/challenges/list")


if __name__ == "__main__":
    if validate_first():
        build_zip()
    else:
        print("\nValidation failed — fix errors before building zip.")
        sys.exit(1)
