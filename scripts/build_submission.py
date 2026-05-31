"""
Build and validate the submission zip for EvalAI.

Submission structure (from README):
  submission.zip
  ├── real/
  │   ├── chart2csv_predictions.jsonl
  │   └── chart2summary_predictions.jsonl
  └── synthetic/
      ├── chart2csv_predictions.jsonl
      └── chart2summary_predictions.jsonl

Usage:
    python scripts/build_submission.py \
        --output_dir submission/track2_full \
        --out submission/submission_chart.zip
"""

import argparse
import json
import zipfile
from pathlib import Path


def validate_jsonl(path: Path, value_key: str) -> tuple[int, list[str]]:
    """Returns (count, errors)."""
    if not path.exists():
        return 0, [f"Missing file: {path}"]
    errors = []
    count = 0
    with open(path) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if "imagename" not in obj:
                    errors.append(f"Line {i+1}: missing 'imagename'")
                if value_key not in obj:
                    errors.append(f"Line {i+1}: missing '{value_key}'")
                count += 1
            except json.JSONDecodeError as e:
                errors.append(f"Line {i+1}: JSON error: {e}")
    return count, errors


def validate_output(output_dir: Path) -> bool:
    print("\nValidating output...")
    all_ok = True
    splits = ["real", "synthetic"]

    for split in splits:
        split_dir = output_dir / split
        print(f"\n  [{split}]")

        for fname, key in [
            ("chart2csv_predictions.jsonl", "predicted_csv"),
            ("chart2summary_predictions.jsonl", "predicted_summary"),
        ]:
            fpath = split_dir / fname
            count, errors = validate_jsonl(fpath, key)
            if errors:
                print(f"    {fname}: {count} rows — ERRORS:")
                for e in errors[:5]:
                    print(f"      {e}")
                all_ok = False
            else:
                print(f"    {fname}: {count} rows — OK")

    return all_ok


def build_zip(output_dir: Path, zip_path: Path):
    splits = ["real", "synthetic"]
    files_added = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for split in splits:
            for fname in ["chart2csv_predictions.jsonl",
                          "chart2summary_predictions.jsonl"]:
                fpath = output_dir / split / fname
                if fpath.exists():
                    arcname = f"{split}/{fname}"
                    zf.write(fpath, arcname)
                    files_added += 1
                    print(f"  Added: {arcname} ({fpath.stat().st_size/1024:.0f} KB)")
                else:
                    print(f"  MISSING: {split}/{fname}")

    size_mb = zip_path.stat().st_size / 1_048_576
    print(f"\nZip: {zip_path} ({size_mb:.1f} MB) | {files_added} files")
    return files_added == 4  # must have all 4 files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=Path,
                        default=Path("submission/track2_full"))
    parser.add_argument("--out",        type=Path,
                        default=Path("submission/submission_chart.zip"))
    parser.add_argument("--skip_validation", action="store_true")
    args = parser.parse_args()

    if not args.skip_validation:
        ok = validate_output(args.output_dir)
        if not ok:
            print("\nValidation failed — fix errors before submitting.")
            return

    print("\nBuilding submission zip...")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    success = build_zip(args.output_dir, args.out)

    if success:
        print(f"\n✅ Ready to submit: {args.out}")
        print("   Upload to: https://eval.ai  → DataMFM → Submit")
        print("   Select: Task = Chart Understanding")
    else:
        print("\n⚠️  Some files missing — check output directory")


if __name__ == "__main__":
    main()
