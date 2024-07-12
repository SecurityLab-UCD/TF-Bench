source ./env.sh

# Define a list of strings
models=("llama3-8b-8192" "llama3-70b-8192" "mixtral-8x7b-32768"\
 "phi3:medium" "gemma-7b-it" "gemma2-9b-it" "whisper-large-v3")

for model in "${models[@]}"; do
  # Perform actions with $item
  echo "Processing $model"
  # Example command using $item
  python3 src/experiment.py \
  --api_key="$GROQ_API_KEY"
  --input_file="data/Benchmark-F.json" \
  --model=$model \
  --output_file="data/generated_responses_${model}.json"

  python3 src/evaluation.py \
  --benchmark_file="data/Benchmark-F.json" \
  --results_file="data/generated_responses_${model}.json" \
  --output_file="data/evaluate_${model}.json" 
done