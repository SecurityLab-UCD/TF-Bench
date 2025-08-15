# TF-Bench

Evaluating Program Semantics Reasoning with Type Inference in System _F_

## Setup

### Python

We use Python 3.11.
We recommend using [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage your Python dependencies.

```sh
cd TF-Bench
uv sync # create a virtual environment, and install dependencies
```

## Building TF-Bench From Scratch (Optional)

### TF-Bench

This script will build the benchmark (Prelude with NL) from the raw data.

```sh
uv run scripts/preprocess_benchmark.py
```

### TF-Bench_pure

```sh
git clone https://github.com/SecurityLab-UCD/alpharewrite.git
cd alpharewrite

stack build
stack exec alpharewrite-exe 1 ../tfb.json > ../tfb.pure.json

cd ..
```

For details, please take a look at the README of [alpharewrite](https://github.com/SecurityLab-UCD/alpharewrite).

## Download Pre-built Benchmark

You can also download our pre-built benchmark from [Zenodo](https://doi.org/10.5281/zenodo.14751813).

<a href="https://doi.org/10.5281/zenodo.14751813"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.14751813.svg" alt="DOI"></a>

## Benchmarking!

Please have your API key ready in `.env`.
Please note that the `.env` in the repository is tracked by git,
we recommend telling your git to ignore its changes by

```sh
git update-index --assume-unchanged .env
```

### GPT Models

To run single model:

```sh
export OPENAI_API_KEY=<OPENAI_API_KEY> # make sure your API key is in the environment
uv run main.py -i TF-Bench.json -m gpt-3.5-turbo
```

To run all GPT models:

```sh
uv run run_all.py --option gpt
```

### Open Source Models

We use [Ollama](https://ollama.com/) to manage and run the OSS models.

```sh
curl -fsSL https://ollama.com/install.sh | sh # install ollama, you need sudo for this
ollama serve # start your own instance instead of a system service
uv run --project . scripts/ollama_pull.sh # install required models
```

```sh
uv run main.py -i Benchmark-F.json -m llama3:70b
```

To run all Ollama models:

```sh
uv run run_all.py --option ollama
```
