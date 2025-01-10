# type: ignore
import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = True
import numpy as np
import pandas as pd
import re
import fire


def remove_dates_from_models(models):
    """
    Removes date suffixes (with or without dashes) from a list of model names.
    """
    cleaned_models = [
        re.sub(r"(-\d{4}-\d{2}-\d{2}$|-?\d{8}$)", "", model) for model in models
    ]
    return cleaned_models


def main(eval_path: str = "result.csv", output_path: str = "model_acc.png"):
    # Read the data
    df_all = pd.read_csv(eval_path)

    # filter out the models with Accuracy (pure) < 20 and Accuracy < 40
    df = df_all[(df_all["Accuracy (pure) (%)"] > 20) & (df_all["Accuracy (%)"] > 40)]

    model_names = df["Model"]
    mean_pure = df["Accuracy (pure) (%)"]
    mean = df["Accuracy (%)"]
    n_models = len(model_names)

    # 1. Use the modern approach for getting colormaps in Matplotlib 3.7+
    color_map = plt.colormaps["tab10"].resampled(n_models)
    model_colors = [color_map(i) for i in range(n_models)]

    # 2. Prepare some markers
    marker_candidates = [
        "o",
        "s",
        "^",
        "v",
        "<",
        ">",
        "D",
        "d",
        "*",
        "p",
        "h",
        "H",
        "P",
        "X",
        "+",
        "x",
        "1",
        "2",
        "3",
        "4",
        "|",
        "_",
    ]
    model_markers = [
        marker_candidates[i % len(marker_candidates)] for i in range(n_models)
    ]

    # Quick helper
    unfilled_markers = {"+", "x", "1", "2", "3", "4", "|", "_"}

    plt.figure(figsize=(17, 17))
    cleaned_model_names = remove_dates_from_models(model_names)

    # 3. Plot each model, with filled/unfilled markers
    for x, y, label, color, marker in zip(
        mean_pure, mean, cleaned_model_names, model_colors, model_markers
    ):
        if marker in unfilled_markers:
            plt.scatter(x, y, c=color, marker=marker, s=100)
        else:
            plt.scatter(x, y, facecolor=color, edgecolor="black", marker=marker, s=100)
        # Add text label
        plt.text(x, y, label, fontsize=15, ha="right", va="bottom")

    # plot linear regression line Accuracy v.s. Accuracy (pure)

    # plt.xlabel("Accuracy on Benchmark-F-Pure", fontsize=20)
    plt.xlabel(r"Accuracy on Benchmark-F-$\mathrm{pure}$", fontsize=20)
    plt.ylabel("Accuracy on Benchmark-F", fontsize=20)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    # plt.savefig(output_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    fire.Fire(main)
