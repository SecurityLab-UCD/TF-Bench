import tiktoken
import fire
from dacite import from_dict
import json
from funcy_chain import Chain
import pandas

from tfbench.common import BenchmarkTask, get_prompt


def main(input_file="tfb.json"):
    with open(input_file, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]
    # count the max, min, and average token length of the task.code

    enc = tiktoken.encoding_for_model("gpt-4o")
    token_counts = [len(enc.encode(task.signature)) for task in tasks]
    df = pandas.DataFrame(token_counts, columns=["token_count"])
    print(f"max: {df.token_count.max()}")
    print(f"min: {df.token_count.min()}")
    print(f"avg: {df.token_count.mean()}")

if __name__ == "__main__":
    fire.Fire(main)
