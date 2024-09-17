#!/bin/bash
# Processing command options
OPTSTRING=":venv"
# To create venv
if [ "$1" == "-venv" ]; then
  echo "===== Creating Python 3.10.0 Virtual Environment ====="
  pip install virtualenv
  python3.10 -m venv .venv
  source .venv/bin/activate
fi

source ./env.sh
rm data/source/*

# Run program
echo "===== Running Extraction and Filtering ====="
mkdir -p data/source
# Toggle below if you need a virtual environment to run
python3 src/dataset.py -o data/source # get raw function dataset
python3 src/prelude.py -o Benchmark-F.temp.json
python3 src/hoogle.py -i Benchmark-F.temp.json -o Benchmark-F.json
python3 src/type_rewrite.py -d Benchmark-F.json -o Benchmark-F.removed.json