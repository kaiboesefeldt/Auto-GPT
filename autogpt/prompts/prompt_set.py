from typing import Dict, Callable

import os
import yaml

from enum import Enum

from autogpt.config import Config


class PromptId(Enum):
    DEFAULT_TRIGGERING_PROMPT = 1
    CONSTRAINT_WORD_LIMIT = 2
    CONSTRAINT_SIMILAR_EVENTS = 3
    CONSTRAINT_NO_USER_ASSISTANCE = 4
    CONSTRAINT_EXCLUSIVE_COMMANDS = 5
    RESOURCES_INTERNET = 6
    RESOURCES_LONG_TERM_MEMORY = 7
    RESOURCES_SIMPLE_AGENT_TASKS = 8
    RESOURCES_FILE_OUTPUT = 9
    EVALUATION_REVIEW_AND_ANALYZE = 10
    EVALUATION_SELF_CRITICIZE = 11
    EVALUATION_REFLECT_PAST_DECISIONS = 12
    EVALUATION_BE_EFFICIENT = 13
    EVALUATION_WRITE_CODE_TO_FILE = 14
    HISTORY_COMMAND_THREW_ERROR = 15
    HISTORY_HUMAN_FEEDBACK = 16
    HISTORY_COMMAND_RESULT = 17
    HISTORY_FAILURE_TOO_MUCH_OUTPUT = 18
    HISTORY_UNABLE_TO_CREATE_COMMAND = 19
    FEEDBACK_PROMPT = 20

class PromptSet:
    """
    A set of prompt snippets and templates. These can be accessed by id, and template
    parameters may be passed.
    """

    def __init__(self, prompts_factory: Callable[[], Dict[str, str]]):
        """
        Initialize the PromptSet.

        Args:
            prompts_factory (Dict[str, str]): The prompt snippets and templates. Key is the id, value
            is the snippet or template.
        """
        self._prompts_factory = prompts_factory
        self._prompts = None

    @property
    def prompts(self) -> Dict[str, str]:
        if not self._prompts:
            self._prompts = self._prompts_factory()
        return self._prompts

    def generate_prompt_string(self, snippet_id: PromptId, **kwargs: str) -> str:
        """
        Get a prompt snippet, eventually with replaced template parameters.

        Args:
            snippet_id (PromptId): The id of the prompt snippet or template to return
            kwargs (str): The template arguments. Must fit exactly the arguments required by
            the template.

        Returns:
            str: The requested prompt snippet or template, with all template arguments inserted.
        """
        prompt = self.prompts[snippet_id.name]
        return prompt.format(**kwargs)


class FilePromptSet(PromptSet):
    """
    A prompt set which ready the prompt template and snippet definition from a yaml file.
    This file has a top level item named "prompts" and for each template or snippet
    one key/value pair.
    """

    def __init__(self, filename: str):
        """
        Initializes the file based prompt set.

        Args:
            filename (str): The file name which contains the prompt set definition.
        """
        self._filename = filename
        super().__init__(self._load_prompts)

    def _load_prompts(self) -> Dict[str, str]:
        with open(self._filename, "r") as f:
            data = yaml.safe_load(f)
            input_data = data["prompts"]
            prompts = {}
            for d in input_data:
                prompts.update(d)
            return prompts


def get_configured_prompt_set(cfg: Config) -> PromptSet:
    """
    Get the configured prompt set.
    Args:
         cfg (Config): The configuration where the prompt set is configured

     Returns:
         The prompt set at the configured location
    """
    prompt_set_path = os.path.join(
        cfg.i18n_prompts_dir, "prompts_" + cfg.prompt_language + ".yaml"
    )
    return FilePromptSet(prompt_set_path)
