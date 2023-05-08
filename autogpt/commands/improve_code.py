from __future__ import annotations

import json

from autogpt.commands.command import command
from autogpt.config import Config
from autogpt.llm import call_ai_function
from autogpt.prompts.prompt_set import get_configured_prompt_set, PromptId

CFG = Config()
PROMPTS = get_configured_prompt_set(CFG)


@command(
    "improve_code",
    PROMPTS.generate_prompt_string(PromptId.COMMAND_IMPROVE_CODE_DESCRIPTION),
    PROMPTS.generate_prompt_string(PromptId.COMMAND_IMPROVE_CODE_SIGNATURE),
)
def improve_code(suggestions: list[str], code: str) -> str:
    """
    A function that takes in code and suggestions and returns a response from create
      chat completion api call.

    Parameters:
        suggestions (list): A list of suggestions around what needs to be improved.
        code (str): Code to be improved.
    Returns:
        A result string from create chat completion. Improved code in response.
    """

    function_string = (
        "def generate_improved_code(suggestions: list[str], code: str) -> str:"
    )
    args = [json.dumps(suggestions), code]
    description_string = PROMPTS.generate_prompt_string(PromptId.COMMAND_IMPROVE_CODE_LONG_DESCRIPTION)

    return call_ai_function(function_string, args, description_string)
