import fire
import funcy
from funcy_chain import Chain
import logging
import json
from dacite import from_dict
from dataclasses import dataclass


@dataclass
class BenchmarkTask:
    task_id: str
    signature: str
    code: str
    poly_type: str
    dependencies: str | None


def build_dependency_dict(tasks: list[BenchmarkTask]) -> dict[str, str]:
    return {}


def get_dependencies(dependency_dict: dict[str, str]):
    def get_for_task(task: BenchmarkTask) -> list[str]:
        return []

    return get_for_task


def main(input_file: str, output_file: str):
    with open(input_file, "r") as fp:
        tasks: list[BenchmarkTask] = (
            Chain(fp.readlines())
            .map(json.loads)
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .value
        )

    dependency_dict = build_dependency_dict(tasks)
    tasks_w_dep = (
        Chain(tasks).map(get_dependencies(dependency_dict)).map(json.dumps).value
    )
    with open(output_file, "w") as fp:
        fp.write("\n".join(tasks_w_dep))


if __name__ == "__main__":
    fire.Fire(main)
