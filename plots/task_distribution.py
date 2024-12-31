# type: ignore
import fire
import matplotlib.pyplot as plt
import json
import seaborn as sns

COLOR_PALETTE = sns.color_palette("Set2")


def plot_task_distribution(
    benchmark: list[dict], output_path: str = "task_distribution.pdf"
):
    """Each task is
        {
        "task_id": "data/repos/ghc/libraries/ghc-prim/GHC/Classes.hs--(==)",
        "poly_type": "Ad-hoc",
        "signature": "(==) :: Eq a => a -> a -> Bool",
        "code": "x == y = not (x /= y)",
        "dependencies": [
            "not :: Bool -> Bool",
            "(/=) :: Eq a => a -> a -> Bool"
        ]
    },
    plot a pie chart of the distribution of task types
    """
    task_types = {}
    for task in benchmark:
        task_type = task["poly_type"].strip()
        if task_type in task_types:
            task_types[task_type] += 1
        else:
            task_types[task_type] = 1

    fig, ax = plt.subplots()
    ax.pie(
        task_types.values(),
        labels=task_types.keys(),
        autopct="%1.1f%%",
        colors=COLOR_PALETTE,
    )
    ax.axis("equal")
    plt.savefig(output_path, bbox_inches="tight", dpi=500)


def main(benchmark_path: str, output_path: str = "task_distribution.pdf"):
    with open(benchmark_path) as f:
        benchmark = json.load(f)

    plot_task_distribution(benchmark, output_path)


if __name__ == "__main__":
    fire.Fire(main)
