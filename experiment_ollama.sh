source ./env.sh

# Define a list of strings
# models=("llama3" "llama3:70b" "phi3" "phi3:medium" "gemma2" "gemma2:27b" \
# "mistral" "mixtral:8x22b" "mixtral:8x7b")
models=("llama3")
# Iterate over the list
for model in "${models[@]}"; do
  # Perform actions with $item
  echo "Processing $model"
  python3 src/experiment_ollama.py \
  --input_file="data/Benchmark-F.json" \
  --model=$model
done