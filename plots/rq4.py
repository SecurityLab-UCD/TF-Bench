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


def main():
    # order: origional, rewrite NL types, rewrite type variables, rewrite bindings, pure
    acc = {
        "O1-preview": [86.17, 54.79, 87.77, 77.13, 53.72],
        "Claude-3.5-sonnet": [85.46, 43.62, 84.04, 55.85, 48.97],
        "GPT-4-turbo": [83.51, 50.53, 80.85, 59.57, 39.72],
    }

    bars = "None", "NL-Ty", " Vars", "Binding", "Pure"
    x = np.arange(len(bars))
    width = 0.25

    # plot each model accuracy


if __name__ == "__main__":
    fire.Fire(main)
