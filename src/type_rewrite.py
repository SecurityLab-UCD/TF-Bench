import fire
import os
from src.common import BenchmarkTask
from funcy_chain import Chain
import funcy
import json
from dacite import from_dict


def rewrite_type(task: BenchmarkTask) -> BenchmarkTask:
    # todo: implement type rewriting logic
    return task


def main(
    dataset_path: str = "Benchmark-F.jsonl",
    output_path: str = "Benchmark-F.removed.jsonl",
):

    with open(dataset_path, "r") as fp:
        tasks: list[BenchmarkTask] = (
            Chain(fp.read().splitlines())
            .map(json.loads)
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .map(rewrite_type)
            .value
        )

    with open(output_path, "w") as fp:
        fp.write("\n".join(json.dumps(t.__dict__) for t in tasks))


if __name__ == "__main__":
    fire.Fire(main)
