# Benchmark-F

Towards Sound Evaluation of Program Logic Understanding with System F

## Setup

### Download Repo(s)

```sh
cd data/ && mkdir -p repos
wget https://hackage.haskell.org/package/base-4.20.0.0/base-4.20.0.0.tar.gz
tar xvf base-4.20.0.0.tar.gz
cd ..
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