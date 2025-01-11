from transformers import AutoModelForCausalLM, AutoTokenizer
from src.common import get_sys_prompt
from typing import Union, List
import torch
import re

TRANSFORMER_MODELS = ["qwen/Qwen2.5-Math-7B-Instruct", "qwen/Qwen2.5-Math-72B-Instruct"]


def qwen_postprocess(text: str):
    # pattern = r"\\boxed\{(.*?)\}"
    pattern = r"boxed\{(.*?)\}"
    match = re.search(pattern, text)
    extracted_text = match.group(1) if match else text
    extracted_text = extracted_text.replace(r"\to", "->")
    extracted_text = extracted_text.replace(r"\rightarrow", "->")
    extracted_text = extracted_text.replace(r"\times", "->")
    extracted_text = extracted_text.replace(r"\Rightarrow", "=>")
    extracted_text = extracted_text.replace(r"\text{", "")

    return extracted_text


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
            generated_ids = model.generate(**model_inputs, max_new_tokens=1024)
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

            # Ensure the output from qwen_postprocess is explicitly str or None
            processed_response = qwen_postprocess(response)
            if not isinstance(processed_response, str):
                return None

            return processed_response

        except Exception as e:
            print(e)
            return None

    return generate_type_signature
