"""
merge_summaries.py — Merge original + updated summaries into final JSONL files
==============================================================================

Folder structure expected:
    track2_granite_qwen_safe_full/
        real/
            chart2csv_predictions.jsonl
            org_real_chart2summary_predictions.jsonl   ← original baseline
        synthetic/
            chart2csv_predictions.jsonl
            org_syn_chart2summary_predictions.jsonl    ← original baseline

    updated_summaries/
        real_updated_summaries/
            collab_real_chart2summary_predictions.jsonl
            summaries_gpu0.jsonl
            summaries_gpu1.jsonl
            chart2summary_predictions.jsonl            (ignored if same as original)
        synthetic_updated_summaries/
            collab_syn_chart2summary_predictions.jsonl
            summaries_gpu2.jsonl
            summaries_gpu3.jsonl

Output:
    final_output/
        real/
            chart2summary_predictions.jsonl   ← merged
            chart2csv_predictions.jsonl       ← copied unchanged
        synthetic/
            chart2summary_predictions.jsonl   ← merged
            chart2csv_predictions.jsonl       ← copied unchanged

Usage:
    python3 merge_summaries.py

    # Preview counts without writing
    python3 merge_summaries.py --dry-run

    # Custom paths
    python3 merge_summaries.py \
        --org-root ./track2_granite_qwen_safe_full \
        --updated-root ./updated_summaries \
        --output-root ./final_output
"""

import argparse
import json
import shutil
from pathlib import Path


# ── Default paths (edit if your folder layout differs) ────────────────────────

DEFAULT_ORG_ROOT     = Path("./track2_granite_qwen_safe_full")
DEFAULT_UPDATED_ROOT = Path("./updated_summaries")
DEFAULT_OUTPUT_ROOT  = Path("./final_output")

# Map split → original summary filename
ORG_SUMMARY_FILES = {
    "real":      "org_real_chart2summary_predictions.jsonl",
    "synthetic": "org_syn_chart2summary_predictions.jsonl",
}

# Map split → updated summaries subfolder
UPDATED_FOLDERS = {
    "real":      "real_updated_summaries",
    "synthetic": "synthetic_updated_summaries",
}

# These files inside updated folders should be SKIPPED
# (they are copies of the original, not updates)
# SKIP_FILENAMES = {
#     "chart2summary_predictions.jsonl",  # likely original copy
# }
SKIP_FILENAMES = set()


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_jsonl(path: Path) -> dict:
    """Load JSONL into {imagename: predicted_summary} dict."""
    records = {}
    skipped = 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                name = obj.get("imagename", "")
                summary = obj.get("predicted_summary", "")
                if name and summary:
                    records[name] = summary
                else:
                    skipped += 1
            except json.JSONDecodeError:
                skipped += 1
    if skipped:
        print(f"    ⚠️  Skipped {skipped} malformed lines in {path.name}")
    return records


def load_all_updates(updated_folder: Path) -> dict:
    """
    Load all JSONL files from the updated folder into one merged dict.
    Later files overwrite earlier ones if same imagename appears.
    Files in SKIP_FILENAMES are ignored.
    """
    all_updates = {}
    jsonl_files = sorted(updated_folder.glob("*.jsonl"))

    if not jsonl_files:
        print(f"  ⚠️  No JSONL files found in {updated_folder}")
        return all_updates

    for jfile in jsonl_files:
        if jfile.name in SKIP_FILENAMES:
            print(f"    ⏭️  Skipping {jfile.name} (in skip list)")
            continue
        updates = load_jsonl(jfile)
        print(f"    📄 {jfile.name}: {len(updates)} entries")
        # Later files take priority — overwrite earlier
        all_updates.update(updates)

    return all_updates


