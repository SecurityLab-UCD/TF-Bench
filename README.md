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

### Haskell

To run evaluation, you need GHC (the Glasgow Haskell Compiler) installed.
We recommend using [ghcup](https://www.haskell.org/ghcup/) to install.

```sh
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
```

Due to the GHC dependency, the evaluation module currently only supports Linux and macOS.
Our evaluation requires Haskell language extensions [type operators](https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/type_operators.html)
and [impredicative polymorphism](https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/impredicative_types.html),
so we require GHC version >= 9.2.1.
Our evaluation used GHC-9.6.7.

## Building TF-Bench From Scratch (Optional)

### TF-Bench

This script will build the benchmark (Prelude with NL) from the raw data.

```sh
uv run scripts/preprocess_benchmark.py -o tfb.json
```

### TF-Bench_pure

```sh
git clone https://github.com/SecurityLab-UCD/alpharewrite.git
cd alpharewrite

stack build
stack exec alpharewrite-exe 1 ../tfb.json > ../tfb.pure.json

cd ..
```

For details, please check out the README of [alpharewrite](https://github.com/SecurityLab-UCD/alpharewrite).

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

### Open Source Models with Ollama

We use [Ollama](https://ollama.com/) to manage and run the OSS models reported in the Appendix.
We switched to vLLM for better performance and SDK design.
Although the Ollama option is still available,
it is no longer maintained.
We recommend using vLLM instead.

```sh
curl -fsSL https://ollama.com/install.sh | sh # install ollama, you need sudo for this
ollama serve # start your own instance instead of a system service
```

NOTE: we required the ollama version at least 0.9.0 to enable thinking parsers.
We use 0.11.7 for our experiments.

```sh
> ollama --version
ollama version is 0.11.7
```

Run the benchmark.

```sh
uv run scripts/experiment_ollama.py -m llama3:8b
```

### (WIP) Running Your Model with vLLM

#### OpenAI-Compatible Server

First, launch the vLLM OpenAI-Compatible Server (with default values, please check vLLM's doc for setting your own):

```sh
uv run vllm serve openai/gpt-oss-120b --tensor-parallel-size 2 --async-scheduling
```

Then, run the benchmark:

```sh
uv run main.py -i Benchmark-F.json -m vllm_openai_chat_completion
```

NOTE: if you set your API key, host, and port when launching the vLLM server,
please add them to the `.env` file as well.
Please modify `.env` for your vLLM api-key, host, and port.
If they are left empty, the default values ("", "localhost", "8000") will be used.
We do not recommend using the default values on machine connect to the public web,
as they are not secure.

```
VLLM_API_KEY=
VLLM_HOST=
VLLM_PORT=
```
