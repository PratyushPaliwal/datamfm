"""
Track 2 model runners for Chart Understanding.

Granite-only version:
    chart image -> Granite Chart2CSV -> CSV
    cleaned CSV -> fact-based rule summary

No DePlot.
No OpenRouter.
No Gemini.
No Claude.
No API keys.
"""

import csv
import io
import math
import re
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def _load_granite_chart2csv(model_name: str):
    """
    Load Granite Vision Chart2CSV model once and cache it.

    Recommended install:
        pip install -U "transformers>=4.49" accelerate pillow torch torchvision
    """
    import torch
    from transformers import AutoProcessor, AutoModelForImageTextToText

    processor = AutoProcessor.from_pretrained(
        model_name,
        trust_remote_code=True,
    )

    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model = AutoModelForImageTextToText.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        trust_remote_code=True,
    )

    model = model.to(device)
    model.eval()

    print(f"[Granite] Loaded {model_name} on {device}")

    return processor, model, device


def extract_csv(image_path: Path, config: dict) -> str:
    """
    Extract chart data as CSV from one chart image.
    """
    model_type = config.get("pipeline", {}).get(
        "csv_model",
        "granite_chart2csv",
    ).lower()

    if model_type == "granite_chart2csv":
        return _granite_extract_csv(image_path, config)

    raise ValueError(
        f"Unknown csv_model: {model_type}. "
        "This runner currently supports only 'granite_chart2csv'."
    )


def _granite_extract_csv(image_path: Path, config: dict) -> str:
    """
    Use Granite Vision Chart2CSV to extract CSV from a chart image.
    """
    import torch
    from PIL import Image

    model_name = config.get("pipeline", {}).get(
        "granite_model_name",
        "ibm-granite/granite-vision-3.3-2b-chart2csv-preview",
    )

    processor, model, device = _load_granite_chart2csv(model_name)

    image = Image.open(image_path).convert("RGB")

    prompt = config.get("prompts", {}).get(
        "granite_csv_prompt",
        "Extract all visible data from this chart into a CSV table. Return only raw CSV.",
    )

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt},
            ],
        }
    ]

    inputs = _build_granite_inputs(
        processor=processor,
        image=image,
        prompt=prompt,
        messages=messages,
        device=device,
    )

    max_new_tokens = config.get("pipeline", {}).get("max_new_tokens", 768)

    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )

    output = _decode_generated_output(
        processor=processor,
        generated_ids=generated_ids,
        inputs=inputs,
    )

    return _clean_model_csv_output(output)


def _build_granite_inputs(processor, image, prompt: str, messages: list, device: str):
    """
    Build Granite model inputs.

    Tries chat-template first. Falls back to direct image+text processing.
    """
    try:
        text = processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = processor(
            text=[text],
            images=[image],
            return_tensors="pt",
            padding=True,
        )

    except Exception:
        inputs = processor(
            images=image,
            text=prompt,
            return_tensors="pt",
        )

    return inputs.to(device)


def _decode_generated_output(processor, generated_ids, inputs) -> str:
    """
    Decode generated model tokens.

    If possible, trim the prompt/input tokens before decoding.
    """
    try:
        input_len = inputs["input_ids"].shape[-1]
        generated_ids = generated_ids[:, input_len:]
    except Exception:
        pass

    output = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]

    return output.strip()


def _clean_model_csv_output(text: str) -> str:
    """
    Clean Granite output into plain CSV-like text.
    """
    text = (text or "").strip()

    if not text:
        return ""

    # Remove Markdown code fences.
    text = re.sub(r"```(?:csv)?", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "")

    # Normalize escaped line breaks.
    text = text.replace("\\n", "\n")
    text = text.replace("<0x0A>", "\n")
    text = text.replace("<0x0a>", "\n")

    # Remove common preambles.
    text = re.sub(
        r"(?is)^.*?(csv|table)\s*[:\-]\s*",
        "",
        text,
    ).strip()

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        return ""

    parsed_rows = []

    for line in lines:
        lower = line.lower()

        if lower.startswith(
            (
                "here is",
                "the csv",
                "csv output",
                "converted",
                "this chart",
                "the chart",
                "below is",
                "sure",
                "i extracted",
            )
        ):
            continue

        line = _normalize_number_text(line)
        cells = _split_table_line(line)

        if cells:
            parsed_rows.append(cells)

    if not parsed_rows:
        return ""

    return _normalize_csv_rows(parsed_rows)


