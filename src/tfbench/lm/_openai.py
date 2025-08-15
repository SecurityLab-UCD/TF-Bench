from typing import get_args

from openai import OpenAI, NOT_GIVEN
from openai.types.shared.reasoning_effort import ReasoningEffort

from ..env import ENV
from ._types import LM, LMAnswer

OAI_MODELS = [
    "gpt-3.5-turbo-0125",
    "gpt-4-turbo-2024-04-09",
    "gpt-4o-2024-11-20",
    "gpt-4o-mini-2024-07-18",
]

OAI_TTC_MODELS = [
    "o1-mini-2024-09-12",
    "o1-preview-2024-09-12",
    "o1-2024-12-17",
    "o3-mini-2025-01-31",
    "o3-2025-04-16",
    "o4-mini-2025-04-16",
]

OAI_O5 = [
    "gpt-5-2025-08-07",
    "gpt-5-mini-2025-08-07",
    "gpt-5-nano-2025-08-07",
    "gpt-5-chat-latest",
]


class OpenAIChatCompletion(LM):
    """
    Generate using OpenAI SDK's Chat Completions API.
    This is the previous standard (supported indefinitely).
    This client should be only used for legacy non-reasoning models,
    i.e., (gpt-3.5-turbo, gpt-4-turbo, gpt-4o).
    """

    def __init__(self, model_name: str, pure: bool = False):
        super().__init__(model_name=model_name, pure=pure)

        api_key = ENV.get("OPENAI_API_KEY")
        assert api_key, "Please set OPENAI_API_KEY in environment!"
        self.client = OpenAI(api_key=api_key)

    def _gen(self, prompt: str) -> LMAnswer:
        """Generate using OpenAI SDK's Chat Completions API."""
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

        return LMAnswer(
            answer=completion.choices[0].message.content,
        )


class OpenAIResponses(LM):
    """Client for New OpenAI Responses API.
    This should be used for newer *reasoning* models,
    especially GPT-5.
    """

    def __init__(
        self,
        model_name: str,
        pure: bool = False,
        effort: ReasoningEffort = None,
    ):
        """OpenAI Responses SDK Client
        If `effort` is None (not provided), we disable reasoning mode.
        """
        super().__init__(model_name=model_name, pure=pure)

        api_key = ENV.get("OPENAI_API_KEY")
        assert api_key, "Please set OPENAI_API_KEY in environment!"
        self.client = OpenAI(api_key=api_key)

        self.effort: ReasoningEffort = effort

    def _gen(self, prompt: str) -> LMAnswer:
        """Generate using OpenAI SDK's Responses API."""

        response = self.client.responses.create(
            model=self.model_name,
            instructions=self.instruction,
            input=prompt,
            reasoning=(
                {
                    "effort": self.effort,
                }
                if self.effort
                else NOT_GIVEN
            ),
        )
        return LMAnswer(answer=response.output_text)
