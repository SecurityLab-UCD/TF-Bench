"""preprocess the raw benchmark data from Markdown files into a json file"""

import json
import os

import fire
from funcy import lmap

from tfbench.common import md2task, BenchmarkTask


def main(input_raw_benchmark_path: str = "benchmark", output_path: str = "tfb.json"):
    """Process pre-extracted tasks from Markdown to JSON"""

    # read in all files ending with .md in the input_raw_benchmark_path
    tasks: list[BenchmarkTask] = []
    files = os.listdir(input_raw_benchmark_path)
    files_w_order = sorted(files)
    for file in files_w_order:
        if not file.endswith(".hs.md"):
            continue
        with open(os.path.join(input_raw_benchmark_path, file), "r") as f:
            data = f.read()

        # convert the markdown file to json
        json_data = md2task(data)
        tasks.append(json_data)

    with open(output_path, "w") as f:
        json.dump(lmap(lambda x: x.__dict__, tasks), f, indent=4)


if __name__ == "__main__":
    fire.Fire(main)
