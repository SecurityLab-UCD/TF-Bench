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
plt.rcParams["font.size"] = 20


def main(output_file: str = "operators.pdf"):
    # order: origional, rewrite NL types, rewrite type variables, rewrite bindings, pure
    acc = {
        "O1-preview": [86.17, 54.79, 87.77, 77.13, 53.72],
        "Claude-3.5-sonnet": [85.46, 43.62, 84.04, 55.85, 48.97],
        "GPT-4-turbo": [83.51, 50.53, 80.85, 59.57, 39.72],
    }

    bars = "None", "NL-Ty", " Ty-Var", "Binding", "Pure"
    x = np.arange(len(bars))
    width = 0.2
    spacing = 0.1

    # plot each model accuracy
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each model's data with edge colors for borders
    ax.bar(
        x - width - spacing / 2,
        acc["O1-preview"],
        width,
        label="O1-preview",
        edgecolor="black",
    )
    ax.bar(
        x, acc["Claude-3.5-sonnet"], width, label="Claude-3.5-sonnet", edgecolor="black"
    )
    ax.bar(
        x + width + spacing / 2,
        acc["GPT-4-turbo"],
        width,
        label="GPT-4-turbo",
        edgecolor="black",
    )

    # Add labels, title, and legend
    ax.set_xlabel("Applied Rewrite Operator")
    ax.set_ylabel("Accuracy (\%)")
    ax.set_xticks(x)
    ax.set_xticklabels(bars)
    ax.legend(title="Models", fontsize="small")

    # Show the grid
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Display the plot
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches="tight", dpi=500)


if __name__ == "__main__":
    fire.Fire(main)
