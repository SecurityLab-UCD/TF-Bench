from transformers import AutoModelForCausalLM, AutoTokenizer
from src.common import get_sys_prompt
from typing import Union, List
import torch

TRANSFORMER_MODELS = ["qwen/Qwen2.5-Math-7B-Instruct", "qwen/Qwen2.5-Math-72B-Instruct"]


def get_model(
    model_name: str = "qwen/Qwen2.5-Math-7B-Instruct",
    pure: bool = False,
):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto" if device == "cuda" else None,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate_type_signature(prompt: str) -> Union[str, None]:
        try:
            text = tokenizer.apply_chat_template(
                conversation=[
                    {
                        "role": "system",
                        "content": get_sys_prompt(pure),
                    },
                    {"role": "user", "content": prompt},
                ],
                tokenize=False,
                add_generation_prompt=True,
            )

            model_inputs = tokenizer([text], return_tensors="pt").to(device)
            generated_ids = model.generate(**model_inputs, max_new_tokens=512)
            # Slice out only the newly generated tokens
            generated_ids = [
                output_ids[len(input_ids) :]
                for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            # Ensure we have an explicit type here
            decoded: List[str] = tokenizer.batch_decode(
                generated_ids, skip_special_tokens=True
            )
            if not decoded:
                return None

            response: str = decoded[0]
            return response

        except Exception as e:
            print(e)
            return None

    return generate_type_signature
