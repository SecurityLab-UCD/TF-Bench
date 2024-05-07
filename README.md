、# Benchmark-F

Towards Sound Evaluation of Program Logic Understanding with System F

## Setup

### Download Repo(s)

```sh
cd data/ && mkdir -p repos
cd repos
wget https://hackage.haskell.org/package/base-4.20.0.0/base-4.20.0.0.tar.gz
tar xvf base-4.20.0.0.tar.gz
cd ../..
```

### Loading Env

```sh
source ./env.sh
```

### Requirements

We use Python 3.10 or above.

```sh
pip install -r requirements.txt
```

## Building Benchmark-F

```sh
mkdir -p data/source data/added data/filtered
source ./env.sh
python3 src/dataset.py -o data/source # get raw function dataset
python3 src/add_dependency.py -o data/added/base-4.20.0.0.jsonl # add type dependencies
python3 src/type_filter.py -s data/added -o data/filtered # get functions with type we want :)
```

## Experiments

### GPT 3.5

### Setup OpenAI API key

1. Create a file named ".env" in the project root directory
2. Add your OpenAI API key to the ".env" file: OPENAI_API_KEY=your-api-key

### Run the experiment
```sh
mkdir -p data/experiment/gpt
python3 src/experiment_gpt.py -o data/experiment/gpt/base-4.20.0.0.jsonl # call OpenAI API to generate type signature
```

### LLAMA 3

### Setup Groq API key

1. Add your Groq API key to the created ".env" file: GROQ_API_KEY=your-api-key

### Run the experiment
```sh
mkdir -p data/experiment/llama
python3 src/experiment_llama.py -o data/experiment/llama/base-4.20.0.0.jsonl # call Groq API to generate type signature
```
