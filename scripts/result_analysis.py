"""find the average and std error of multiple runs"""

import fire
import json
import pandas as pd


def main(
    input_evaluation_log_path: str = "evaluation_log.jsonl",
    output_path: str = "evaluation_results.json",
):
    with open(input_evaluation_log_path, "r") as f:
        logs = f.readlines()
    results = [json.loads(log) for log in logs]

    result_dict: dict[str, list[float]] = {}
    for result in results:
        model_name = result["model_name"]
        if model_name not in result_dict:
            result_dict[model_name] = []
        result_dict[model_name].append(result["accuracy"])

    df = pd.DataFrame(result_dict)
    # sort df by mean
    df = df.reindex(df.mean().sort_values(ascending=False).index, axis=1)

    results = [
        {
            "model_name": model_name,
            "mean": df[model_name].mean(),
            "std_error": df[model_name].std(),
        }
        for model_name in df.columns
    ]

    with open(output_path, "w") as f:
        json.dump({"num_runs": len(df), "results": results}, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main)
