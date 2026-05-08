"""
Track 1 post-processing.
Cleans raw model output to maximise eval scores.
"""

import re
from bs4 import BeautifulSoup


def clean_markdown(raw: str, config: dict) -> str:
    """Apply all post-processing steps to raw markdown output."""
    text = raw.strip()

    # Strip markdown code fences if model wrapped output
    text = _strip_code_fences(text)

    if config.get("postprocess", {}).get("normalise_text", True):
        text = _normalise_text(text)

    if config.get("postprocess", {}).get("lint_html_tables", True):
        text = _lint_html_tables(text)

    if config.get("postprocess", {}).get("validate_latex", True):
        text = _validate_latex_blocks(text)

    return text


def _strip_code_fences(text: str) -> str:
    """Remove ```markdown ... ``` or ```html ... ``` wrappers."""
    text = re.sub(r"^```(?:markdown|md|html)?\s*\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n```\s*$", "", text, flags=re.MULTILINE)
    return text.strip()


def _normalise_text(text: str) -> str:
    """Normalise unicode characters that hurt edit distance."""
    replacements = {
        "\u2019": "'",   # right single quote → apostrophe
        "\u2018": "'",   # left single quote → apostrophe
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2013": "-",   # en dash
        "\u2014": "--",  # em dash
        "\u00a0": " ",   # non-breaking space
        "\ufeff": "",    # BOM
        "\u2022": "-",   # bullet → hyphen (consistent list marker)
        "\u2023": "-",
        "\u25e6": "-",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)

    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _lint_html_tables(text: str) -> str:
    """
    Find all <table>...</table> blocks and validate/repair them.
    Malformed HTML tables score 0 on TEDS — better to have a plain text fallback.
    """
    def fix_table(match):
        raw_table = match.group(0)
        try:
            soup = BeautifulSoup(raw_table, "lxml")
            table = soup.find("table")
            if table:
                return str(table)
        except Exception:
            pass
        # If we can't fix it, return as-is (don't silently drop it)
        return raw_table

    return re.sub(r"<table[\s\S]*?</table>", fix_table, text, flags=re.IGNORECASE)


def _validate_latex_blocks(text: str) -> str:
    """
    Find all $$...$$ blocks and check they are non-empty.
    Replace empty or obviously broken blocks with a placeholder comment.
    """
    def check_display(match):
        content = match.group(1).strip()
        if not content:
            return "<!-- empty formula removed -->"
        # Basic sanity: must have at least one letter or digit
        if not re.search(r"[a-zA-Z0-9]", content):
            return "<!-- invalid formula removed -->"
        return f"$$\n{content}\n$$"

    text = re.sub(r"\$\$\s*([\s\S]*?)\s*\$\$", check_display, text)
    return text
