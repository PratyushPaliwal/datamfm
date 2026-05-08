"""Tests for post-processing — no API keys needed."""
import sys
sys.path.insert(0, '.')

from track1.postprocess.cleaner import clean_markdown
from track2.postprocess.cleaner import clean_csv, clean_summary

CONFIG_T1 = {"postprocess": {"normalise_text": True, "lint_html_tables": True, "validate_latex": True}}
CONFIG_T2 = {"postprocess": {"min_numbers_in_summary": 3}}

def test_strip_code_fences():
    raw = "```markdown\n# Title\n\nText\n```"
    result = clean_markdown(raw, CONFIG_T1)
    assert "```" not in result
    assert "# Title" in result

def test_normalise_quotes():
    raw = "It\u2019s a \u201chello\u201d world"
    result = clean_markdown(raw, CONFIG_T1)
    assert "\u2019" not in result
    assert "\u201c" not in result

def test_csv_parses():
    raw = "Year,Value\n2020,100\n2021,200"
    result = clean_csv(raw, CONFIG_T2)
    assert "Year" in result
    assert "2020" in result

def test_csv_strips_fences():
    raw = "```csv\nYear,Value\n2020,100\n```"
    result = clean_csv(raw, CONFIG_T2)
    assert "```" not in result

def test_summary_strips_fences():
    raw = "```\nThe bar chart shows revenue growing from $1.2M in 2020 to $3.4M in 2023.\n```"
    result = clean_summary(raw, CONFIG_T2)
    assert "```" not in result
    assert "bar chart" in result
