import json
from pathlib import Path


ANN_PATH = Path("data/OmniDocBench/OmniDocBench.json")
OUT_DIR = Path("evaluation/omni_ground_truth_md")

OUT_DIR.mkdir(parents=True, exist_ok=True)


def block_to_markdown(block: dict) -> str:
    category = block.get("category_type", "")
    
    # Prefer table HTML if available
    if category == "table":
        html = block.get("html")
        if html:
            return html.strip()
        latex = block.get("latex")
        if latex:
            return latex.strip()

    # Formula blocks
    if "equation" in category or "formula" in category:
        latex = block.get("latex") or block.get("text")
        if latex:
            latex = latex.strip()
            return f"$$\n{latex}\n$$"

    # Text-like blocks
    text = block.get("text")
    if text:
        text = text.strip()

        if category == "title":
            return f"# {text}"

        if category in {"section_header", "header"}:
            return f"## {text}"

        return text

    return ""


def get_page_id(item: dict) -> str:
    page_info = item.get("page_info", {})
    image_path = page_info.get("image_path", "")
    if image_path:
        return Path(image_path).stem

    # fallback
    page_no = page_info.get("page_no", "unknown")
    return f"page_{page_no}"


def main():
    with ANN_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0

    for item in data:
        page_id = get_page_id(item)
        blocks = item.get("layout_dets", [])

        valid_blocks = [
            b for b in blocks
            if not b.get("ignore", False)
        ]

        valid_blocks.sort(key=lambda b: b.get("order") if b.get("order") is not None else 10**9)

        md_parts = []
        for block in valid_blocks:
            md = block_to_markdown(block)
            if md:
                md_parts.append(md)

        out_path = OUT_DIR / f"{page_id}.md"
        out_path.write_text("\n\n".join(md_parts).strip() + "\n", encoding="utf-8")
        count += 1

    print(f"Wrote {count} ground-truth Markdown files to {OUT_DIR}")


if __name__ == "__main__":
    main()