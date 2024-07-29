import fire
import os
from ollama import Client
from tqdm import tqdm  # Import tqdm for the progress bar
from experiment import get_prompt, SYSTEM_PROMPT, INSTRUCT_PROMPT
from add_dependency import BenchmarkTask
from dacite import from_dict
import json
import logging
from src.evaluation import evaluate
from src.postprocessing import postprocess, RESPONSE_STRATEGIES

from typing import Union, Callable


def get_model(
    client: Client = Client(host="http://localhost:11434"),
    model: str = "llama3",
    seed=123,
    temperature=0.2,
    top_p=0.95,
):
    def generate_type_signature(prompt: str) -> Union[str, None]:
        response = client.chat(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {"role": "user", "content": INSTRUCT_PROMPT + "\n\n" + prompt},
            ],
            model=model,
            options={
                "seed": seed,
                "top_p": top_p,
                "temperature": temperature,
            },
        )

        if isinstance(response, dict) and "message" in response:
            message = response["message"]
            if isinstance(message, dict) and "content" in message:
                content = message["content"]
                if isinstance(content, str):
                    return content

        return None

    return generate_type_signature


def main(
    input_file: str = "data/filtered/base-4.20.0.0.jsonl",
    output_file: str | None = None,
    model: str = "llama3",
    seed: int = 123,
    temperature: float = 0.2,
    top_p: float = 0.95,
):

    assert model in [
        "llama2:7b",
        "llama2:13b",
        "llama2:70b",
        "llama3",
        "llama3:70b",
        "phi3",
        "phi3:medium",
        "gemma:2b",
        "gemma:7b",
        "gemma2",
        "gemma2:27b",
        "mistral",
        "mixtral:8x22b",
        "mixtral:8x7b",
        "deepseek-coder-v2:16b",
        "deepseek-coder-v2:236b",
        "codegemma:2b",
        "codegemma:7b",
        "codellama:7b",
        "codellama:13b",
        "codellama:34b",
        "codellama:70b",
        "starcoder2:3b",
        "starcoder2:7b",
        "starcoder2:15b",
        "nous-hermes2:10.7b",
        "nous-hermes2:34b",
        "nous-hermes2-mixtral:8x7b",
        "codestral:22b",
        "stable-code:3b",
        "codeqwen:7b",
        "phind-codellama:34b",
        "granite-code:3b",
        "granite-code:8b",
        "granite-code:20b",
        "granite-code:34b",
        "codebooga:34b",
    ], f"{model} is not supported."

    if output_file is None:
        output_file = f"result/{model}.txt"

    client = Client(host="http://localhost:11434")

    generate = get_model(client, model, seed, temperature, top_p)

    with open(input_file, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    gen_results = []
    with tqdm(total=len(tasks), desc="Processing tasks") as pbar:
        for task in tasks:
            prompt = get_prompt(task)
            generated = generate(prompt)
            processed = postprocess(str(generated), RESPONSE_STRATEGIES)
            gen_results.append(processed)
            pbar.update(1)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as file:
        file.write("\n".join(gen_results))

    logging.info(f"Get {len(gen_results)} results from {model}.")
    eval_acc = evaluate(tasks, gen_results)
    print(eval_acc)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open("evaluation_log.txt", "a") as log_file:
        logging_result = {"model_name": model, **eval_acc}
        log_file.write(f"{logging_result}\n")


if __name__ == "__main__":
    fire.Fire(main)
