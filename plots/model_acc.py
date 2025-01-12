# type: ignore
import matplotlib.pyplot as plt
from matplotlib import markers
import itertools
import numpy as np
import pandas as pd
import re
import fire

plt.rcParams["text.usetex"] = True
plt.style.use("_mpl-gallery")
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["font.size"] = 35


def remove_dates_from_models(models):
    """
    Removes date suffixes (with or without dashes) from a list of model names.
    """
    cleaned_models = [
        re.sub(r"(-\d{4}-\d{2}-\d{2}$|-?\d{8}$)", "", model) for model in models
    ]
    return cleaned_models


def save_legend(
    cleaned_model_names, model_colors, model_markers, legend_path="legend.png"
):
    """
    Save the legend to a separate file.
    """
    plt.figure(figsize=(10, 2))
    markers = [
        plt.Line2D(
            [0],
            [0],
            color=color,
            marker=marker,
            linestyle="",
            markersize=30,
            label=label,
        )
        for label, color, marker in zip(
            cleaned_model_names, model_colors, model_markers
        )
    ]
    plt.legend(
        handles=markers,
        loc="center",
        frameon=False,
        ncol=4,  # Adjust number of columns in the legend
    )
    plt.axis("off")
    plt.savefig(legend_path, dpi=500, bbox_inches="tight")
    plt.close()


def main(input_path: str = "result.csv", output_path: str = "model_acc.png"):
    # Read the data
    df_all = pd.read_csv(input_path)

    # filter out the models with Accuracy (pure) < 20 and Accuracy < 40
    # df = df_all[(df_all["Accuracy (pure) (%)"] > 20) & (df_all["Accuracy (%)"] > 40)]
    df = df_all

    model_names = df["Model"]
    acc_pure = df["Accuracy (pure) (%)"]
    acc = df["Accuracy (%)"]
    n_models = len(model_names)

    # 1. Use the modern approach for getting colormaps in Matplotlib 3.7+
    color_map = plt.colormaps["tab10"].resampled(n_models)
    model_colors = [color_map(i) for i in range(n_models)]

    # Automatically get markers from the Matplotlib marker collection
    # default_markers = itertools.cycle(markers.MarkerStyle.markers.keys())
    # # Replace the manual marker assignment
    # model_markers = [next(default_markers) for _ in range(n_models)]
    default_markers = itertools.cycle(
        ["o", "s", "^", "v", "<", ">", "D", "*", "P", "X"]
    )
    # Replace the manual marker assignment
    model_markers = [next(default_markers) for _ in range(n_models)]

    plt.figure(figsize=(20, 15))
    cleaned_model_names = remove_dates_from_models(model_names)

    # 3. Plot each model, with filled/unfilled markers
    marker_size = 300
    for x, y, label, color, marker in zip(
        acc, acc_pure, cleaned_model_names, model_colors, model_markers
    ):
        plt.scatter(x, y, color=color, marker=marker, s=marker_size)
        # plt.text(x, y, label, ha="right", va="bottom", fontsize=15)

    # plot y = x line
    plt.plot([0, 100], [0, 100], "--", color="grey")

    # scale the axes with df
    plt.ylim(0, 60)
    plt.xlim(0, 90)

    plt.gca().set_aspect("equal", adjustable="box")

    # plt.xlabel("Accuracy on Benchmark-F-Pure", fontsize=20)
    plt.xlabel(r"Acc (\%)")
    plt.ylabel(r"Acc$_\mathrm{pure}$ (\%)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    # plt.show()
    plt.savefig(output_path, dpi=500, bbox_inches="tight")

    save_legend(
        cleaned_model_names,
        model_colors,
        model_markers,
        legend_path=f"legend_{output_path}",
    )


if __name__ == "__main__":
    fire.Fire(main)
