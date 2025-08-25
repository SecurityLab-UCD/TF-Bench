from ollama import chat, ChatResponse

from ._types import LM, LMAnswer

OLLAMA_TTC_MODELS = [
    "qwen3:30b",
    "qwen3:32b",
    "qwen3:235b",
    "gpt-oss:20b",
    "gpt-oss:120b",
    "deepseek-r1:32b",
    "deepseek-r1:70b",
    "magistral:24b",
]


class OllamaChat(LM):
    """Generate using Ollama's chat API,"""

    def __init__(self, model_name: str, pure: bool = False):
        super().__init__(model_name=model_name, pure=pure)

    def _gen(self, prompt: str) -> LMAnswer:
        response: ChatResponse = chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": self.instruction,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            think=True,
        )
        return LMAnswer(
            answer=response.message.content,  # type: ignore
            reasoning_steps=response.message.thinking,  # type: ignore
        )
