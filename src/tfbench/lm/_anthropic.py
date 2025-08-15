from typing import Callable
from anthropic import Anthropic, InternalServerError
from ..env import ENV
from ._types import LM, LMAnswer
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


def get_ant_ttc_model(
    client: Anthropic,
    model: str = "claude-3-7-sonnet-20250219",
    pure: bool = False,
    thinking_budget: int = 1024,
) -> Callable[[str], str | None]:
    "Claude Reasoning Models"

    def generate_type_signature(prompt: str) -> str | None:
        try:
            message = client.beta.messages.create(
                model=model,
                thinking={"type": "enabled", "budget_tokens": thinking_budget},
                system=get_sys_prompt(pure),
                messages=[
                    {"role": "user", "content": prompt},
                ],
                max_tokens=thinking_budget + MAX_TOKENS,
                betas=["output-128k-2025-02-19"],
            )
        except InternalServerError as e:
            print(e)
            return None

        try:
            thinking, answer = message.content
            text = answer.text  # type: ignore
            return text if isinstance(text, str) else None
        except Exception as e:
            logging.error(f"Error processing message content: {e}")
            return None

    return generate_type_signature


class ClaudeLM(LM):
    """API client for Claude models."""

    def __init__(self, model_name: str, pure: bool = False):
        """Initialize the Claude model client."""
        super().__init__(model_name=model_name, pure=pure)

        api_key = ENV.get("ANTHROPIC_API_KEY")
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
        contents = message.content
        if not contents:
            raise ValueError("No content returned from the model.")
        text = contents[0].text  # type: ignore

        return LMAnswer(answer=text)
