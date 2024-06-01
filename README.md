# Benchmark-F

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

```sh
mkdir -p data/experiment
```

### GPT 3.5

```sh
python3 src/experiment.py -o data/experiment/gpt_generated_responses.jsonl -m gpt-3.5-turbo -a "please replace with your openai api key" # call OpenAI API to generate type signature
```

### LLAMA 3

```sh
python3 src/experiment.py -o data/experiment/llama_generated_responses.jsonl -m llama3-8b-8192 -a "please replace with your groq api key" # call Groq API to generate type signature
```

## Evaluation

```sh
mkdir -p data/evaluate
python3 src/evaluation.py -r data/experiment/gpt_generated_responses.jsonl -o data/evaluate/gpt_evaluation_result.jsonl # evaluate the results of GPT 3.5
python3 src/evaluation.py -r data/experiment/llama_generated_responses.jsonl -o data/evaluate/llama_evaluation_result.jsonl # evaluate the results of GPT 3.5
```
