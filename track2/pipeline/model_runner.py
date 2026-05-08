"""
Track 2 model runners — CSV extraction and summary generation.
"""

import base64
import os
from pathlib import Path


def encode_image(image_path: Path) -> tuple[str, str]:
    suffix = image_path.suffix.lower()
    media_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".png": "image/png", ".webp": "image/webp"}
    media_type = media_map.get(suffix, "image/jpeg")
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, media_type


def extract_csv(image_path: Path, config: dict) -> str:
    """Extract chart data as CSV."""
    model = config["pipeline"].get("csv_model", "gemini-2.5-pro")
    from track2.prompts.templates import CSV_PROMPT

    if "gemini" in model:
        return _gemini(image_path, CSV_PROMPT, config)
    elif "claude" in model:
        return _claude(image_path, CSV_PROMPT)
    else:
        return _gemini(image_path, CSV_PROMPT, config)


def generate_summary(image_path: Path, config: dict) -> str:
    """Generate grounded natural language summary."""
    model = config["pipeline"].get("summary_model", "gemini-2.5-pro")
    from track2.prompts.templates import SUMMARY_PROMPT

    if "gemini" in model:
        return _gemini(image_path, SUMMARY_PROMPT, config)
    elif "claude" in model:
        return _claude(image_path, SUMMARY_PROMPT)
    else:
        return _gemini(image_path, SUMMARY_PROMPT, config)


def _claude(image_path: Path, prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    img_data, media_type = encode_image(image_path)
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {
                "type": "base64", "media_type": media_type, "data": img_data,
            }},
            {"type": "text", "text": prompt},
        ]}],
    )
    return message.content[0].text


def _gemini(image_path: Path, prompt: str, config: dict) -> str:
    import google.generativeai as genai
    import PIL.Image
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model_name = config["pipeline"].get("csv_model", "gemini-2.5-pro")
    model = genai.GenerativeModel(model_name)
    img = PIL.Image.open(image_path)
    response = model.generate_content([prompt, img])
    return response.text
