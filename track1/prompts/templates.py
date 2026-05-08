"""
Track 1 prompt templates.
All prompts live here so the whole team can iterate on them in one place.
"""

FULL_PAGE_PROMPT = """You are an expert document parser. Convert this document page image into clean, structured Markdown.

STRICT RULES — follow every rule exactly:

1. TEXT
   - Use standard Markdown. Paragraphs separated by double newlines (\\n\\n).
   - Headings: # for h1, ## for h2, ### for h3.
   - Do NOT bold random words inside paragraphs.

2. FORMULAS
   - Display (block) formulas: $$\\n<LaTeX>\\n$$
   - Inline formulas: $<LaTeX>$
   - LaTeX must be valid and compilable. Prefer \\dfrac over \\frac for display formulas.
   - Use \\left( and \\right) for large parentheses.
   - Never write formulas as Unicode (e.g. never write α — write $\\alpha$).

3. TABLES
   - Always use HTML <table> format, never Markdown pipe tables.
   - Use <th> for header cells, <td> for data cells.
   - Use colspan and rowspan for merged cells — never duplicate content.
   - Example:
     <table>
       <tr><th>Model</th><th>Score</th></tr>
       <tr><td>Baseline</td><td>82.3</td></tr>
     </table>

4. READING ORDER
   - Elements MUST appear in the order they are read: top-to-bottom, left-to-right.
   - For two-column layouts: complete the left column first, then the right column.
   - The eval script uses file position as reading order — this is critical.

5. OUTPUT
   - Output ONLY the Markdown content of the page.
   - No preamble, no commentary, no code fences around the output.
   - No "Here is the parsed content:" or similar.
"""

TEXT_ONLY_PROMPT = """Extract only the plain text from this document region.
Output raw text only. No Markdown formatting. No commentary."""

TABLE_PROMPT = """Convert this table image to valid HTML.

Rules:
- Use <table>, <tr>, <th>, <td> tags only.
- <th> for header cells, <td> for data cells.
- Use colspan and rowspan for any merged cells.
- Do not add CSS or class attributes.
- Output ONLY the raw HTML <table>...</table> block, nothing else."""

FORMULA_PROMPT = """Convert this mathematical formula image to LaTeX.

Rules:
- Output ONLY the LaTeX expression, nothing else.
- Do not wrap in $$ or $ delimiters — the caller will add them.
- LaTeX must be valid and compilable.
- Prefer \\dfrac over \\frac for display formulas.
- Use \\left( \\right) for large brackets."""
