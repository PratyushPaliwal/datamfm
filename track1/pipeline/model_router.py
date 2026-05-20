"""
Model router for Track 1.

Currently supported:
    - docling

This keeps the Track 1 document parsing pipeline local.
No Claude, no Gemini, no API keys.
"""

import subprocess
import tempfile
from pathlib import Path


def route_page(image_path: Path, config: dict) -> str:
    """
    Route one page image through the configured parser.

    Args:
        image_path: path to one page image
        config: loaded YAML config

    Returns:
        raw Markdown string
    """
    primary = config.get("pipeline", {}).get("primary_model", "docling").lower()

    if primary in ("docling", "docling-cli"):
        return _run_docling(image_path, config)

    raise ValueError(
        f"Unknown primary_model: {primary}. "
        "This router currently supports only 'docling'."
    )


def _run_docling(image_path: Path, config: dict) -> str:
    """
    Run Docling CLI on a single image and return Markdown.

    Requires:
        pip install docling

    Equivalent command:
        docling image.png --to md --output temp_dir
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        cmd = [
            "docling",
            str(image_path),
            "--to",
            "md",
            "--image-export-mode",
            "placeholder",
            "--output",
            str(tmpdir_path),
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Docling failed.\n"
                f"STDOUT:\n{result.stdout}\n\n"
                f"STDERR:\n{result.stderr}"
            )

        md_files = list(tmpdir_path.rglob("*.md"))

        if not md_files:
            raise RuntimeError(
                f"Docling did not generate a Markdown file for {image_path}"
            )

        return md_files[0].read_text(encoding="utf-8").strip()