"""
Validate submission outputs before zipping.
Usage:
    python scripts/validate.py --track 1 --output_dir submission/track1
    python scripts/validate.py --track 2 --output_dir submission/track2
"""

import argparse
import csv
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup


def validate_track1(output_dir: Path):
    print(f"\nValidating Track 1 output: {output_dir}")
    folders = [d for d in output_dir.iterdir() if d.is_dir()]
    if not folders:
        print("  ERROR: no document folders found")
        return

    total_files = 0
    errors = []

    for folder in sorted(folders):
        md_files = sorted(folder.glob("*.md"))
        total_files += len(md_files)

        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")

            # Check for error placeholders
            if content.startswith("<!-- ERROR"):
                errors.append(f"  ERROR placeholder: {md_path}")
                continue

            # Check tables are valid HTML
            tables = re.findall(r"<table[\s\S]*?</table>", content, re.IGNORECASE)
            for table in tables:
                try:
                    soup = BeautifulSoup(table, "lxml")
                    if not soup.find("table"):
                        errors.append(f"  Malformed table in {md_path.name}")
                except Exception as e:
                    errors.append(f"  Table parse error in {md_path.name}: {e}")

            # Check formulas are non-empty
            display_formulas = re.findall(r"\$\$([\s\S]*?)\$\$", content)
            for formula in display_formulas:
                if not formula.strip():
                    errors.append(f"  Empty formula in {md_path.name}")

    print(f"  Folders: {len(folders)}")
    print(f"  Total .md files: {total_files}")
    if errors:
        print(f"  WARNINGS ({len(errors)}):")
        for e in errors[:20]:
            print(f"    {e}")
        if len(errors) > 20:
            print(f"    ... and {len(errors) - 20} more")
    else:
        print("  All files valid.")


def validate_track2(output_dir: Path):
    print(f"\nValidating Track 2 output: {output_dir}")
    splits = ["real", "synthetic"]
    all_ok = True

    for split in splits:
        split_dir = output_dir / split
        if not split_dir.exists():
            print(f"  WARNING: missing split directory: {split_dir}")
            all_ok = False
            continue

        for task_file, key in [
            ("chart2csv_predictions.jsonl", "predicted_csv"),
            ("chart2summary_predictions.jsonl", "predicted_summary"),
        ]:
            fpath = split_dir / task_file
            if not fpath.exists():
                print(f"  ERROR: missing {fpath}")
                all_ok = False
                continue

            with open(fpath) as f:
                lines = [l.strip() for l in f if l.strip()]

            errors = []
            for i, line in enumerate(lines):
                try:
                    obj = json.loads(line)
                    if "imagename" not in obj:
                        errors.append(f"line {i+1}: missing 'imagename'")
                    if key not in obj:
                        errors.append(f"line {i+1}: missing '{key}'")
                    if key == "predicted_csv" and obj.get(key):
                        # Check CSV parses
                        import io
                        rows = list(csv.reader(io.StringIO(obj[key])))
                        if not rows:
                            errors.append(f"line {i+1}: empty CSV")
                except json.JSONDecodeError as e:
                    errors.append(f"line {i+1}: JSON error: {e}")

            status = "OK" if not errors else f"ERRORS ({len(errors)})"
            print(f"  {split}/{task_file}: {len(lines)} entries — {status}")
            for err in errors[:5]:
                print(f"    {err}")

    if all_ok:
        print("  All Track 2 files valid.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", type=int, choices=[1, 2], required=True)
    parser.add_argument("--output_dir", type=Path, required=True)
    args = parser.parse_args()

    if args.track == 1:
        validate_track1(args.output_dir)
    else:
        validate_track2(args.output_dir)


if __name__ == "__main__":
    main()
