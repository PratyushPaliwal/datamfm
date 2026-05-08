# DataMFM Challenge — CVPR 2026

Team submission for the [DataMFM Challenge](https://datamfm.github.io/challenge.html) at CVPR 2026.  
**Deadline: May 29, 2026 · Submission via EvalAI**

---

## Team

| Member | Role | GitHub |
|--------|------|--------|
| You | Track 1 — Document Parsing | @you |
| Friend | Track 2 — Chart Understanding | @friend |

---

## Repo Structure

```
datamfm/
├── track1/                  # Document parsing pipeline
│   ├── pipeline/            # Main inference scripts
│   ├── prompts/             # Prompt templates
│   └── postprocess/         # Output cleaning & validation
├── track2/                  # Chart understanding pipeline
│   ├── pipeline/
│   ├── prompts/
│   └── postprocess/
├── scripts/                 # Shared utilities (zip, validate, submit)
├── configs/                 # Model configs, API keys template
├── evaluation/              # Local eval scripts (OmniDocBench + ChartNet)
├── notebooks/               # Exploration & analysis notebooks
├── submission/              # Final zipped outputs (git-ignored)
└── data/                    # Downloaded challenge data (git-ignored)
    ├── doc_pages/           # 1,005 page images in 89 folders
    └── charts/
        ├── real/            # 1,807 real chart images
        └── synthetic/       # 2,000 synthetic chart images
```

---

## Quickstart

### 1. Clone and install

```bash
git clone https://github.com/YOUR_ORG/datamfm.git
cd datamfm
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
cp configs/secrets.template.env configs/secrets.env
# Edit configs/secrets.env — never commit this file
```

### 3. Download challenge data

```bash
# Download from Google Drive links on the challenge page, then place in:
# data/doc_pages/   ← document parsing images
# data/charts/      ← chart images (real/ and synthetic/ subfolders)
```

### 4. Run Track 1 (Document Parsing)

```bash
python track1/pipeline/run.py \
  --input_dir data/doc_pages \
  --output_dir submission/track1 \
  --config configs/track1.yaml
```

### 5. Run Track 2 (Chart Understanding)

```bash
python track2/pipeline/run.py \
  --input_dir data/charts \
  --output_dir submission/track2 \
  --config configs/track2.yaml
```

### 6. Validate outputs locally

```bash
python scripts/validate.py --track 1 --output_dir submission/track1
python scripts/validate.py --track 2 --output_dir submission/track2
```

### 7. Build submission zip

```bash
python scripts/build_submission.py
# Creates submission/submission.zip — upload this to EvalAI
```

---

## Architecture

```
Image(s)
  │
  ├─ Track 1 ──► Layout detection (DocLayout-YOLO)
  │                │
  │                ├─ Text blocks  ──► PaddleOCR-VL
  │                ├─ Tables       ──► RapidTable
  │                └─ Formulas     ──► UniMERNet
  │                │
  │                └─ Post-process ──► sort by bbox, lint HTML, validate LaTeX
  │                │
  │                └─ Output: one .md per page
  │
  └─ Track 2 ──► Chart classifier
                  │
                  ├─ CSV task    ──► Qwen3-VL / Gemini 2.5 Pro
                  └─ Summary task ──► Gemini 2.5 Pro
                  │
                  └─ Post-process ──► validate CSV, enforce numeric precision
                  │
                  └─ Output: chart2csv_predictions.jsonl
                             chart2summary_predictions.jsonl
```

---

## Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable, submission-ready code only |
| `dev` | Integration branch — merge feature branches here first |
| `track1/` | Your work on document parsing |
| `track2/` | Friend's work on chart understanding |

**Workflow:**
1. Branch off `dev` for your work
2. Open a PR into `dev` when ready
3. Merge `dev` → `main` only before a submission

---

## Submission Rules

- Max **3 submissions per day** on EvalAI
- **2 final submissions** count for the leaderboard
- Top teams must submit a **technical report**
- External training data must be **disclosed**

---

## Evaluation Metrics

**Track 1 — Document Parsing**
- Text Edit Distance ↓ (lower = better)
- Table TEDS ↑
- Formula CDM ↑
- Reading Order Edit Distance ↓
- **Overall = ((1 − TextED) × 100 + TableTEDS + FormulaCDM) / 3** ↑

**Track 2 — Chart Understanding**
- CSV Numeric F1 ↑
- CSV Structural Score ↑
- Summary ROUGE-L ↑
- Summary Numeric Fact F1 ↑
- **Overall = average of all four** ↑
