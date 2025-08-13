# script to pull all ollama models
from tfbench.experiment_ollama import OLLAMA_MODELS
import subprocess
from tqdm import tqdm

if __name__ == "__main__":
    for model in tqdm(OLLAMA_MODELS):
        subprocess.run(
            ["ollama", "pull", model],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
