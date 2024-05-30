import fire
import funcy
from funcy_chain import Chain
import logging
import json
from dacite import from_dict
from dataclasses import dataclass
from src.filter2complete import extract_function_name


@dataclass
class BenchmarkTask:
    task_id: str
    signature: str
    code: str
    poly_type: str
    dependencies: str | None


def build_dependency_dict(tasks: list[BenchmarkTask]) -> dict[str, str]:
    return {
        fn_name: t.signature
        for t in tasks
        if (fn_name := extract_function_name(t.task_id)) is not None
    }


def get_dependencies(dependency_dict: dict[str, str]):
    def get_for_task(task: BenchmarkTask) -> list[str]:
        return []

    return get_for_task


def main(
    input_file: str = "data/source/base-4.20.0.0.jsonl",
    output_file: str = "out.jsonl",
):
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
