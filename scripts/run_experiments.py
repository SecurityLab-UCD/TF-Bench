"""
Script to run all experiments
"""

from src.experiment import GPT_MODELS, CLAUDE_MODELS, main as run_experiment
from src.experiment_ollama import OLLAMA_MODELS, OLLAMA_LARGE, OLLAMA_SMALL
from src.common import SEED, TEMPERATURE, TOP_P
import fire


def main(
    input_file: str = "Benchmark-F.json",
    output_file: str | None = None,
    option: str = "ollama",
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    top_p: float = TOP_P,
    port: int = 11434,
):
    assert option in ("gpt", "claude", "ollama-all", "ollama-large", "ollama-small")

    models: list[str]
    match option:
        case "gpt":
            models = GPT_MODELS
        case "claude":
            models = CLAUDE_MODELS
        case "ollama-all":
            models = OLLAMA_MODELS
        case "ollama-small":
            models = OLLAMA_SMALL
        case "ollama-large":
            models = OLLAMA_LARGE

    for m in models:
        run_experiment(
            input_file=input_file,
            output_file=output_file,
            model=m,
            seed=seed,
            temperature=temperature,
            top_p=top_p,
            port=port,
        )


if __name__ == "__main__":
    fire.Fire(main)
