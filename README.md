# TF-Bench

[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Evaluating Program Semantics Reasoning with Type Inference in System _F_

![evaluation workflow](./imgs/tfb.png)

If you find this work useful, please cite us as:
```bibtex
@inproceedings{he2025tfbench,
    author = {He, Yifeng and Yang, Luning and Gonzalo, Christopher and Chen, Hao},
    title = {Evaluating Program Semantics Reasoning with Type Inference in System F},
    booktitle = {Neural Information Processing Systems (NeurIPS)},
    date = {2025-11-30/2025-12-07},
    address = {San Diego, CA, USA},
}
```

## Development

### Python

We use Python 3.11.
We recommend using [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage your Python dependencies.

```sh
cd TF-Bench
uv sync # create a virtual environment, and install dependencies
```

### Haskell

To run evaluation, you need GHC (the Glasgow Haskell Compiler) installed.
We recommend using [ghcup](https://www.haskell.org/ghcup/) to install.

```sh
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
```

Due to the GHC dependency, the evaluation module currently only supports Linux and macOS.
Our evaluation requires Haskell language extensions [type operators](https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/type_operators.html)
and [impredicative polymorphism](https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/impredicative_types.html),
so we require GHC version >= 9.2.1.
Our evaluation used GHC-9.6.7.

## Building TF-Bench from scratch (optional)

### TF-Bench (base)

This script will build the benchmark (Prelude with NL) from the raw data.

```sh
uv run scripts/preprocess_benchmark.py -o tfb.json
```

### TF-Bench (pure)

```sh
git clone https://github.com/SecurityLab-UCD/alpharewrite.git
cd alpharewrite

stack build
stack exec alpharewrite-exe 1 ../tfb.json > ../tfb.pure.json

cd ..
```

For details, please check out the README of [alpharewrite](https://github.com/SecurityLab-UCD/alpharewrite).

## Download pre-built benchmark

You can also use TF-Bench on HuggingFace datasets.

```python
from datasets import load_dataset

split = "pure" # or "base"
dataset = load_dataset("SecLabUCD/TF-Bench", split=split)
```

Or through our provided package.

```python
from tfbench import load_tfb_from_hf

dataset = load_tfb_from_hf(split)
```

## Using as an application

```sh
git clone https://github.com/SecurityLab-UCD/TF-Bench.git
cd TF-Bench
uv sync
```

Please have your API key ready in `.env`.

### Proprietary models

We use each provider's official SDK to access their models.
You can check our pre-supported models in `tfbench.lm` module.

```python
from tfbench.lm import supported_models
print(supported_models)
```

To run single model, which runs both `base` and `pure` splits:

```sh
uv run main.py -m gpt-5-2025-08-07
```

### Open-weights models with Ollama

We use [Ollama](https://ollama.com/) to manage and run the OSS models reported in the Appendix.
We switched to vLLM for better performance and SDK design.
Although the Ollama option is still available,
it is no longer maintained.
We recommend using vLLM instead.

```sh
curl -fsSL https://ollama.com/install.sh | sh # install ollama, you need sudo for this
ollama serve # start your own instance instead of a system service
```

NOTE: we required the ollama version at least 0.9.0 to enable thinking parsers.
We use 0.11.7 for our experiments.

```sh
> ollama --version
ollama version is 0.11.7
```

Run the benchmark.

```sh
uv run src/main.py -m llama3:8b
```

### Running any model on HuggingFace Hub

We also support running any model that is on HuggingFace Hub out-of-the-box.
We provide an example using Qwen3.

```sh
uv run src/main.py Qwen/Qwen3-4B-Instruct-2507 # or other models
```

Note that our `main.py` uses a pre-defined model router,
which routes all un-recognized model names to HuggingFace.
We use the `</think>` token to parse thinking process,
if the model do it differently, please see the next section.

### Running your own model

To support your customized model,
you can input the path to your HuggingFace compatible checkpoint to our `main.py`.

```sh
uv run src/main.py <path to your checkpoint>
```

## Using as a package

Our package is also available on PyPi.

```sh
uv add tfbench
```

Or directly using pip, you know the way

```sh
pip install tfbench
```

### Proprietary model checkpoints that are not currently supported

Our supported model list is used to route the model name to the correct SDK.
Even a newly released model is not in our supported models list,
you can still use it by specifying the SDK client directly.
We take OpenAI GPT-4.1 as and example here.

```python
from tfbench.lm import OpenAIResponse
from tfbench import run_one_model

model = "gpt-4.1"
split = "pure"
client = OpenAIResponses(model_name=model, pure=split == "pure", effort=None)
eval_result = run_one_model(client, pure=split == "pure", effort=None)
```

### Support other customized models

You may implement an `LM` instance.

```python
from tfbench.lm._types import LM, LMAnswer

class YourLM(LM):
    def __init__(self, model_name: str, pure: bool = False):
        """initialize your model"""
        super().__init__(model_name=model_name, pure=pure)
        ...

    def _gen(self, prompt: str) -> LMAnswer:
        """your generation logic here"""
        return LMAnswer(answer=content, reasoning_steps=thinking_content)
```
