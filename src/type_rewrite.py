import fire
import os
from src.common import BenchmarkTask


def main(dataset_path: str = "Benchmark-F.jsonl"):
    dataset_path = os.path.abspath(dataset_path)

    pass


if __name__ == "__main__":
    fire.Fire(main)
