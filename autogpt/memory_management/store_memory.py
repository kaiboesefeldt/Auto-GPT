from autogpt.config import Config
from autogpt.json_utils.utilities import (
    LLM_DEFAULT_RESPONSE_FORMAT,
    is_string_valid_json,
)
from autogpt.logs import logger
from autogpt.prompts.prompt_set import get_configured_prompt_set, PromptId

CFG = Config()
PROMPTS = get_configured_prompt_set(CFG)


def format_memory(assistant_reply, next_message_content):
    # the next_message_content is a variable to stores either the user_input or the command following the assistant_reply
    COMMAND = PROMPTS.generate_prompt_string(PromptId.FORMAT_MEMORY_COMMAND)
    NO_COMMAND = PROMPTS.generate_prompt_string(PromptId.FORMAT_MEMORY_NO_COMMAND)
    HUMAN_FEEDBACK = PROMPTS.generate_prompt_string(PromptId.FORMAT_MEMORY_HUMAN_FEEDBACK)
    NO_USER_INPUT = PROMPTS.generate_prompt_string(PromptId.FORMAT_MEMORY_NO_USER_INPUT)

    result = (
        NO_COMMAND if next_message_content.startswith(COMMAND) else next_message_content
    )
    user_input = (
        NO_USER_INPUT
        if next_message_content.startswith(HUMAN_FEEDBACK)
        else next_message_content
    )

    return PROMPTS.generate_prompt_string(
        PromptId.FORMAT_MEMORY_REPLY,
        assistant_reply=assistant_reply,
        result=result,
        user_input=user_input
    )


def save_memory_trimmed_from_context_window(
    full_message_history, next_message_to_add_index, permanent_memory
):
    while next_message_to_add_index >= 0:
        message_content = full_message_history[next_message_to_add_index]["content"]
        if is_string_valid_json(message_content, LLM_DEFAULT_RESPONSE_FORMAT):
            next_message = full_message_history[next_message_to_add_index + 1]
            memory_to_add = format_memory(message_content, next_message["content"])
            logger.debug(f"Storing the following memory: {memory_to_add}")
            permanent_memory.add(memory_to_add)

        next_message_to_add_index -= 1
