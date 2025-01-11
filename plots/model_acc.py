import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"
plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        "text.latex.preamble": r"\usepackage{amsmath}",
    }
)

from matplotlib.patches import Ellipse
import numpy as np
import pandas as pd
import re
import fire

# If you don't already have sklearn, install or ensure it's available
from sklearn.decomposition import PCA


def remove_dates_from_models(models):
    """
    Removes date suffixes (with or without dashes) from a list of model names.
    """
    cleaned_models = [
        re.sub(r"(-\d{4}-\d{2}-\d{2}$|-?\d{8}$)", "", model) for model in models
    ]
    return cleaned_models


def main(eval_path: str = "result.xlsx", output_path: str = "model_acc.png"):
    # Read the data
    df = pd.read_excel(eval_path)

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
        plt.text(x, y, label, fontsize=8, ha="right", va="bottom")

    # -----------------------------
    # AUTOMATICALLY-FIT ELLIPSE
    # -----------------------------
    # Gather the points in a NumPy array
    X = np.column_stack((mean_pure, mean))
    pca = PCA(n_components=2)
    pca.fit(X)

    # Center is just the mean of X
    center = X.mean(axis=0)

    # Angle of the ellipse is the angle of the first principal component
    # (We take atan2 of the loadings in the first PCA component)
    angle = np.degrees(np.arctan2(pca.components_[0, 1], pca.components_[0, 0]))

    # Eigenvalues give variances along principal axes;
    # explained_variance_ is the variance, so sqrt(...) gives stdev
    width = 2 * np.sqrt(pca.explained_variance_[0]) * 1.5
    height = 2 * np.sqrt(pca.explained_variance_[1]) * 2

    # Create and add the ellipse
    ellipse_green = Ellipse(
        xy=center,
        width=width,
        height=height,
        angle=angle,
        color="green",
        alpha=0.1,
        label="Aligned Region",
    )
    plt.gca().add_patch(ellipse_green)

    # (Optional) If you still want a "red" ellipse for "Overfitting Region,"
    # just create another ellipse similarly.

    # 4. Adjust axis limits with a bit of padding
    plt.margins(0.1)
    x_min, x_max = min(mean_pure), max(mean_pure)
    y_min, y_max = min(mean), max(mean)
    padding = 0.05
    x_range = x_max - x_min
    y_range = y_max - y_min
    plt.xlim(x_min - x_range * padding, x_max + x_range * padding)
    plt.ylim(y_min - y_range * padding, y_max + y_range * padding)

    # 5. Build legend handles
    handles = []
    for color, marker in zip(model_colors, model_markers):
        if marker in unfilled_markers:
            handle = plt.Line2D(
                [0],
                [0],
                marker=marker,
                color=color,
                markerfacecolor="none",
                markersize=10,
                linewidth=0,
            )
        else:
            handle = plt.Line2D(
                [0],
                [0],
                marker=marker,
                color="black",
                markerfacecolor=color,
                markeredgecolor="black",
                markersize=10,
                linewidth=0,
            )
        handles.append(handle)

    # Append the green ellipse handle
    handles.append(
        Ellipse((0, 0), 1, 1, angle=0, color="green", alpha=0.3, label="Aligned Region")
    )

    plt.legend(
        handles,
        cleaned_model_names + ["Aligned Region"],
        loc="lower right",
        title="Models",
    )

    # plt.xlabel("Accuracy on Benchmark-F-Pure", fontsize=20)
    plt.xlabel(r"Accuracy on Benchmark-F$_{\text{pure}}$", fontsize=20)
    plt.ylabel("Accuracy on Benchmark-F", fontsize=20)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    fire.Fire(main)