def _normalize_number_text(line: str) -> str:
    """
    Normalize numbers in a CSV/table line.

    Examples:
        42.3K -> 42300
        1.5M  -> 1500000
        $42,300 -> 42300
    """
    line = re.sub(
        r"(?i)(\d+(?:\.\d+)?)\s*K\b",
        lambda m: f"{float(m.group(1)) * 1000:g}",
        line,
    )
    line = re.sub(
        r"(?i)(\d+(?:\.\d+)?)\s*M\b",
        lambda m: f"{float(m.group(1)) * 1000000:g}",
        line,
    )
    line = re.sub(
        r"(?i)(\d+(?:\.\d+)?)\s*B\b",
        lambda m: f"{float(m.group(1)) * 1000000000:g}",
        line,
    )

    # Remove currency symbols.
    line = re.sub(r"[$€£¥]", "", line)

    # Remove thousands separators inside numbers.
    line = re.sub(r"(?<=\d),(?=\d{3}\b)", "", line)

    return line


def _split_table_line(line: str) -> list[str]:
    """
    Split one table-like line into cells.
    """
    line = line.strip()

    if not line:
        return []

    if "|" in line and "," not in line:
        cells = [cell.strip() for cell in line.split("|")]
        return [cell for cell in cells if cell]

    if "\t" in line and "," not in line:
        cells = [cell.strip() for cell in line.split("\t")]
        return [cell for cell in cells if cell]

    try:
        cells = next(csv.reader([line]))
        return [cell.strip() for cell in cells if cell.strip()]
    except Exception:
        return [line]


def _normalize_csv_rows(rows: list[list[str]]) -> str:
    """
    Make CSV rows more consistent.

    Keeps the most common useful column count.
    Also removes exact duplicate rows.
    """
    rows = [row for row in rows if any(cell.strip() for cell in row)]

    if not rows:
        return ""

    # Remove exact duplicate rows while preserving order.
    deduped = []
    seen = set()

    for row in rows:
        key = tuple(cell.strip().lower() for cell in row)
        if key not in seen:
            deduped.append(row)
            seen.add(key)

    rows = deduped

    length_counts = {}
    for row in rows:
        length_counts[len(row)] = length_counts.get(len(row), 0) + 1

    sorted_lengths = sorted(
        length_counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    target_len = sorted_lengths[0][0]

    if target_len == 1:
        for length, _count in sorted_lengths:
            if length > 1:
                target_len = length
                break

    cleaned_rows = []

    for row in rows:
        if len(row) == target_len:
            cleaned_rows.append(row)
        elif len(row) > target_len:
            cleaned_rows.append(row[:target_len])
        elif 1 < len(row) < target_len:
            cleaned_rows.append(row + [""] * (target_len - len(row)))

    if not cleaned_rows:
        cleaned_rows = rows

    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerows(cleaned_rows)

    return out.getvalue().strip()

@lru_cache(maxsize=1)
def _load_qwen_text_model(model_name: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        trust_remote_code=True,
    )

    model = model.to(device)
    model.eval()

    print(f"[Qwen text] Loaded {model_name} on {device}")

    return tokenizer, model, device


def _qwen_summary_from_csv(csv_text: str, config: dict) -> str:
    import torch

    model_name = config.get("pipeline", {}).get(
        "qwen_text_model_name",
        "Qwen/Qwen2.5-3B-Instruct",
    )

    tokenizer, model, device = _load_qwen_text_model(model_name)

    verified_facts = _rule_based_summary_from_csv(csv_text)

    prompt = f"""You are given chart data in CSV format and verified facts extracted from that CSV.

Write a concise natural-language chart summary in 2 to 4 sentences.

Critical rules:
- Use ONLY the CSV and verified facts.
- Do NOT infer percentages from Yes/No values.
- Do NOT convert Yes/No into 100% or 0%.
- Do NOT swap column meanings.
- Use exact labels and exact numbers from the verified facts.
- Do not add numbers that are not in the CSV or verified facts.
- If verified facts say no clear numeric metric was detected, return that idea in one natural sentence.
- Do not invent chart topics that are not present in the CSV.
- Do not say "the chart compares X across N entries" unless it sounds natural.
- Output only the summary.

CSV:
{csv_text}

Verified facts:
{verified_facts}

Write the summary now:"""

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    if hasattr(tokenizer, "apply_chat_template"):
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
    else:
        text = prompt

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=4096,
    ).to(device)

    max_new_tokens = config.get("pipeline", {}).get(
        "summary_max_new_tokens",
        180,
    )

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )

    generated = output_ids[:, inputs["input_ids"].shape[-1]:]

    summary = tokenizer.decode(
        generated[0],
        skip_special_tokens=True,
    ).strip()

    summary = summary.replace("Summary:", "").strip()
    summary = " ".join(summary.split())

    if not summary:
        return verified_facts

    return summary

