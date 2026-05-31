"""
Model router for Track 1.

Supported:
    - docling
    - mineru

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

    if primary in {"docling", "docling-cli"}:
        return _run_docling(image_path, config)

    if primary in {"mineru", "mineru-cli"}:
        return _run_mineru(image_path, config)

    raise ValueError(
        f"Unknown primary_model: {primary}. "
        "Supported: docling, mineru."
    )


def _run_docling(image_path: Path, config: dict) -> str:
    """
    Run Docling CLI on a single image and return Markdown.

    Requires:
        pip install docling
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        docling_cmd = config.get("pipeline", {}).get("docling_cmd", "docling")

        cmd = [
            docling_cmd,
            str(image_path),
            "--to",
            "md",
            "--image-export-mode",
            "placeholder",
            "--output",
            str(tmpdir_path),
        ]

        timeout = config.get("pipeline", {}).get("page_timeout", 180)

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Docling failed.\n"
                f"Command: {' '.join(cmd)}\n\n"
                f"STDOUT:\n{result.stdout}\n\n"
                f"STDERR:\n{result.stderr}"
            )

        md_files = list(tmpdir_path.rglob("*.md"))

        if not md_files:
            raise RuntimeError(
                f"Docling did not generate a Markdown file for {image_path}"
            )

        return _read_largest_markdown(md_files)


def _run_mineru(image_path: Path, config: dict) -> str:
    """
    Run MinerU CLI on a single image and return Markdown.

    Requires:
        pip install -U mineru
        mineru-models-download

    Equivalent command:
        mineru -p image.png -o temp_dir
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        mineru_cmd = config.get("pipeline", {}).get("mineru_cmd", "mineru")
        timeout = config.get("pipeline", {}).get("page_timeout", 180)

        cmd = [
            mineru_cmd,
            "-p",
            str(image_path),
            "-o",
            str(tmpdir_path),
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "MinerU failed.\n"
                f"Command: {' '.join(cmd)}\n\n"
                f"STDOUT:\n{result.stdout}\n\n"
                f"STDERR:\n{result.stderr}"
            )

        md_files = list(tmpdir_path.rglob("*.md"))

        if not md_files:
            raise RuntimeError(
                f"MinerU did not generate a Markdown file for {image_path}"
            )

        return _read_largest_markdown(md_files)


def _read_largest_markdown(md_files: list[Path]) -> str:
    """
    Some tools may produce multiple Markdown files.
    The main content file is usually the largest one.
    """
    md_file = max(md_files, key=lambda p: p.stat().st_size)
    return md_file.read_text(encoding="utf-8", errors="ignore").strip()