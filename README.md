# Benchmark-F

Towards Sound Evaluation of Program Logic Understanding with System F

## Setup

### Loading Env

```sh
source ./env.sh
```

### Python

We use Python 3.10 or above.
We suggest using virtual environments instead of directly installing the requirements to your system.

1. conda
    ```sh
    conda create --name benchmarkf python=3.10
    conda activate benchmarkf
    ```

2. venv: We provide script to use `venv` in `init.sh`. You have to check your Python version is 3.10.

### Getting Required Data

```sh
./scripts/init.sh # -venv
```

This script will download raw data from [Hackage](https://hackage.haskell.org/),
and install Python packages in `requirements.txt`.

## Building Benchmark-F

### Benchmark-F

This script will build the benchmark (Prelude with NL) from the raw data.

```sh
python scripts/preprocess_benchmark.py -i benchmark/ -o Benchmark-F.json
```

### Benchmark-F_pure

```sh
git clone https://github.com/EYH0602/alpharewrite.git
cd alpharewrite

stack build
stack exec alpharewrite-exe 1 Benchmark-F.json > Benchmark-F.pure.json
```

For details, please refer to the README of [alpharewrite](https://github.com/EYH0602/alpharewrite.git).

### Benchmark-F_extended

ToDo


## Experiments

### GPT Models

To run single model:

```sh
export OPENAI_API_KEY=<OPENAI_API_KEY> # make sure your API key is in environment
python3 src/experiment.py -i Benchmark-F.json -m gpt-3.5-turbo
```

To run all GPT models:

```sh
python3 scripts/run_experiments.py --option gpt
```

### Open Source Models

We use [Ollama](https://ollama.com/) to manange and run the OSS models.

```sh
curl -fsSL https://ollama.com/install.sh | sh # install ollama, you need sudo for this
ollama serve # start your own instance instead of system service
python3 scripts/ollama_pull.sh # install required models
```

```sh
python3 src/experiment.py -i Benchmark-F.json -m llama3
```

To run all Ollama models:

```sh
python3 scripts/run_experiments.py --option ollama
```