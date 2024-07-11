source ./env.sh

# Define a list of strings
models=("llama3" "llama3:70b" "phi3" "phi3:medium" "gemma2" "gemma2:27b" )

# Iterate over the list
for model in "${models[@]}"; do
  # Perform actions with $item
  echo "Processing $model"
  # Example command using $item
  python3 src/experiment_ollama.py \
  --input_file="data/Benchmark-F.jsonl" \
  --model=$model \
  --output_file="data/generated_responses_${model}.jsonl"

  python3 src/evaluation.py \
  --benchmark_file="data/Benchmark-F.jsonl" \
  --results_file="data/generated_responses_${model}.jsonl" \
  --output_file="data/evaluate_${model}.jsonl" 
done