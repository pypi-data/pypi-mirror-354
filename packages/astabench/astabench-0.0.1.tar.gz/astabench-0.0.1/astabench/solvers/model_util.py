"""
Utilities for model name normalization and usage recording.

This module provides centralized functions for normalizing model names
and recording model usage for consistent tracking and reporting.
"""

import logging
import re

import litellm
from inspect_ai.log import ModelEvent, transcript
from inspect_ai.model import GenerateConfig, ModelOutput, ModelUsage
from inspect_ai.model._model import record_and_check_model_usage

logger = logging.getLogger(__name__)

# Regex to validate model names; allows names with or without provider prefix
VALID_MODEL_NAME_REGEX = re.compile(r"^([^\s\/]+/)?[^\s\/]+$")


def normalize_model_name(model_name: str) -> str:
    """
    Normalize model name to the format <provider>/<model_name>.

    Uses litellm's get_llm_provider function to identify the provider
    for a given model name and format it as provider/model_name.

    Args:
        model_name: The model name to normalize

    Returns:
        A normalized model name in the format <provider>/<model_name>
        or the original model name if provider couldn't be determined
    """
    if not VALID_MODEL_NAME_REGEX.match(model_name):
        raise ValueError(
            f"Invalid model name cannot be normalized: '{model_name}'; must match regex '{VALID_MODEL_NAME_REGEX.pattern}'"
        )

    # If already has provider prefix, return as is
    if "/" in model_name:
        return model_name

    try:
        # get_llm_provider returns (model, provider, api_base, api_base_from_map)
        _, provider, _, _ = litellm.get_llm_provider(model_name)

        if provider:
            return f"{provider}/{model_name}"
        else:
            logger.warning(f"Unable to determine provider for model {model_name}")
            return model_name
    except Exception as e:
        logger.warning(f"Error normalizing model name '{model_name}': {e}")
        return model_name


def record_model_usage_with_inspect(
    model_name: str,
    usage: ModelUsage,
    normalize_name: bool = True,
) -> None:
    """Convenience function to record model usage with inspect_ai for tracking
    and reporting.

    See record_model_usage_event_with_inspect for more details; this just
    creates a ModelEvent with default blank values other than the name/usage
    info."""

    # missing finer details like input/output/tools so we leave those blank
    event = ModelEvent(
        model=model_name,
        input=[],
        tools=[],
        tool_choice="auto",
        config=GenerateConfig(),
        output=ModelOutput(model=model_name, usage=usage),
        cache=None,
        call=None,
        pending=False,
    )

    record_model_usage_event_with_inspect(event, normalize_name=normalize_name)


def record_model_usage_event_with_inspect(
    event: ModelEvent, normalize_name: bool = True
) -> None:
    """
    Record ModelEvent with inspect_ai for usage tracking and reporting.

    Note: This should not be used for models implemented via Inspect, since
    they already log automatically; this function is useful for cases where
    e.g. an external system exposes internal model API calls.

    This function normalizes the model name by default and records token usage
    in a format that will appear in both the ModelEvents transcript and the
    usage summary.

    Args:
        event: ModelEvent to record; `event.output.usage` should contain usage info
        normalize_name: Whether to normalize the model name (default: True)
    """

    if normalize_name:
        event = event.model_copy()
        event.model = normalize_model_name(event.model)
        event.output = event.output.model_copy()
        event.output.model = normalize_model_name(event.output.model)

    # ModelEvents show up in `inspect view`
    transcript()._event(event)

    # Model usage is tracked via record_model_usage as well; this determines
    # what gets shown in the cli printout at the end of `inspect eval`
    assert (
        event.output.usage is not None
    ), "ModelEvent output must have usage information"
    record_and_check_model_usage(event.model, event.output.usage)
