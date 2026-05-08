"""Track 2 prompt templates."""

CSV_PROMPT = """You are an expert chart data extractor. Convert the data in this chart image to a clean CSV.

STRICT RULES:
1. First row must be the header row with column names.
2. Use comma as delimiter. Quote values containing commas with double quotes.
3. NEVER round, abbreviate, or paraphrase numbers. If the chart shows 1,247.3 → output 1247.3 exactly.
4. NEVER use K, M, B suffixes — write the full number (e.g. 1500000 not 1.5M).
5. For dates/years use the format shown in the chart.
6. Output ONLY the raw CSV text — no explanation, no markdown fences, no preamble.

Example output:
Year,Revenue,Profit
2020,1200000,340000
2021,1450000,410000
"""

SUMMARY_PROMPT = """You are an expert chart analyst. Write a concise, grounded summary of this chart.

STRICT RULES:
1. State the chart type in the first sentence (bar chart, line chart, pie chart, scatter plot, etc.).
2. You MUST include the exact numeric values for:
   - The highest data point (name + value)
   - The lowest data point (name + value)
   - The overall trend or key insight
   - Any notable outlier or turning point
3. Write in flowing prose — no bullet points, no lists.
4. Keep it to 3–5 sentences.
5. NEVER round or paraphrase numbers. Write exact values as shown in the chart.
6. Output ONLY the summary text — no preamble like "This chart shows..." at the very start.
   Begin directly with the chart type and topic.

Example:
"The bar chart compares annual revenue across five product categories from 2019 to 2023.
Electronics led with $4.2M in 2023, while Stationery had the lowest revenue at $0.8M the same year.
Overall revenue grew steadily at approximately 12% per year, with a notable dip in 2020
when total revenue fell to $8.1M due to supply chain disruptions."
"""
