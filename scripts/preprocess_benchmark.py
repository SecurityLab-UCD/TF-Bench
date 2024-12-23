"""preprocess the raw benchmark data from Markdown files into a json file"""

import json
import os
import markdown_to_json
import fire
from src.common import md2task, BenchmarkTask
from funcy import lmap


def main(raw_benchmark_path: str = "benchmark", output_path: str = "Benchmark-F.json"):

    # read in all files ending with .md in the raw_benchmark_path
    tasks: list[BenchmarkTask] = []
    for file in os.listdir(raw_benchmark_path):
        if not file.endswith(".core.md"):
            continue
        with open(os.path.join(raw_benchmark_path, file), "r") as f:
            data = f.read()

        # convert the markdown file to json
        json_data = md2task(data)
        tasks.append(json_data)

    with open(output_path, "w") as f:
        json.dump(lmap(lambda x: x.__dict__, tasks), f, indent=4)


if __name__ == "__main__":
    fire.Fire(main)
