from vllm import LLM, SamplingParams

from ..env import ENV
from ._types import LM, LMAnswer, ReasoningEffort, EFFORT_TOKEN_MAP


_CHAT_TEMPLATE = """# Instructions
{instruction}

## Task
{task}
"""


class VLLMGen(LM):

    def __init__(self, model_name: str, pure: bool = False):
        super().__init__(model_name=model_name, pure=pure)
        self.llm = LLM(model=self.model_name)

    def _gen(self, prompt: str) -> LMAnswer:
        _prompt = _CHAT_TEMPLATE.format(instruction=self.instruction, task=prompt)
        result = self.llm.generate(_prompt)
        output = result[0].outputs[0]  # any exception would be caught by @safe
        return LMAnswer(answer=output.text)
