"""
Script to run all experiments
"""

from src.experiment import GPT_MODELS, main as run_experiment
from src.experiment_ollama import OLLAMA_MODELS
from src.common import SEED, TEMPERATURE, TOP_P
import fire


def main(
    input_file: str = "Benchmark-F.json",
    option: str = "ollama",
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    top_p: float = TOP_P,
    port: int = 11434,
):
    assert option in ("gpt", "ollama")
    models = GPT_MODELS if option == "gpt" else OLLAMA_MODELS
    for m in models:
        run_experiment(
            input_file=input_file,
            output_file=None,
            model=m,
            seed=seed,
            temperature=temperature,
            top_p=top_p,
            port=port,
        )


if __name__ == "__main__":
    fire.Fire(main)
