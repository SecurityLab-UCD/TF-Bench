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
# Create the data directory and load package
echo "===== Downloading Haskell Base Package ====="
rm -rf data/repos data/source data/filtered
mkdir -p data/repos
wget -P data/repos https://hackage.haskell.org/package/base-4.20.0.0/base-4.20.0.0.tar.gz
tar xvf data/repos/base-4.20.0.0.tar.gz -C data/repos
# Download packages if not loaded
echo "===== Downloading Python Packages ====="
pip install -r requirements.txt
source env.sh