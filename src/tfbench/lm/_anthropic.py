import os
from anthropic import Anthropic
from ._types import LM, LMAnswer, ReasoningEffort, EFFORT_TOKEN_MAP, NoneResponseError
from .settings import MAX_TOKENS

CLAUDE_MODELS = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
]

CLAUDE_TTC_MODELS = [
    "claude-3-7-sonnet-20250219",
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-sonnet-4-20250514",
]


class ClaudeChat(LM):
    """API client for Claude models.

    SDK wrapper for legacy Claude models with no reasoning.
    """

    def __init__(self, model_name: str, pure: bool = False):
        """Initialize the Claude model client."""
        super().__init__(model_name=model_name, pure=pure)

        api_key = os.getenv("ANTHROPIC_API_KEY")
        assert api_key, "Please set ANTHROPIC_API_KEY in environment!"
        self.client = Anthropic(api_key=api_key)

    def _gen(self, prompt: str) -> LMAnswer:
        """Generate using Anthropic's Chat Completions API."""
        message = self.client.messages.create(
            system=self.instruction,
            messages=[
                {"role": "user", "content": prompt},
            ],
            model=self.model_name,
            max_tokens=MAX_TOKENS,
        )

        text = None
        for c in message.content:
            if c.type == "text":
                text = c.text
                break

        if text is None:
            raise NoneResponseError(self.model_name)

        return LMAnswer(answer=text)


class ClaudeReasoning(LM):
    """API client for Claude models."""

    def __init__(
        self, model_name: str, pure: bool = False, effort: ReasoningEffort | None = None
    ):
        """Initialize the Claude model client."""
        super().__init__(model_name=model_name, pure=pure)

        api_key = os.getenv("ANTHROPIC_API_KEY")
        assert api_key, "Please set ANTHROPIC_API_KEY in environment!"
        self.client = Anthropic(api_key=api_key)

        self.effort: ReasoningEffort = effort or "medium"

    def _gen(self, prompt: str) -> LMAnswer:
        """Generate using Anthropic's Chat Completions API."""
        rsn_tokens = EFFORT_TOKEN_MAP[self.effort]
        message = self.client.messages.create(
            system=self.instruction,
            messages=[
                {"role": "user", "content": prompt},
            ],
            thinking={
                "type": "enabled",
                "budget_tokens": rsn_tokens,
            },
            model=self.model_name,
            max_tokens=MAX_TOKENS + rsn_tokens,
        )
        text = None
        thinking = None
        for block in message.content:
            if block.type == "text":
                text = block.text
            if block.type == "thinking":
                thinking = block.thinking
            if text and thinking:
                break

        if text is None:
            raise NoneResponseError(self.model_name)

        return LMAnswer(answer=text, reasoning_steps=thinking)
