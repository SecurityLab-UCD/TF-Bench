from transformers import AutoModelForCausalLM, AutoTokenizer

from ._types import LM, LMAnswer


def extract_thinking_content(output: str) -> tuple[str, str | None]:
    """Extract the thinking content and the final answer from the model output.
    based on <think> and </think> tags.

    Args:
        output (str): The model output.
    Returns:
        tuple[str, str | None]: The thinking content and the final answer.
    """
    if "<think>" in output and "</think>" in output:
        thinking_content = output.split("<think>")[1].split("</think>")[0].strip()
        content = output.split("</think>")[-1].strip()
        return content, thinking_content

    return output, None


class HFChat(LM):

    def __init__(self, model_name: str, pure: bool = False):
        super().__init__(model_name=model_name, pure=pure)

        # load the tokenizer and the model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype="auto", device_map="auto"
        )

    def _gen(self, prompt: str) -> LMAnswer:
        messages = [
            {"role": "system", "content": self.instruction},
            {"role": "user", "content": prompt},
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        # conduct text completion
        generated_ids = self.model.generate(**model_inputs, max_new_tokens=32768)
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]) :].tolist()
        output = self.tokenizer.decode(output_ids, skip_special_tokens=True).strip("\n")

        content, thinking_content = extract_thinking_content(output)
        return LMAnswer(answer=content, reasoning_steps=thinking_content)