def merge_split(
    split: str,
    org_root: Path,
    updated_root: Path,
    output_root: Path,
    dry_run: bool = False,
):
    print(f"\n{'='*60}")
    print(f"  Processing: {split.upper()}")
    print(f"{'='*60}")

    # ── Paths ─────────────────────────────────────────────────────────────────
    org_summary_path = org_root / split / ORG_SUMMARY_FILES[split]
    csv_path         = org_root / split / "chart2csv_predictions.jsonl"
    updated_folder   = updated_root / UPDATED_FOLDERS[split]
    out_dir          = output_root / split
    out_summary      = out_dir / "chart2summary_predictions.jsonl"
    out_csv          = out_dir / "chart2csv_predictions.jsonl"

    # ── Validate ──────────────────────────────────────────────────────────────
    if not org_summary_path.exists():
        print(f"  ❌ Original summary not found: {org_summary_path}")
        return
    if not updated_folder.exists():
        print(f"  ❌ Updated folder not found: {updated_folder}")
        return

    # ── Load original summaries ───────────────────────────────────────────────
    print(f"\n  Loading original summaries...")
    originals = load_jsonl(org_summary_path)
    all_names = list(originals.keys())
    print(f"  ✅ {len(all_names)} images in original file")

    # ── Load all updates ──────────────────────────────────────────────────────
    print(f"\n  Loading updated summaries from {updated_folder.name}/...")
    updates = load_all_updates(updated_folder)
    print(f"  ✅ {len(updates)} total updated entries across all files")

    # ── Merge ─────────────────────────────────────────────────────────────────
    replaced = 0
    kept     = 0
    missing  = 0

    merged = []
    for name in all_names:
        if name in updates:
            merged.append({"imagename": name, "predicted_summary": updates[name]})
            replaced += 1
        elif name in originals:
            merged.append({"imagename": name, "predicted_summary": originals[name]})
            kept += 1
        else:
            merged.append({"imagename": name, "predicted_summary": ""})
            missing += 1

    total = len(merged)
    print(f"\n  {'[DRY RUN] ' if dry_run else ''}Merge results:")
    print(f"    Total images  : {total}")
    print(f"    Updated        : {replaced} ({replaced/total*100:.1f}%)")
    print(f"    Kept original  : {kept}     ({kept/total*100:.1f}%)")
    print(f"    Missing both   : {missing}")

    if dry_run:
        print(f"\n  [DRY RUN] Would write to: {out_summary}")
        return

    # ── Write output ──────────────────────────────────────────────────────────
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_summary, "w") as f:
        for obj in merged:
            f.write(json.dumps(obj) + "\n")
    print(f"\n  ✅ Written: {out_summary}")
    print(f"     Lines: {len(merged)}")

    # Copy CSV unchanged
    if csv_path.exists():
        shutil.copy2(csv_path, out_csv)
        print(f"  ✅ CSV copied: {out_csv}")
    else:
        print(f"  ⚠️  CSV not found at {csv_path} — skipping")


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="Merge original + updated summaries")
    p.add_argument("--org-root",     type=Path, default=DEFAULT_ORG_ROOT)
    p.add_argument("--updated-root", type=Path, default=DEFAULT_UPDATED_ROOT)
    p.add_argument("--output-root",  type=Path, default=DEFAULT_OUTPUT_ROOT)
    p.add_argument("--split",        choices=["real", "synthetic", "all"], default="all")
    p.add_argument("--dry-run",      action="store_true",
                   help="Preview counts without writing any files")
    return p.parse_args()


if __name__ == "__main__":
    args   = parse_args()
    splits = ["real", "synthetic"] if args.split == "all" else [args.split]

    print(f"\n{'='*60}")
    print(f"  Summary Merge Script")
    print(f"  Org root     : {args.org_root}")
    print(f"  Updated root : {args.updated_root}")
    print(f"  Output root  : {args.output_root}")
    print(f"  Dry run      : {args.dry_run}")
    print(f"{'='*60}")

    for split in splits:
        merge_split(
            split=split,
            org_root=args.org_root,
            updated_root=args.updated_root,
            output_root=args.output_root,
            dry_run=args.dry_run,
        )

    if not args.dry_run:
        print(f"\n✅ ALL DONE — final files in: {args.output_root}")
        print(f"   {args.output_root}/real/chart2summary_predictions.jsonl")
        print(f"   {args.output_root}/synthetic/chart2summary_predictions.jsonl")
    else:
        print(f"\n[DRY RUN] No files written.")