def _csv_has_repeated_constant_count_column(csv_text: str) -> bool:
    """
    Detect tables like:
        State,Population Range,Number of States
        Georgia,200000-250000,1
        Colorado,200000-250000,1

    These are usually expanded list/count tables. Qwen may hallucinate that
    every state has '1 state', so use rule-based fallback.
    """
    try:
        rows = list(csv.reader(io.StringIO(csv_text)))
    except Exception:
        return False

    if len(rows) < 5:
        return False

    header = [h.strip().lower() for h in rows[0]]
    data = rows[1:]

    count_like_names = {
        "number of states",
        "number",
        "count",
        "states",
    }

    for idx, name in enumerate(header):
        if name not in count_like_names:
            continue

        values = []
        for row in data:
            if idx >= len(row):
                continue

            value = _numeric_value(row[idx])
            if value is not None:
                values.append(value)

        if len(values) >= 5 and len(set(values)) == 1:
            return True

    return False
def _csv_has_mostly_boolean_values(csv_text: str) -> bool:
    try:
        rows = list(csv.reader(io.StringIO(csv_text)))
    except Exception:
        return False

    if len(rows) < 2:
        return False

    values = []
    for row in rows[1:]:
        for cell in row[1:]:
            val = cell.strip().lower()
            if val:
                values.append(val)

    if not values:
        return False

    boolean_like = {"yes", "no", "true", "false", "y", "n"}
    count_boolean = sum(1 for v in values if v in boolean_like)

    return count_boolean / max(len(values), 1) > 0.5


def _csv_is_too_weak_for_qwen(csv_text: str) -> bool:
    try:
        rows = list(csv.reader(io.StringIO(csv_text)))
    except Exception:
        return True

    if len(rows) < 2:
        return True

    if len(rows) == 2:
        return False

    data = rows[1:]
    numeric_cells = 0
    total_cells = 0

    for row in data:
        for cell in row[1:]:
            val = cell.strip()
            if not val:
                continue

            total_cells += 1

            if _numeric_value(val) is not None:
                numeric_cells += 1

    if total_cells == 0:
        return True

    numeric_ratio = numeric_cells / total_cells
    return numeric_ratio < 0.25


def _summary_has_unsupported_100_percent(summary: str, csv_text: str) -> bool:
    lower_summary = summary.lower()

    if "100%" not in lower_summary and "100 percent" not in lower_summary:
        return False

    lower_csv = csv_text.lower()
    return "100" not in lower_csv and "100%" not in lower_csv


