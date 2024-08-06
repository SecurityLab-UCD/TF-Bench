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
./init.sh # -venv
```

This script will download raw data from [Hackage](https://hackage.haskell.org/),
and install Python packages in `requirements.txt`.

## Building Benchmark-F

```sh
./run.sh
```

## Experiments

```sh
mkdir -p data/experiment
```

### GPTs

```sh
python3 src/experiment.py -o data/experiment/gpt_generated_responses.jsonl -m gpt-3.5-turbo -a <OPENAI_API_KEY>
```

### Open Source Models

We use [Ollama](https://ollama.com/) to manange and run the OSS models.
```sh
curl -fsSL https://ollama.com/install.sh | sh # install ollama, you need sudo for this
ollama serve # start your own instance instead of system service
./ollama_pull.sh # pull the required models
```


```sh
python3 src/experiment.py -o data/experiment/llama_generated_responses.jsonl -m llama3-8b-8192 -a "please replace with your groq api key" # call Groq API to generate type signature
```