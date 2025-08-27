import os
import fire
from datasets.load import load_dataset


def main(base_path: str = "tfb.json", pure_path: str = "tfb.pure.json"):
    """load TF-Bench from local JSON and upload to HuggingFace Hub
    To run this script, you need:
    1. Build the base version of TF-Bench
    2. Build the pure version of TF-Bench
    3. login in to HuggingFace Hub with your HF_TOKEN
    """
    base_path = os.path.abspath(base_path)
    pure_path = os.path.abspath(pure_path)
    dataset = load_dataset(
        "json",
        data_files={"base": base_path, "pure": pure_path},
    )
    print(dataset)

    base = dataset["base"]
    pure = dataset["pure"]

    assert len(base) == 188  # type: ignore
    assert len(base) == len(pure), "Base and pure datasets must have the same length"  # type: ignore

    dataset.push_to_hub("SecLabUCD/TF-Bench")


if __name__ == "__main__":
    fire.Fire(main)
