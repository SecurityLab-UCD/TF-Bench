# Processing command options
OPTSTRING=":venv"
# To create venv
if [ "$1" == "-venv" ]; then
  echo "===== Creating Python 3.10.0 Virtual Environment ====="
  pip install virtualenv
  python3.10 -m venv .venv
  source .venv/bin/activate
fi
# Run program
echo "===== Running Extraction and Filtering ====="
mkdir -p data/source data/filtered
# Toggle below if you need a virtual environment to run
python3 src/dataset.py -o data/source # get raw function dataset
python3 src/type_filter.py -s data/source -o data/filtered # get functions with type we want :)