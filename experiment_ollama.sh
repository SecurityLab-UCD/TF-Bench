source ~/.zshrc
conda activate benchmarkf
source ./env.sh
# Define a list of strings
# models=("llama2:7b" "llama2:13b" "llama2:70b" "llama3" "llama3:70b" "phi3" \
# "phi3:medium" "gemma:2b" "gemma:7b" "gemma2" "gemma2:27b" "mistral" \
# "mixtral:8x22b" "mixtral:8x7b"  "deepseek-coder-v2:16b" \
# "deepseek-coder-v2:236b" "codellama:7b" \
# "codellama:13b" "codellama:34b" "codellama:70b")
models=("codegemma:2b" "codegemma:7b" "starcoder2:3b" \
"starcoder2:7b" "starcoder2:15b" "nous-hermes2:10.7b" "nous-hermes2:34b" \
"nous-hermes2-mixtral:8x7b" "codestral:22b" "stable-code:3b" \
"codeqwen:7b" "phind-codellama:34b" "granite-code:3b" "granite-code:8b" \
"granite-code:20b" "granite-code:34b" "codebooga:34b")

# Iterate over the list
for model in "${models[@]}"; do
  # Perform actions with $item
  echo "Processing $model"
  python3 src/experiment_ollama.py \
  --input_file="data/Benchmark-F-filtered.json" \
  --model=$model
done