"""
Script to run all experiments
"""

from src.experiment import GPT_MODELS, CLAUDE_MODELS, O1_MODELS
from src.experiment_ollama import OLLAMA_MODELS, OLLAMA_OSS, OLLAMA_CODE
from src.common import SEED, TEMPERATURE
from main import main as run_experiment
import fire
import sys


def main(
    input_file: str = "Benchmark-F.removed.json",
    log_file: str | None = None,
    option: str = "gpt",
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    repeat: int = 1,
    pure: bool = False,
):

    port: int = 11434
    models: list[str]
    match option:
        case "gpt":
            models = GPT_MODELS
        case "o1":
            models = O1_MODELS
        case "claude":
            models = CLAUDE_MODELS
        case "ollama-all":
            models = OLLAMA_MODELS
        case "ollama-oss":
            models = OLLAMA_OSS
        case "ollama-code":
            models = OLLAMA_CODE
        case "api":
            models = GPT_MODELS + CLAUDE_MODELS
        case _:
            print(f"Invalid option: {option}", file=sys.stderr)
            sys.exit(1)

    for _ in range(repeat):
        for m in models:
            run_experiment(
                input_file=input_file,
                output_file=None,
                model=m,
                seed=seed,
                temperature=temperature,
                port=port,
                log_file=log_file,
                pure=pure,
            )


if __name__ == "__main__":
    fire.Fire(main)