def _extract_numbers(text: str) -> set[str]:
    nums = re.findall(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?%?", text)
    return set(n.strip() for n in nums if n.strip())


def _normalize_num_token(token: str) -> str:
    return token.strip().replace(",", "").replace("%", "")


def _summary_has_numbers_not_in_csv_or_facts(
    summary: str,
    csv_text: str,
    verified_facts: str,
) -> bool:
    summary_nums = {_normalize_num_token(n) for n in _extract_numbers(summary)}

    allowed_nums = {
        _normalize_num_token(n)
        for n in (_extract_numbers(csv_text) | _extract_numbers(verified_facts))
    }

    ignore = {"1", "2", "3", "4", "5"}
    unsupported = summary_nums - allowed_nums - ignore

    return len(unsupported) > 0

def generate_summary_from_csv(csv_text: str, config: dict) -> str:
    """
    Generate summary from cleaned CSV.

    Supports:
        - rule_based
        - rule_based_facts
        - qwen_text

    For qwen_text, use safety gates to avoid hallucinations on:
        - Yes/No categorical tables
        - non-numeric CSVs
        - weak extracted tables
        - unsupported numeric claims
    """
    model = config.get("pipeline", {}).get(
        "summary_model",
        "rule_based_facts",
    ).lower()

    if model in {"rule_based", "rule_based_facts"}:
        return _rule_based_summary_from_csv(csv_text)

    if model in {"qwen_text", "qwen", "qwen2.5"}:
        verified_facts = _rule_based_summary_from_csv(csv_text)

        if "no clear numeric metric column was detected" in verified_facts.lower():
            return verified_facts
        
        if _csv_has_repeated_constant_count_column(csv_text):
            return verified_facts

        if _csv_has_mostly_boolean_values(csv_text):
            return verified_facts

        if _csv_is_too_weak_for_qwen(csv_text):
            return verified_facts

        qwen_summary = _qwen_summary_from_csv(csv_text, config)

        if _summary_has_unsupported_100_percent(qwen_summary, csv_text):
            return verified_facts

        if _summary_has_numbers_not_in_csv_or_facts(qwen_summary, csv_text, verified_facts):
            return verified_facts

        return qwen_summary

    raise ValueError(
        f"Unknown summary_model: {model}. "
        "Supported: rule_based, rule_based_facts, qwen_text."
    )


def _is_number(value: str) -> bool:
    """
    Check whether a value is numeric after removing common symbols.
    """
    value = (
        str(value)
        .strip()
        .replace(",", "")
        .replace("%", "")
        .replace("$", "")
        .replace("€", "")
        .replace("£", "")
    )

    if not value:
        return False

    try:
        float(value)
        return True
    except ValueError:
        return False


def _numeric_value(value: str):
    """
    Convert a string value to float if possible.
    """
    raw = (
        str(value)
        .strip()
        .replace(",", "")
        .replace("%", "")
        .replace("$", "")
        .replace("€", "")
        .replace("£", "")
    )

    try:
        return float(raw)
    except ValueError:
        return None


def _choose_label_column(header: list[str], rows: list[list[str]]) -> int:
    """
    Choose the best label column for summaries.

    Important:
        If the first column is Year/Date/Month, use it as the label axis.
        Prefer Country over Region.
        Prefer specific label/category columns over metric columns.
    """
    lower_header = [h.strip().lower() for h in header]

    # Critical fix for time-series tables.
    if lower_header and lower_header[0] in {
        "year",
        "date",
        "month",
        "quarter",
        "time",
        "week",
    }:
        return 0

    strong_preferred = [
        "country",
        "state",
        "city",
        "category",
        "group",
        "rating",
        "name",
        "label",
        "type",
    ]

    for key in strong_preferred:
        for idx, name in enumerate(lower_header):
            if key in name:
                return idx

    avoid = [
        "region",
        "continent",
        "area",
        "population range",
    ]

    best_idx = 0
    best_score = -1

    for idx, col_name in enumerate(lower_header):
        text_count = 0
        numeric_count = 0

        for row in rows:
            if idx >= len(row):
                continue

            value = row[idx].strip()
            if not value:
                continue

            if _is_number(value):
                numeric_count += 1
            else:
                text_count += 1

        score = text_count - numeric_count

        if any(a in col_name for a in avoid):
            score -= 5

        if score > best_score:
            best_score = score
            best_idx = idx

    return best_idx


def _choose_numeric_columns(header: list[str], rows: list[list[str]], label_col_idx: int) -> list[int]:
    """
    Choose meaningful numeric metric columns.

    Avoid treating label columns such as Year/Date/Country/Category as metrics.
    """
    blocked_exact = {
        "year",
        "date",
        "month",
        "quarter",
        "time",
        "week",
        "population range",
        "states",
        "country",
        "region",
        "category",
        "group",
        "rating",
        "name",
        "label",
        "type",
        "city",
        "state",
    }

    numeric_cols = []

    for idx, col_name in enumerate(header):
        if idx == label_col_idx:
            continue

        name = col_name.strip().lower()

        if name in blocked_exact:
            continue

        values = []

        for row in rows:
            if idx >= len(row):
                continue

            value = _numeric_value(row[idx])
            if value is not None:
                values.append(value)

        if len(values) >= 2:
            numeric_cols.append(idx)

    return numeric_cols[:3]


def _is_ordered_label_axis(label_name: str) -> bool:
    """
    Decide whether first-to-last trend language is meaningful.

    Use trend for time axes.
    Use spread for categorical axes.
    """
    name = label_name.strip().lower()

    ordered_keys = [
        "year",
        "date",
        "month",
        "time",
        "quarter",
        "week",
    ]

    return any(key in name for key in ordered_keys)


def _make_row_label(
    row: list[str],
    header: list[str],
    label_col_idx: int,
    numeric_cols: list[int],
) -> str:
    """
    Build a better row label.

    Simple table:
        Country,Value
        France,85
        -> France

    Multi-index table:
        Category,Rating,Dec 2011
        NET Upper class,Poor,4
        -> NET Upper class - Poor
    """
    text_parts = []

    for idx, cell in enumerate(row):
        if idx in numeric_cols:
            continue

        if idx >= len(header):
            continue

        value = str(cell).strip()

        if not value:
            continue

        if _is_number(value):
            continue

        col_name = header[idx].strip().lower()

        # Do not include broad grouping columns if there are better text columns.
        # But keep category/rating/country/group because they are meaningful labels.
        if col_name in {"region", "continent", "area"}:
            continue

        text_parts.append(value)

    if text_parts:
        return " - ".join(text_parts[:2])

    if label_col_idx < len(row) and row[label_col_idx].strip():
        return row[label_col_idx].strip()

    return "row"


def _rule_based_summary_from_csv(csv_text: str) -> str:
    """
    Generate a factual chart summary from CSV.

    Improvements:
        - uses Year/Date as label axis when it is the first column
        - avoids using Year/Date as metric columns
        - combines labels for multi-text-column tables
        - handles up to 3 numeric series
        - uses trend only for ordered axes
        - uses spread for categorical axes
    """
    csv_text = (csv_text or "").strip()

    if not csv_text:
        return "The chart data could not be extracted reliably."

    try:
        rows = list(csv.reader(io.StringIO(csv_text)))
    except Exception:
        return "The chart contains data, but the extracted CSV could not be parsed reliably."

    rows = [row for row in rows if any(cell.strip() for cell in row)]

    if len(rows) < 2:
        return "The chart contains limited extracted data."

    header = rows[0]
    data = rows[1:]

    # Remove repeated header rows inside the data.
    data = [
        row for row in data
        if [c.strip().lower() for c in row] != [c.strip().lower() for c in header]
    ]

    if not header or not data:
        return "The chart contains limited extracted data."

    label_col_idx = _choose_label_column(header, data)
    numeric_cols = _choose_numeric_columns(header, data, label_col_idx)

    if not numeric_cols:
        return (
            f"The chart contains {len(data)} extracted data rows, "
            "but no clear numeric metric column was detected."
        )

    label_name = header[label_col_idx] if label_col_idx < len(header) else "category"
    metric_names = [header[idx] for idx in numeric_cols if idx < len(header)]

    sentences = [
        f"The chart compares {', '.join(metric_names)} across {len(data)} {label_name.lower()} entries."
    ]

    is_ordered_axis = _is_ordered_label_axis(label_name)

    for col_idx in numeric_cols[:3]:
        metric_name = header[col_idx] if col_idx < len(header) else "value"

        values = []
        labels = []

        for row in data:
            if col_idx >= len(row):
                continue

            value = _numeric_value(row[col_idx])
            if value is None or math.isnan(value) or math.isinf(value):
                continue

            label = _make_row_label(
                row=row,
                header=header,
                label_col_idx=label_col_idx,
                numeric_cols=numeric_cols,
            )

            values.append(value)
            labels.append(label)

        if len(values) < 2:
            continue

        max_i = max(range(len(values)), key=lambda i: values[i])
        min_i = min(range(len(values)), key=lambda i: values[i])

        max_value = values[max_i]
        min_value = values[min_i]
        max_label = labels[max_i]
        min_label = labels[min_i]

        sentences.append(
            f"For {metric_name}, the highest value is {max_value:g} for {max_label}, while the lowest is {min_value:g} for {min_label}."
        )

        if is_ordered_axis:
            first_value = values[0]
            last_value = values[-1]
            first_label = labels[0]
            last_label = labels[-1]

            if last_value > first_value:
                trend = "increases"
            elif last_value < first_value:
                trend = "decreases"
            else:
                trend = "stays the same"

            sentences.append(
                f"From {first_label} to {last_label}, {metric_name} {trend} from {first_value:g} to {last_value:g}."
            )
        else:
            spread = max_value - min_value
            sentences.append(
                f"The spread for {metric_name} is {spread:g} points between {max_label} and {min_label}."
            )

    return " ".join(sentences[:6])