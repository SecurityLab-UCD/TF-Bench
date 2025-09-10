from typing import get_args
import os

import fire
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pokepalette

from tfbench.error_analysis import ErrorCategories

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
FONT_SIZE = 20

# CMAP = pokepalette.get_colormap("lapras")
CMAP = pokepalette.get_colormap("gengar")


def plot_error_categories_pie_charts(df: pd.DataFrame):
    """
    Plot pie charts showing the proportion of error categories by split and model.

    Args:
        df: pandas DataFrame containing ErrorAnalysisResult data
    """
    # Get unique models and splits
    models = sorted(df["model"].unique())
    splits = ["base", "pure"]  # Ensure consistent ordering

    # Set up the subplot grid
    n_models = len(models)
    fig, axes = plt.subplots(2, n_models, figsize=(5 * n_models, 10))

    # Handle case where there's only one model (axes won't be 2D)
    if n_models == 1:
        axes = axes.reshape(-1, 1)

    # Define colors for consistency across plots
    error_categories = list(get_args(ErrorCategories))
    colors = CMAP(np.linspace(0, 1, len(error_categories)))
    color_map = dict(zip(error_categories, colors))

    # Create pie charts for each split-model combination
    for split_idx, split in enumerate(splits):
        for model_idx, model in enumerate(models):
            # Filter data for current split and model
            subset = df[(df["split"] == split) & (df["model"] == model)]

            if len(subset) == 0:
                # Handle empty subset
                axes[split_idx, model_idx].text(
                    0.5,
                    0.5,
                    "No Data",
                    ha="center",
                    va="center",
                    transform=axes[split_idx, model_idx].transAxes,
                )
                axes[split_idx, model_idx].set_title(f"{model} ({split})")
                continue

            # Count error categories and ensure consistent ordering
            error_counts = subset["error_category"].value_counts()

            # Prepare data for pie chart with consistent ordering
            labels = []
            sizes = []
            plot_colors = []

            for category in error_categories:
                if category in error_counts:
                    labels.append(category)
                    sizes.append(error_counts[category])
                    plot_colors.append(color_map[category])

            # Create pie chart (without labels and autopct since we'll add custom percentages)
            wedges = axes[split_idx, model_idx].pie(
                sizes,
                colors=plot_colors,
                startangle=90,
            )[0]

            # Calculate percentages
            total = sum(sizes)
            percentages = [(size / total) * 100 for size in sizes]

            # Add percentage labels only for slices >= 5%
            for i, (wedge, pct) in enumerate(zip(wedges, percentages)):
                if pct >= 5:  # Only show percentage if >= 5%
                    # Get wedge center angle
                    angle = (wedge.theta2 + wedge.theta1) / 2

                    # Place inside the pie slice
                    radius = 0.7

                    # Calculate text position
                    x = radius * np.cos(np.radians(angle))
                    y = radius * np.sin(np.radians(angle))

                    # Add percentage text
                    axes[split_idx, model_idx].text(
                        x,
                        y,
                        f"{pct:.1f}%",
                        ha="center",
                        va="center",
                        fontweight="bold",
                        fontsize=10,
                        color="black",
                    )

    # Add model names as column headers (only on top row)
    for model_idx, model in enumerate(models):
        axes[0, model_idx].set_title(model, fontsize=FONT_SIZE)

    # Add split names as row labels (only on leftmost column)
    for split_idx, split in enumerate(splits):
        axes[split_idx, 0].text(
            -0.03,
            0.5,
            split.upper(),
            transform=axes[split_idx, 0].transAxes,
            fontsize=FONT_SIZE,
            ha="center",
            va="center",
            rotation=90,
        )

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(
        top=0.93,
        wspace=-0.15,  # controls the space between columns
        hspace=-0.1,  # controls the space between rows
    )

    # Add legend with all error categories that appear anywhere in the data
    all_categories_in_data = set(df["error_category"].unique())

    # Create legend for all categories that appear in the data, in consistent order
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, fc=color_map[cat])
        for cat in error_categories
        if cat in all_categories_in_data
    ]
    legend_labels_filtered = [
        cat for cat in error_categories if cat in all_categories_in_data
    ]

    fig.legend(
        legend_elements,
        legend_labels_filtered,
        loc="center",
        bbox_to_anchor=(0.5, 0.02),
        ncol=min(4, len(legend_labels_filtered)),
        fontsize=16,
    )

    return fig


def main(
    error_analysis_file_dir: str,
    output_file: str = "error_analysis_pie_charts.png",
):
    # Example usage:
    # Assuming your DataFrame is called 'df'
    files = [
        os.path.join(error_analysis_file_dir, f)
        for f in os.listdir(error_analysis_file_dir)
        if f.endswith(".jsonl")
    ]
    df = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
    fig = plot_error_categories_pie_charts(df)

    fig.savefig(output_file, dpi=500, bbox_inches="tight")


if __name__ == "__main__":
    fire.Fire(main)
