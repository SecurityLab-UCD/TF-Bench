source ./env.sh

# Define the arrays
poly_types=("Ad-hoc" "Parametric" "Monomorphic" "Polymorphic")
models=("api")
pure_values=("true" "false")

# Loop through each combination
for poly_type in "${poly_types[@]}"; do
    for model in "${models[@]}"; do
        for pure in "${pure_values[@]}"; do
            if [ "$pure" = "true" ]; then
                python scripts/run_experiments.py \
                    --poly_type="$poly_type" \
                    --option="$model" \
                    --pure="$pure" \
                    --input_file="Benchmark-F.pure.json"
            else
                python scripts/run_experiments.py \
                    --poly_type="$poly_type" \
                    --option="$model" \
                    --pure="$pure" \
                    --input_file="Benchmark-F.json"
            fi
        done
    done
done
