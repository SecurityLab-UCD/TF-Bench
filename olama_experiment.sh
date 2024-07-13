source ./env.sh

# Define a list of strings
# models=("llama3" "llama3:70b" "phi3" "phi3:medium" "gemma2" "gemma2:27b" \
# "mistral:latest" "mixtral:8x22b" "mixtral:8x7b")
models=("phi3")
# Iterate over the list
for model in "${models[@]}"; do
  # Perform actions with $item
  echo "Processing $model"
  # Example command using $item
  python3 src/experiment_ollama.py \
  --input_file="data/Benchmark-F.json" \
  --model=$model \
  --output_file="data/generated_responses_${model}.json"

  python3 src/evaluation.py \
  --benchmark_file="data/Benchmark-F.json" \
  --results_file="data/generated_responses_${model}.json" \
  --output_file="data/evaluate_${model}.json" 
done