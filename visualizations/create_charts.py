"""Generate MeaningGuard result visualizations from the combined results CSV."""

from pathlib import Path

import matplotlib

# Use a non-interactive backend so the script works in headless environments.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "results" / "final_results.csv"
OUTPUT_DIR = PROJECT_ROOT / "visualizations"
RISK_ORDER = ["Low", "Medium", "High"]


def load_results(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    """Load result data and verify the columns required for the charts."""
    results = pd.read_csv(input_path)
    required_columns = {"category", "language", "meaning_loss", "risk"}
    missing = required_columns.difference(results.columns)
    if missing:
        raise ValueError(f"Input CSV is missing required columns: {', '.join(sorted(missing))}")

    results["meaning_loss"] = pd.to_numeric(results["meaning_loss"], errors="coerce")
    results = results.dropna(subset=["category", "language", "meaning_loss", "risk"])
    if results.empty:
        raise ValueError("Input CSV contains no complete rows to chart")
    return results


def create_charts(
    input_path: Path = INPUT_PATH,
    output_dir: Path = OUTPUT_DIR,
) -> None:
    """Generate category, language, risk, and language/category charts."""
    results = load_results(Path(input_path))
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # Plot average meaning loss for each category.
    category_means = results.groupby("category", as_index=False)["meaning_loss"].mean()
    category_means = category_means.sort_values("meaning_loss", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=category_means, x="category", y="meaning_loss", color="steelblue")
    plt.title("Average Meaning Loss by Category")
    plt.xlabel("Category")
    plt.ylabel("Average Meaning Loss")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "category_loss.png", dpi=300)
    plt.close()

    # Compare average meaning loss across translation languages.
    language_means = results.groupby("language", as_index=False)["meaning_loss"].mean()
    plt.figure(figsize=(7, 5))
    sns.barplot(data=language_means, x="language", y="meaning_loss", color="darkcyan")
    plt.title("Average Meaning Loss by Language")
    plt.xlabel("Language")
    plt.ylabel("Average Meaning Loss")
    plt.tight_layout()
    plt.savefig(output_dir / "language_comparison.png", dpi=300)
    plt.close()

    # Show the count of translations in each risk band, including empty bands.
    risk_counts = results["risk"].value_counts().reindex(RISK_ORDER, fill_value=0)
    risk_data = risk_counts.rename_axis("risk").reset_index(name="count")
    plt.figure(figsize=(7, 5))
    sns.barplot(data=risk_data, x="risk", y="count", order=RISK_ORDER, palette="Set2")
    plt.title("Risk Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Translations")
    plt.tight_layout()
    plt.savefig(output_dir / "risk_distribution.png", dpi=300)
    plt.close()

    # Display average meaning loss for every language/category combination.
    heatmap_data = results.pivot_table(
        index="language",
        columns="category",
        values="meaning_loss",
        aggfunc="mean",
    )
    plt.figure(figsize=(max(8, len(heatmap_data.columns) * 1.2), 5))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5)
    plt.title("Average Meaning Loss by Language and Category")
    plt.xlabel("Category")
    plt.ylabel("Language")
    plt.tight_layout()
    plt.savefig(output_dir / "heatmap.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    create_charts()
    print(f"Charts saved to {OUTPUT_DIR}")
