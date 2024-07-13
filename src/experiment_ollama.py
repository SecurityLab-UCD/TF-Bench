import fire
from ollama import Client
from tqdm import tqdm  # Import tqdm for the progress bar
from experiment import get_prompt, SYSTEM_PROMPT
from add_dependency import BenchmarkTask
from dacite import from_dict
import json
import logging
from src.evaluation import evaluate
from src.common import postprocess


def get_model(
    client: Client = Client(host="http://localhost:11434"),
    model: str = "llama3",
    seed=123,
    temperature=0.0,
    top_p=1.0,
):
    def generate_type_signature(prompt: str) -> str | None:
        response = client.chat(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {"role": "user", "content": prompt},
            ],
            model=model,
            options={
                "seed": seed,
                "top_p": top_p,
                "temperature": temperature,
            },
        )

        return response["message"]["content"]

    return generate_type_signature


def main(
    input_file: str = "data/filtered/base-4.20.0.0.jsonl",
    output_file: str | None = None,
    model: str = "llama3",
    seed: int = 123,
    temperature: float = 0.0,
    top_p: float = 1.0,
):

    assert model in [
        "llama3",
        "llama3:70b",
        "phi3",
        "phi3:medium",
        "gemma2",
        "gemma2:27b",
        "mistral",
        "mixtral:8x22b",
        "mixtral:8x7b",
    ], f"{model} is not supported."

    if output_file is None:
        output_file = f"{model}.txt"

    client = Client(host="http://localhost:11434")

    generate = get_model(client, model, seed, temperature, top_p)

    with open(input_file, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    gen_results = []
    with tqdm(total=len(tasks), desc="Processing tasks") as pbar:
        for task in tasks:
            prompt = get_prompt(task)
            generated = generate(prompt)
            processed = postprocess(str(generated))
            gen_results.append(processed)
            pbar.update(1)

    with open(output_file, "w") as file:
        file.write("\n".join(gen_results))

    logging.info(f"Get {len(gen_results)} results from {model}.")
    eval_acc = evaluate(tasks, gen_results)
    print(eval_acc)


if __name__ == "__main__":
    fire.Fire(main)
