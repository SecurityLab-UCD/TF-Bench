import logging

from returns.result import ResultE, Success, Failure, Result

from ._types import LM, ReasoningEffort, LMAnswer
from ._openai import (
    OpenAIChatCompletion,
    OpenAIResponses,
    OAI_MODELS,
    OAI_TTC_MODELS,
    OAI_O5,
)


def router(
    model_name: str, pure: bool, effort: ReasoningEffort | None = None
) -> LM | None:
    """Route the model name to the appropriate LM class."""
    if model_name in OAI_MODELS:
        return OpenAIChatCompletion(model_name=model_name, pure=pure)
    if model_name in OAI_TTC_MODELS:
        return OpenAIResponses(model_name=model_name, pure=pure)
    if model_name in OAI_O5:
        return OpenAIResponses(model_name=model_name, pure=pure, effort=effort)
    return None


def is_supported(model_name: str) -> bool:
    """check if the model is supported"""
    all_models = OAI_MODELS + OAI_TTC_MODELS + OAI_O5
    return model_name in all_models


def extract_response(response: ResultE[LMAnswer]) -> str:
    """Extract the answer from the LMAnswer or return an empty string if None."""
    match response:
        case Success(r):
            return r.answer or ""
        case Failure(e):
            logging.error(f"Error generating response: {e}")
            return ""
    return ""
