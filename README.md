# DataMFM Challenge — CVPR 2026

Our submission for the [DataMFM Challenge](https://datamfm.github.io/challenge.html) at CVPR 2026, part of the *Emerging Directions in Data for Multimodal Foundation Models* workshop. The challenge tests whether AI systems can read documents and charts the way a human expert would, reconstructing structured content from raw images.

We competed in both tracks and reached the top 5 on the leaderboard.

---

## What the challenge asked us to do

**Track 1 — Document Parsing.** Given 1,005 page images from academic papers, financial reports, and newspapers, produce a structured Markdown file for each page. Text in Markdown, tables as HTML, formulas as LaTeX. The evaluation measured how accurately we recovered text, table structure, mathematical formulas, and reading order.

**Track 2 — Chart Understanding.** Given 3,807 chart images split into real-world and synthetic samples, produce two outputs per chart: a CSV table of the underlying data, and a natural language summary. Scored on numeric accuracy, structural correctness, text overlap with reference summaries, and how precisely the summaries quoted numbers from the chart.

---

## Track 1 — Document Parsing

We tried Docling first and found it produced near-zero scores on tables and formulas because it outputs Markdown pipe tables rather than HTML, and has no formula extraction at all. We replaced it entirely with MinerU, then switched to PaddleOCR-VL-1.6 for the final submission.

PaddleOCR-VL-1.6 is a 0.9B vision-language model purpose-built for document parsing. It handles layout detection, OCR, table extraction (outputting proper HTML), and formula recognition (outputting LaTeX) in a single pass. The model achieves 96.33% on OmniDocBench v1.6, the same benchmark the challenge dataset is based on.

We ran inference on a university HPC cluster using a SLURM job array, processing both splits overnight. The output required minimal post-processing — we added a normalisation pass for unicode characters and a validation step to catch empty formula blocks before submission.

**Final scores**

| Metric | Score |
|---|---|
| Text Edit Distance | 0.19 |
| Table TEDS | 74.93 |
| Formula CDM | 0.41 |
| Reading Order | 61.12 |
| Overall | 54.24 |

---

## Track 2 — Chart Understanding

This track had a more nuanced problem. Our initial approach using DePlot scored 31 overall because DePlot has no summary capability and its CSV output format is non-standard. We rebuilt the pipeline around a two-step architecture.

**Step 1 — CSV extraction.** We used Granite 4.0 3B Vision, an IBM model fine-tuned specifically on ChartNet (the same dataset the challenge uses). The task tag `<chart2csv>` triggers its specialised extraction behaviour, producing clean comma-separated output with exact numeric values.

**Step 2 — Grounded summary generation.** Rather than generating summaries from the image alone, we fed both the image and the CSV extracted in Step 1 into Qwen2.5-VL 7B. Giving the model the structured data alongside the visual forced it to use exact numbers in its summaries rather than estimating from the image, which directly improved the Numeric Fact F1 score.

The summary format was a significant challenge. Our early submissions scored around 11 on ROUGE-L because we were producing 30-80 word summaries while the ground truth expected 250-350 word comprehensive descriptions covering chart type, axes, every data series with its color, source attribution, and visual design details. Once we aligned our prompt to match that structure the ROUGE-L jumped substantially.

We ran the full pipeline on Google Colab with a T4 GPU, processing the 3,807 charts overnight with resume support built in so disconnections didn't lose progress.

**Final scores**

| Metric | Score |
|---|---|
| CSV Numeric F1 | 65.52 |
| CSV Structural Score | 68.65 |
| Summary ROUGE-L | 11.54 |
| Summary Numeric Fact F1 | 34.77 |
| Overall | 45.12 |

---

## Models used

**PaddleOCR-VL-1.6** (Track 1) — 0.9B document parsing VLM from PaddlePaddle, SOTA on OmniDocBench. Apache 2.0.

**Granite 4.0 3B Vision** (Track 2 CSV) — IBM vision model fine-tuned on ChartNet with dedicated chart2csv and chart2summary task tags. Apache 2.0.

**Qwen2.5-VL 7B** (Track 2 Summary) — Alibaba's vision-language model, strong on structured text generation and visual reasoning.

**MinerU** (Track 1 baseline) — Open-source document parsing pipeline combining DocLayout-YOLO, PaddleOCR, RapidTable, and UniMERNet.

---

## Repository structure

```
datamfm/
  track1/          document parsing pipeline
  track2/          chart understanding pipeline
  evaluation/      local scoring scripts
  configs/         model and pipeline configuration
  hpc/             SLURM job scripts for cluster inference
  scripts/         submission validation and zip builder
```

---

## Team

Pratyush Paliwal and [teammate name] — submitted for CVPR 2026 DataMFM Challenge.
