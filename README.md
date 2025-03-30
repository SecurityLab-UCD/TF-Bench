# TF-Bench

Towards Sound Evaluation of Program Logic Reasoning with Type Inference under System F

## Setup

### Python

We use Python 3.11.
We recommend using [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage your Python dependencies.

```sh
cd TF-Bench
uv sync # create a virtual environment, and install dependencies
```

## Building TF-Bench From Scratch (Optional)

### Getting Required Data

```sh
./scripts/init.sh
```

This script will download raw data from [Hackage](https://hackage.haskell.org/).

### TF-Bench

This script will build the benchmark (Prelude with NL) from the raw data.

```sh
python scripts/preprocess_benchmark.py -i benchmark/ -o TF-Bench.json
```

### TF-Bench_pure

```sh
git clone https://github.com/SecurityLab-UCD/alpharewrite.git
cd alpharewrite

stack build
stack exec alpharewrite-exe 1 TF-Bench.json > TF-Bench.pure.json
```

For details, please refer to the README of [alpharewrite](https://github.com/SecurityLab-UCD/alpharewrite).

## Download Pre-build Benchmark

You can also download our pre-build benchmark from [Zenodo](https://doi.org/10.5281/zenodo.14751813).

<a href="https://doi.org/10.5281/zenodo.14751813"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.14751813.svg" alt="DOI"></a>

## Benchmarking!

### GPT Models

To run single model:

```sh
export OPENAI_API_KEY=<OPENAI_API_KEY> # make sure your API key is in environment
uv run main.py -i TF-Bench.json -m gpt-3.5-turbo
```

To run all GPT models:

```sh
uv run run_all.py --option gpt
```

### Open Source Models

We use [Ollama](https://ollama.com/) to manange and run the OSS models.

```sh
curl -fsSL https://ollama.com/install.sh | sh # install ollama, you need sudo for this
ollama serve # start your own instance instead of system service
uv run ollama_pull.sh # install required models
```

```sh
uv run main.py -i Benchmark-F.json -m llama3:70b
```

To run all Ollama models:

```sh
uv run run_all.py --option ollama
```
