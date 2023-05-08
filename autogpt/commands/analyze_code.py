"""Code evaluation module."""
from __future__ import annotations

from autogpt.commands.command import command
from autogpt.config import Config
from autogpt.llm import call_ai_function
from autogpt.prompts.prompt_set import get_configured_prompt_set, PromptId

CFG = Config()
PROMPTS = get_configured_prompt_set(CFG)


@command(
    "analyze_code",
    PROMPTS.generate_prompt_string(PromptId.COMMAND_ANALYZE_CODE_DESCRIPTION),
    PROMPTS.generate_prompt_string(PromptId.COMMAND_ANALYZE_CODE_SIGNATURE),
)
def analyze_code(code: str) -> list[str]:
    """
    A function that takes in a string and returns a response from create chat
      completion api call.

    Parameters:
        code (str): Code to be evaluated.
    Returns:
        A result string from create chat completion. A list of suggestions to
            improve the code.
    """

    function_string = "def analyze_code(code: str) -> list[str]:"
    args = [code]
    description_string = PROMPTS.generate_prompt_string(PromptId.COMMAND_ANALYZE_CODE_LONG_DESCRIPTION)

    return call_ai_function(function_string, args, description_string)
