"""Inference helper for Google Gemini"""

from typing import Literal
import os

from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig

from ._types import LM, LMAnswer, ReasoningEffort, EFFORT_TOKEN_MAP, NoneResponseError

GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    # ! gemini-1.5 models are deprecated
    # "gemini-1.5-flash",
    # "gemini-1.5-flash-8b",
    # "gemini-1.5-pro",
]

GEMINI_TTC_MODELS = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    # ! gemini-2.5-preview models are deprecated
    # "gemini-2.5-flash-preview-04-17",
    # "gemini-2.5-pro-preview-03-25",
]

GeminiReasoningEffort = ReasoningEffort | Literal["dynamic"]
# Upcast to a Mapping with the *wider* key type
GEMINI_MAP: dict[str, int] = {
    **EFFORT_TOKEN_MAP,
    "dynamic": -1,
}


class GeminiChat(LM):
    """Wrapper class for `google-genai` SDK for chat models
    NOTE: this class is only used for legacy Gemini models (2.0-flash) that cannot "think".

    For reasoning models with "thinking" disabled, please use `GeminiReasoning`
    with `reasoning_effort` set to "off".
    We keep this implementation since there are default thinking config for each model,
    and `thinking_config=None` has different behavior with `thinking_budget=0`.
    """

    def __init__(self, model_name: str, pure: bool = False):
        super().__init__(model_name=model_name, pure=pure)

        api_key = os.getenv("GEMINI_API_KEY")
        assert api_key, "Please set GEMINI_API_KEY in environment!"
        self.client = genai.Client(api_key=api_key)

    def _gen(self, prompt: str) -> LMAnswer:
        """generation function for legacy Gemini models (2.0)"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=[self.instruction],
            ),
        )
        content = response.text
        if content is None:
            raise NoneResponseError(self.model_name)
        return LMAnswer(answer=content)


class GeminiReasoning(LM):
    """Wrapper class for `google-genai` SDK for reasoning models"""

    def __init__(
        self,
        model_name: str,
        pure: bool = False,
        effort: GeminiReasoningEffort | None = None,
    ):
        """Initialize the GeminiReasoning model.
        effort (ReasoningEffort, optional): Defaults to None, which is `dynamic`.
        """

        super().__init__(model_name=model_name, pure=pure)

        api_key = os.getenv("GEMINI_API_KEY")
        assert api_key, "Please set GEMINI_API_KEY in environment!"
        self.client = genai.Client(api_key=api_key)

        # default to dynamic if effort is None
        self.effort = effort or "dynamic"

    def _gen(self, prompt: str) -> LMAnswer:

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=[self.instruction],
                thinking_config=ThinkingConfig(
                    thinking_budget=GEMINI_MAP[self.effort],
                    include_thoughts=True,
                ),
            ),
        )

        if not response.candidates:
            raise ValueError("No candidates returned from Gemini model.")

        candidate = response.candidates[0]
        if not candidate.content or not candidate.content.parts:
            raise NoneResponseError(self.model_name)

        answer = ""
        thinking = ""
        for part in candidate.content.parts:
            if not part.text:
                continue
            if part.thought:
                thinking += part.text
            else:
                answer += part.text

        return LMAnswer(answer=answer, reasoning_steps=thinking)
