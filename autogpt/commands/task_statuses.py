"""Task Statuses module."""
from __future__ import annotations

from typing import NoReturn

from autogpt.commands.command import command
from autogpt.config import Config
from autogpt.logs import logger
from autogpt.prompts.prompt_set import get_configured_prompt_set, PromptId

CFG = Config()
PROMPTS = get_configured_prompt_set(CFG)

@command(
    "task_complete",
    PROMPTS.generate_prompt_string(PromptId.COMMAND_TASK_COMPLETE_DESCRIPTION),
    PROMPTS.generate_prompt_string(PromptId.COMMAND_TASK_COMPLETE_SIGNATURE),
)
def task_complete(reason: str) -> NoReturn:
    """
    A function that takes in a string and exits the program

    Parameters:
        reason (str): The reason for shutting down.
    Returns:
        A result string from create chat completion. A list of suggestions to
            improve the code.
    """
    logger.info(title="Shutting down...\n", message=reason)
    quit()
