import fire
import json


def count_type(tasks: list[dict[str, str]], type: str) -> int:
    return len([task for task in tasks if task["poly_type"] == type])


def main(dataset_path: str = "Benchmark-F.json"):
    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    mono = count_type(dataset, "Monomorphic")
    para = count_type(dataset, "Parametric")

    print(f"Monomorphic: {mono}")
    print(f"Polymorphic: {para}")


if __name__ == "__main__":
    fire.Fire(main)
