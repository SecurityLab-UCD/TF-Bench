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
plt.rcParams["font.size"] = 25


def remove_dates_from_models(models):
    """
    Removes date suffixes (with or without dashes) from a list of model names.
    """
    cleaned_models = [
        re.sub(r"(-\d{4}-\d{2}-\d{2}$|-?\d{8}$)", "", model) for model in models
    ]
    return cleaned_models


def main(input_path: str = "result.csv", output_path: str = "model_acc.png"):
    # Read the data
    df_all = pd.read_csv(input_path)

    # filter out the models with Accuracy (pure) < 20 and Accuracy < 40
    df = df_all[(df_all["Accuracy (pure) (%)"] > 20) & (df_all["Accuracy (%)"] > 40)]

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

    # Quick helper
    unfilled_markers = {"+", "x", "1", "2", "3", "4", "|", "_"}

    plt.figure(figsize=(20, 15))
    cleaned_model_names = remove_dates_from_models(model_names)

    # 3. Plot each model, with filled/unfilled markers
    marker_size = 200
    for x, y, label, color, marker in zip(
        acc_pure, acc, cleaned_model_names, model_colors, model_markers
    ):
        if marker in unfilled_markers:
            plt.scatter(x, y, color=color, marker=marker, s=marker_size)
        else:
            plt.scatter(
                x, y, facecolor=color, edgecolor="black", marker=marker, s=marker_size
            )
        # Add text label
        plt.text(x, y, label, ha="right", va="bottom", fontsize=15)

    # plot linear regression line Accuracy v.s. Accuracy (pure)
    x = np.array(df_all["Accuracy (pure) (%)"])
    y = np.array(df_all["Accuracy (%)"])
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, "-", color="grey")

    # scale the axes with df
    plt.xlim(15, 55)
    plt.ylim(55, 90)

    # add legend of model plots
    # plt.legend(cleaned_model_names)
    plt.legend(
        cleaned_model_names,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.08),
        fancybox=True,
        shadow=True,
        ncol=6,
        fontsize=20,
    )

    # add indicator lines
    # Calculate points on the regression line
    arrow_x = 35
    arrow_y = m * arrow_x + b

    # Perpendicular slope to the regression line
    perp_slope = -1 / m

    # Define arrow lengths
    arrow_length = 10

    # Arrow 1 (near x1, y1)
    arrow_dx1 = arrow_length / (1 + perp_slope**2) ** 0.5
    arrow_dy1 = perp_slope * arrow_dx1
    plt.arrow(
        arrow_x,
        arrow_y,
        arrow_dx1,
        arrow_dy1,
        color="green",
        width=0.1,
        head_width=0.5,
        alpha=0.5,
    )
    plt.text(
        arrow_x + arrow_dx1 + 1,
        arrow_y + arrow_dy1 - 1,
        "Tend to answer\n by reasoning",
        color="green",
        ha="left",
        va="bottom",
    )

    # Arrow 2 (near x2, y2)
    arrow_dx2 = arrow_length / (1 + perp_slope**2) ** 0.5
    arrow_dy2 = perp_slope * arrow_dx2
    plt.arrow(
        arrow_x,
        arrow_y,
        -arrow_dx2,
        -arrow_dy2,
        color="red",
        width=0.1,
        head_width=0.5,
        alpha=0.5,
    )
    plt.text(
        arrow_x - arrow_dx2 - 4,
        arrow_y - arrow_dy2 + 3,
        "Tend to answer by \n connecting superficial memory",
        color="red",
        ha="left",
        va="top",
    )

    # plt.xlabel("Accuracy on Benchmark-F-Pure", fontsize=20)
    plt.xlabel(r"Acc$_\mathrm{pure}$ (\%)")
    plt.ylabel(r"Acc (\%)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    # plt.show()
    plt.savefig(output_path, dpi=500, bbox_inches="tight")


if __name__ == "__main__":
    fire.Fire(main)
