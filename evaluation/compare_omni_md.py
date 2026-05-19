from pathlib import Path
from difflib import SequenceMatcher


PRED_DIR = Path("submission/track1_omni_test")
GT_DIR = Path("evaluation/omni_ground_truth_md")


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def main():
    pred_files = sorted(PRED_DIR.glob("*.md"))

    if not pred_files:
        raise RuntimeError(f"No prediction files found in {PRED_DIR}")

    for pred_file in pred_files:
        gt_file = GT_DIR / pred_file.name

        if not gt_file.exists():
            print(f"[MISSING GT] {pred_file.name}")
            continue

        pred_text = pred_file.read_text(encoding="utf-8")
        gt_text = gt_file.read_text(encoding="utf-8")

        score = similarity(pred_text, gt_text)

        pred_tables = pred_text.count("<table")
        gt_tables = gt_text.count("<table")

        pred_formulas = pred_text.count("$$")
        gt_formulas = gt_text.count("$$")

        print(
            f"{pred_file.name}: "
            f"similarity={score:.3f}, "
            f"tables pred/gt={pred_tables}/{gt_tables}, "
            f"formulas pred/gt={pred_formulas}/{gt_formulas}"
        )


if __name__ == "__main__":
    main()