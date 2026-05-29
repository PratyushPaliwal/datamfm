CSV_PROMPT = """Extract all data from this chart into a CSV table.

CRITICAL RULES:
1. Header row first — use the exact axis labels or legend text as column names
2. One row per data point — never skip or merge data points
3. NEVER round numbers — 1247.3 stays 1247.3, never becomes 1247 or 1250
4. NEVER use K/M/B — write 1500000 not 1.5M, write 42300 not 42.3K
5. NEVER use currency symbols — write 42300 not $42,300
6. For percentages keep the % sign: 45.2%
7. For dates use exactly the format shown in the chart
8. Output ONLY the raw CSV — no explanation, no markdown, no title row

Correct example:
Year,Revenue,Profit
2020,1200000,340000
2021,1450000,410000"""

SUMMARY_PROMPT = """Write a factual data-driven summary of this chart.

MANDATORY STRUCTURE — follow this exactly:
Sentence 1: Chart type + topic (e.g. "This bar chart shows annual revenue by region from 2018 to 2023.")
Sentence 2: Highest value — state the EXACT label and EXACT number (e.g. "The highest value was North America in 2023 at 4,250,000.")
Sentence 3: Lowest value — state the EXACT label and EXACT number (e.g. "The lowest was Africa in 2018 at 320,000.")
Sentence 4: Overall trend (e.g. "Revenue grew consistently across all regions, with a compound annual growth rate of approximately 12%.")
Sentence 5: One notable outlier or comparison if visible in the chart.

CRITICAL RULES:
- NEVER round numbers — write exact values as they appear in the chart
- NEVER use K/M/B — write 4250000 not 4.25M
- Include units if shown (%, $, kg etc.)
- Output ONLY the summary — no preamble, no "Here is a summary:"
"""
