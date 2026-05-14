"""
Track 2 model runners — CSV extraction and summary generation.
Supports: openrouter (free), gemini, claude
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
    model = config["pipeline"].get("csv_model", "meta-llama/llama-4-scout:free")
    from track2.prompts.templates import CSV_PROMPT
    if "gemini" in model:
        return _gemini(image_path, CSV_PROMPT, model)
    elif "claude" in model:
        return _claude(image_path, CSV_PROMPT)
    else:
        return _openrouter(image_path, CSV_PROMPT, model)


def generate_summary(image_path: Path, config: dict) -> str:
    model = config["pipeline"].get("summary_model", "meta-llama/llama-4-scout:free")
    from track2.prompts.templates import SUMMARY_PROMPT
    if "gemini" in model:
        return _gemini(image_path, SUMMARY_PROMPT, model)
    elif "claude" in model:
        return _claude(image_path, SUMMARY_PROMPT)
    else:
        return _openrouter(image_path, SUMMARY_PROMPT, model)


def _openrouter(image_path: Path, prompt: str, model_name: str) -> str:
    """Call any OpenRouter model (free or paid) using OpenAI-compatible SDK."""
    from openai import OpenAI
    img_data, media_type = encode_image(image_path)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:{media_type};base64,{img_data}"
                }},
            ],
        }],
        max_tokens=2048,
    )
    return response.choices[0].message.content


def _gemini(image_path: Path, prompt: str, model_name: str) -> str:
    from google import genai
    import PIL.Image
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    img = PIL.Image.open(image_path)
    response = client.models.generate_content(
        model=model_name,
        contents=[prompt, img],
    )
    return response.text


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