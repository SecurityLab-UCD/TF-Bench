import fire
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate


def main(input_csv: str, output_path: str = "corr_matrix.png") -> None:
    """
    Main function to read a CSV file and plot the correlation matrix.

    Args:
        input_file (str): Path to the input CSV file.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    # Compute correlation matrix
    correlation_matrix = df[
        [
            "TFB",
            "TFB_pure",
            "LCB_gen",
            "LCB_repair",
        ]
    ].corr()
    print(tabulate(correlation_matrix, headers="keys", tablefmt="github"))  # type: ignore
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.savefig(output_path)

    # # Plot the correlation matrix
    # plot_correlation_matrix(df, output_path)


if __name__ == "__main__":
    fire.Fire(main)
