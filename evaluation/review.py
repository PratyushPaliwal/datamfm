"""
Generate a visual HTML review report — image + CSV + summary side by side.

Usage:
    python evaluation/review.py \
        --predictions  submission/track2_sample \
        --images_dir   "/Users/pratyushpaliwal/Downloads/drive-download-20260514T140114Z-3-001" \
        --split        real \
        --output       submission/review.html
"""

import argparse
import base64
import json
import shutil
from pathlib import Path


def load_jsonl(path: Path) -> dict[str, dict]:
    records = {}
    if not path.exists():
        return records
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                records[obj["imagename"]] = obj
            except Exception:
                pass
    return records


def find_image(imagename: str, images_dir: Path, split: str) -> Path | None:
    """Search common folder layouts for the image file."""
    candidates = [
        images_dir / split / "images" / imagename,
        images_dir / split / imagename,
        images_dir / "images" / imagename,
        images_dir / imagename,
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def image_to_base64(path: Path) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    suffix = path.suffix.lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "webp": "image/webp"}.get(suffix.lstrip("."), "image/png")
    return f"data:{mime};base64,{data}"


def build_html(records: list[dict], split: str) -> str:
    cards = ""
    for i, r in enumerate(records):
        img_tag = (
            f'<img src="{r["img_src"]}" alt="{r["imagename"]}">'
            if r["img_src"] else
            '<div class="no-img">Image not found</div>'
        )
        csv_html = r["csv"].replace("\n", "<br>") if r["csv"] else '<span class="err">empty</span>'
        summary_html = r["summary"] if r["summary"] else '<span class="err">empty</span>'

        is_error = "ERROR:" in r["csv"] or "ERROR:" in r["summary"]
        card_class = "card error" if is_error else "card"

        cards += f"""
        <div class="{card_class}">
            <div class="card-header">
                <span class="num">#{i+1}</span>
                <span class="name">{r["imagename"]}</span>
                {"<span class='badge-err'>ERROR</span>" if is_error else ""}
            </div>
            <div class="card-body">
                <div class="col img-col">
                    <div class="col-label">Input image</div>
                    {img_tag}
                </div>
                <div class="col csv-col">
                    <div class="col-label">Predicted CSV</div>
                    <pre>{r["csv"]}</pre>
                </div>
                <div class="col summary-col">
                    <div class="col-label">Predicted summary</div>
                    <p>{summary_html}</p>
                </div>
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Track 2 Review — {split}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          font-size: 14px; background: #f5f5f5; color: #1a1a1a; padding: 24px; }}
  h1 {{ font-size: 20px; font-weight: 500; margin-bottom: 20px; color: #111; }}
  .meta {{ font-size: 13px; color: #666; margin-bottom: 24px; }}
  .card {{ background: #fff; border: 1px solid #e0e0e0; border-radius: 10px;
           margin-bottom: 24px; overflow: hidden; }}
  .card.error {{ border-color: #f5a3a3; }}
  .card-header {{ display: flex; align-items: center; gap: 10px; padding: 12px 16px;
                  border-bottom: 1px solid #eee; background: #fafafa; }}
  .num {{ font-size: 12px; color: #999; min-width: 28px; }}
  .name {{ font-size: 13px; font-weight: 500; color: #333; word-break: break-all; }}
  .badge-err {{ font-size: 11px; background: #fee; color: #c00;
                padding: 2px 8px; border-radius: 4px; margin-left: auto; }}
  .card-body {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0; }}
  .col {{ padding: 16px; border-right: 1px solid #eee; }}
  .col:last-child {{ border-right: none; }}
  .col-label {{ font-size: 11px; font-weight: 600; color: #888;
                text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }}
  .img-col img {{ width: 100%; border-radius: 6px; border: 1px solid #eee; }}
  .no-img {{ background: #f0f0f0; border-radius: 6px; padding: 40px;
             text-align: center; color: #999; font-size: 12px; }}
  .csv-col pre {{ font-family: "SF Mono", Menlo, monospace; font-size: 12px;
                  white-space: pre-wrap; word-break: break-word; color: #1a1a1a;
                  background: #f8f8f8; padding: 10px; border-radius: 6px;
                  border: 1px solid #eee; max-height: 300px; overflow-y: auto; }}
  .summary-col p {{ font-size: 13px; line-height: 1.7; color: #333; }}
  .err {{ color: #c00; font-style: italic; }}
  @media (max-width: 900px) {{ .card-body {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<h1>Track 2 review — {split} split</h1>
<p class="meta">{len(records)} images · generated by evaluation/review.py</p>
{cards}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True,
                        help="Dir containing real/ and synthetic/ JSONL files")
    parser.add_argument("--images_dir",  type=Path, required=True,
                        help="Root dir of the downloaded chart dataset")
    parser.add_argument("--split",       type=str,  default="real")
    parser.add_argument("--output",      type=Path, default=Path("submission/review.html"))
    parser.add_argument("--limit",       type=int,  default=None,
                        help="Only include this many images in the report")
    args = parser.parse_args()

    pred_csv     = load_jsonl(args.predictions / args.split / "chart2csv_predictions.jsonl")
    pred_summary = load_jsonl(args.predictions / args.split / "chart2summary_predictions.jsonl")

    all_images = sorted(set(list(pred_csv.keys()) + list(pred_summary.keys())))
    if args.limit:
        all_images = all_images[:args.limit]

    if not all_images:
        print(f"No predictions found in {args.predictions / args.split}")
        return

    print(f"Building report for {len(all_images)} images...")

    records = []
    missing = 0
    for imagename in all_images:
        img_path = find_image(imagename, args.images_dir, args.split)
        if img_path:
            img_src = image_to_base64(img_path)
        else:
            img_src = None
            missing += 1

        records.append({
            "imagename": imagename,
            "img_src":   img_src,
            "csv":       pred_csv.get(imagename, {}).get("predicted_csv", ""),
            "summary":   pred_summary.get(imagename, {}).get("predicted_summary", ""),
        })

    if missing:
        print(f"  Warning: {missing} images not found in {args.images_dir}")

    html = build_html(records, args.split)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")

    print(f"Report saved: {args.output}")
    print(f"Open it in your browser: open {args.output}")


if __name__ == "__main__":
    main()