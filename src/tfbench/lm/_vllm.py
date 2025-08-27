from vllm import LLM
from vllm.entrypoints.chat_utils import ChatCompletionMessageParam

from openai import OpenAI

from ..env import ENV
from ._types import LM, LMAnswer, NoneResponseError


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


class VLLMOpenAIChatCompletion(LM):
    """Serving mode of vLLM that is compatible with OpenAI-Compatible Server
    https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html
    """

    def __init__(self, model_name: str, pure: bool = False):
        super().__init__(model_name=model_name, pure=pure)

        api_key = ENV.get("VLLM_API_KEY", "")
        host = ENV.get("VLLM_HOST", "localhost")
        port = ENV.get("VLLM_PORT", "8000")

        url = f"http://{host}:{port}/v1"
        self.client = OpenAI(
            base_url=url,
            api_key=api_key,
        )

    def _gen(self, prompt: str) -> LMAnswer:
        """generate using vLLM's OpenAI compatible interface"""
        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "developer",
                    "content": self.instruction,
                },
                {"role": "user", "content": prompt},
            ],
            model=self.model_name,
        )

        message = completion.choices[0].message
        content = message.content
        if content is None:
            raise NoneResponseError(self.model_name)

        return LMAnswer(
            answer=content,
            reasoning_steps=(
                message.reasoning_content  # type: ignore
                if hasattr(message, "reasoning_content")
                else None
            ),
        )
