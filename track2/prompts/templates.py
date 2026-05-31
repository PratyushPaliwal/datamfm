"""
Track 2 prompts — engineered from ground truth analysis.

Key findings from the GT samples:
1. Summaries are LONG (250-330 words) — not 3-5 sentences
2. Start with "This image is a [type] chart..." or "The chart image is a..."
3. Describe: title, axes, ALL series with colors, exact values, source
4. Use numbered lists for multiple series: 1. **Series**: ...
5. CSV preserves exact header text from chart axes/legends
6. CSV uses exact date formats shown (2011-01 not January 2011)
"""

CSV_PROMPT = """You are a precise chart data extractor. Extract ALL data from this chart into CSV format.

RULES:
1. First row: exact column headers from the chart (axis labels, legend text)
2. One row per data point — extract EVERY visible data point
3. NEVER round numbers — preserve exact values (27.2 stays 27.2)
4. NEVER expand abbreviations — chart shows "90 %" write "90 %"
5. Use exact date/label format from chart (2011-01 not "January 2011")
6. Comma delimiter — quote values containing commas
7. NEVER use K/M/B suffixes — write full numbers
8. Output ONLY raw CSV — no explanation, no markdown fences, no title row

Examples:
- Line chart with Date x-axis, metals as series → Date,Aluminium,Zinc,Copper
- Donut chart with scenarios → Scenario,Average Value
- Bar chart with countries → Country,Value"""

SUMMARY_PROMPT = """You are an expert chart analyst. Write a comprehensive detailed description of this chart.

STRUCTURE:
1. Opening: "This image is a [chart type] depicting/showing [topic]. The title is [exact title]."
2. Axes: describe x-axis (labels/range), y-axis (range/units), any reference lines
3. Each data series — use numbered list if multiple:
   "1. **[Series Name]**: Represented by a [color] [line/bar/segment]. [trend with specific values]."
4. Visual elements: labels, legends, colors, annotations, source/publisher if visible
5. Closing: overall layout or key takeaway

RULES:
- Write 250-350 words — be comprehensive
- Include EXACT numeric values from the chart
- Describe colors of each series/segment
- Bold series names: **Aluminium**, **Iron Ore**
- Start with "This image is a" or "The chart image is a"
- Output ONLY the summary text"""

GROUNDED_SUMMARY_PROMPT = """You are an expert chart analyst. Write a comprehensive detailed description of this chart.
The extracted data table below is provided for numeric accuracy — use exact values from it.

Extracted data:
{csv_data}

STRUCTURE:
1. Opening: "This image is a [chart type] depicting [topic]. The title is [exact title from chart]."
2. Axes: x-axis (labels, range), y-axis (range, units), reference lines
3. Each data series/segment — numbered list if multiple:
   "1. **[Name]**: Represented by a [color] [element]. [trend or value using EXACT numbers from table]."
4. Visual elements: labels, legend, annotations, source/publisher if visible
5. Key insight or overall takeaway

RULES:
- Write 250-350 words
- Use EXACT numbers from the extracted data above
- Describe colors of each series/segment
- Bold series/segment names: **Iron Ore**, **Policy-Adjusted**
- Start with "This image is a" or "The chart image is a"
- Output ONLY the summary"""
