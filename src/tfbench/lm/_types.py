from abc import ABC, abstractmethod
from enum import StrEnum
from dataclasses import dataclass
from typing import Literal

from returns.result import safe
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from .prompts import get_sys_prompt


@dataclass
class LMAnswer:
    answer: str | None
    reasoning_steps: str | None = None


class LM(ABC):
    def __init__(self, model_name: str, pure: bool = False):
        self.model_name = model_name
        self.pure = pure
        self.instruction = get_sys_prompt(self.pure)

    @safe
    @retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def generate(self, prompt: str) -> LMAnswer:
        """Generate a response for the given prompt.
        We use factory mode to for @safe and @retry,
        see https://www.oodesign.com/factory-method-pattern
        """
        return self._gen(prompt)

    @abstractmethod
    def _gen(self, prompt) -> LMAnswer:
        """The actual generation method for different clients"""
