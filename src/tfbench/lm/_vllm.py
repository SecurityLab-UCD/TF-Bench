from vllm import LLM, SamplingParams
from vllm.entrypoints.chat_utils import ChatCompletionMessageParam

from ..env import ENV
from ._types import LM, LMAnswer, ReasoningEffort, EFFORT_TOKEN_MAP


_CHAT_TEMPLATE = """# Instructions
{instruction}

## Task
{task}
"""


class VLLMChat(LM):

    def __init__(self, model_name: str, pure: bool = False):
        super().__init__(model_name=model_name, pure=pure)
        self.llm = LLM(model=self.model_name)

    def _gen(self, prompt: str) -> LMAnswer:
        """generate using vLLM's chat interface"""
        conversation: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.instruction},
            {"role": "user", "content": prompt},
        ]
        outputs = self.llm.chat(conversation)
        output = outputs[0].outputs[0]  # any exception would be caught by @safe
        return LMAnswer(answer=output.text)
