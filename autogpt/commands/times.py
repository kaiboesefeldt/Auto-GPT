from datetime import datetime

from autogpt.config import Config
from autogpt.prompts.prompt_set import get_configured_prompt_set, PromptId

CFG = Config()
PROMPTS = get_configured_prompt_set(CFG)


def get_datetime() -> str:
    """Return the current date and time

    Returns:
        str: The current date and time
    """
    return PROMPTS.generate_prompt_string(PromptId.GET_DATE_TIME_RESULT, date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
