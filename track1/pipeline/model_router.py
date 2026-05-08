"""
Model router for Track 1.
Decides which model handles each element type on a page.
Extend this file to plug in new models.
"""

import base64
import os
from pathlib import Path

import anthropic


def encode_image(image_path: Path) -> tuple[str, str]:
    suffix = image_path.suffix.lower()
    media_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".png": "image/png", ".webp": "image/webp"}
    media_type = media_map.get(suffix, "image/jpeg")
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, media_type


def route_page(image_path: Path, config: dict) -> str:
    """
    Route a full page image through the configured pipeline.
    Returns raw markdown string.
    
    Currently: single-model full-page approach.
    TODO: integrate DocLayout-YOLO to crop elements and route each separately.
    """
    primary = config["pipeline"].get("primary_model", "claude")

    if primary in ("claude", "claude-opus"):
        return _run_claude(image_path, config)
    elif primary in ("gemini", "gemini-2.5-pro"):
        return _run_gemini(image_path, config)
    else:
        return _run_claude(image_path, config)


def _run_claude(image_path: Path, config: dict) -> str:
    from track1.prompts.templates import FULL_PAGE_PROMPT

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    img_data, media_type = encode_image(image_path)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": img_data,
                }},
                {"type": "text", "text": FULL_PAGE_PROMPT},
            ],
        }],
    )
    return message.content[0].text


def _run_gemini(image_path: Path, config: dict) -> str:
    """Gemini 2.5 Pro via Google Generative AI SDK."""
    import google.generativeai as genai
    from track1.prompts.templates import FULL_PAGE_PROMPT

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-pro")

    import PIL.Image
    img = PIL.Image.open(image_path)
    response = model.generate_content([FULL_PAGE_PROMPT, img])
    return response.text
