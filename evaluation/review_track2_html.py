import argparse
import html
import json
from pathlib import Path


def read_jsonl(path: Path) -> dict:
    data = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            name = (
                obj.get("imagename")
                or obj.get("image_name")
                or obj.get("filename")
                or obj.get("id")
            )
            if name:
                data[name] = obj
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images_dir", type=Path, required=True)
    parser.add_argument("--csv_jsonl", type=Path, required=True)
    parser.add_argument("--summary_jsonl", type=Path, required=True)
    parser.add_argument("--out_html", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    csv_data = read_jsonl(args.csv_jsonl)
    summary_data = read_jsonl(args.summary_jsonl)

    names = sorted(set(csv_data.keys()) | set(summary_data.keys()))
    names = names[: args.limit]

    rows = []

    for name in names:
        image_path = args.images_dir / name

        pred_csv = csv_data.get(name, {}).get("predicted_csv", "")
        pred_summary = summary_data.get(name, {}).get("predicted_summary", "")

        if image_path.exists():
            image_src = image_path.resolve().as_uri()
            image_html = f'<img src="{image_src}" class="chart">'
        else:
            image_html = f"<p class='missing'>Missing image: {html.escape(name)}</p>"

        rows.append(
            f"""
            <section class="card">
                <h2>{html.escape(name)}</h2>
                <div class="grid">
                    <div>
                        {image_html}
                    </div>
                    <div>
                        <h3>Predicted CSV</h3>
                        <pre>{html.escape(pred_csv)}</pre>
                        <h3>Predicted Summary</h3>
                        <p>{html.escape(pred_summary)}</p>
                    </div>
                </div>
            </section>
            """
        )

    page = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Track 2 Review</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 24px;
    background: #f7f7f7;
    color: #222;
}}
.card {{
    background: white;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}}
.grid {{
    display: grid;
    grid-template-columns: 45% 55%;
    gap: 20px;
    align-items: start;
}}
.chart {{
    max-width: 100%;
    border: 1px solid #ddd;
    border-radius: 8px;
}}
pre {{
    white-space: pre-wrap;
    background: #f1f1f1;
    padding: 12px;
    border-radius: 8px;
    overflow-x: auto;
}}
h2 {{
    font-size: 16px;
    margin-top: 0;
}}
h3 {{
    margin-bottom: 6px;
}}
.missing {{
    color: red;
}}
</style>
</head>
<body>
<h1>Track 2 Review</h1>
<p>Showing {len(names)} samples.</p>
{''.join(rows)}
</body>
</html>
"""

    args.out_html.parent.mkdir(parents=True, exist_ok=True)
    args.out_html.write_text(page, encoding="utf-8")
    print(f"Wrote {args.out_html}")


if __name__ == "__main__":
    main()
