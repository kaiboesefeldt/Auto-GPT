from typing import Dict, Callable

import os
import yaml

from enum import Enum, auto

from autogpt.config import Config


class PromptId(Enum):
    DEFAULT_TRIGGERING_PROMPT = auto()
    PROMPT_START = auto()
    PROMPT_START_OS_INFO = auto()
    PROMPT_BUDGET = auto()
    FULL_PROMPT = auto()
    CONSTRAINT_WORD_LIMIT = auto()
    CONSTRAINT_SIMILAR_EVENTS = auto()
    CONSTRAINT_NO_USER_ASSISTANCE = auto()
    CONSTRAINT_EXCLUSIVE_COMMANDS = auto()
    RESOURCES_INTERNET = auto()
    RESOURCES_LONG_TERM_MEMORY = auto()
    RESOURCES_SIMPLE_AGENT_TASKS = auto()
    RESOURCES_FILE_OUTPUT = auto()
    EVALUATION_REVIEW_AND_ANALYZE = auto()
    EVALUATION_SELF_CRITICIZE = auto()
    EVALUATION_REFLECT_PAST_DECISIONS = auto()
    EVALUATION_BE_EFFICIENT = auto()
    EVALUATION_WRITE_CODE_TO_FILE = auto()
    HISTORY_COMMAND_THREW_ERROR = auto()
    HISTORY_HUMAN_FEEDBACK = auto()
    HISTORY_COMMAND_RESULT = auto()
    HISTORY_FAILURE_TOO_MUCH_OUTPUT = auto()
    HISTORY_UNABLE_TO_CREATE_COMMAND = auto()
    FEEDBACK_PROMPT = auto()
    DEFAULT_DESIRE = auto()
    DEFAULT_AI_ROLE = auto()
    DEFAULT_AI_GOALS = auto()
    SYSTEM_PROMPT = auto()
    USER_PROMPT = auto()
    CALL_AI_FUNTION = auto()
    DATE_AND_TIME = auto()
    BUDGET_INFO = auto()
    BUDGET_EXCEEDED = auto()
    BUDGET_NEARLY_EXCEEDED = auto()
    BUDGET_LOW = auto()
    MEMORY_ADD = auto()
    COMMAND_DISABLED = auto()
    COMMAND_RECORD = auto()
    COMMAND_GENERAL_ERROR = auto()
    COMMAND_ANALYZE_CODE_DESCRIPTION = auto()
    COMMAND_ANALYZE_CODE_LONG_DESCRIPTION = auto()
    COMMAND_ANALYZE_CODE_SIGNATURE = auto()
    COMMAND_AUDIO_TEXT_DESCRIPTION = auto()
    COMMAND_AUDIO_TEXT_SIGNATURE = auto()
    COMMAND_AUDIO_TEXT_DISABLE_REASON = auto()
    COMMAND_AUDIO_TEXT_RESULT = auto()
    COMMAND_EXECUTE_PYTHON_FILE_DESCRIPTION = auto()
    COMMAND_EXECUTE_PYTHON_FILE_SIGNATURE = auto()
    COMMAND_EXECUTE_PYTHON_FILE_ERROR_INVALID_TYPE = auto()
    COMMAND_EXECUTE_PYTHON_FILE_ERROR_FILE_NOT_EXIST = auto()
    COMMAND_EXECUTE_SHELL_DESCRIPTION = auto()
    COMMAND_EXECUTE_SHELL_SIGNATURE = auto()
    COMMAND_EXECUTE_SHELL_DISABLE_REASON = auto()
    COMMAND_EXECUTE_SHELL_POPEN_DESCRIPTION = auto()
    COMMAND_EXECUTE_SHELL_POPEN_SIGNATURE = auto()
    COMMAND_EXECUTE_SHELL_POPEN_DISABLE_REASON = auto()
    COMMAND_EXECUTE_SHELL_POPEN_RESULT = auto()
    COMMAND_READ_FILE_DESCRIPTION = auto()
    COMMAND_READ_FILE_SIGNATURE = auto()
    COMMAND_WRITE_TO_FILE_DESCRIPTION = auto()
    COMMAND_WRITE_TO_FILE_SIGNATURE = auto()
    COMMAND_WRITE_TO_FILE_ERROR_DUPLICATE_OPERATION = auto()
    COMMAND_WRITE_TO_FILE_SUCCESS = auto()
    COMMAND_APPEND_TO_FILE_DESCRIPTION = auto()
    COMMAND_APPEND_TO_FILE_SIGNATURE = auto()
    COMMAND_APPEND_TO_FILE_SUCCESS = auto()
    COMMAND_DELETE_FILE_DESCRIPTION = auto()
    COMMAND_DELETE_FILE_SIGNATURE = auto()
    COMMAND_DELETE_FILE_ERROR_DUPLICATE_OPERATION = auto()
    COMMAND_DELETE_FILE_SUCCESS = auto()
    COMMAND_LIST_FILES_DESCRIPTION = auto()
    COMMAND_LIST_FILES_SIGNATURE = auto()
    COMMAND_DOWNLOAD_FILE_DESCRIPTION = auto()
    COMMAND_DOWNLOAD_FILE_SIGNATURE = auto()
    COMMAND_DOWNLOAD_FILE_DISABLE_REASON = auto()
    COMMAND_DOWNLOAD_FILE_ERROR_HTTP = auto()
    COMMAND_DOWNLOAD_FILE_SUCCESS = auto()
    COMMAND_CLONE_GIT_REPO_DESCRIPTION = auto()
    COMMAND_CLONE_GIT_REPO_SIGNATURE = auto()
    COMMAND_CLONE_GIT_REPO_DISABLE_REASON = auto()
    COMMAND_CLONE_GIT_REPO_RESULT = auto()
    COMMAND_GOOGLE_SEARCH_DESCRIPTION = auto()
    COMMAND_GOOGLE_SEARCH_SIGNATURE = auto()
    COMMAND_GOOGLE_SEARCH_DISABLE_REASON = auto()
    COMMAND_GOOGLE_SEARCH_ERROR_INVALID_API_KEY = auto()
    COMMAND_GENERATE_IMAGE_DESCRIPTION = auto()
    COMMAND_GENERATE_IMAGE_SIGNATURE = auto()
    COMMAND_GENERATE_IMAGE_ERROR_NO_PROVIDER = auto()
    COMMAND_GENERATE_IMAGE_SAVED_TO_DISK = auto()
    COMMAND_IMPROVE_CODE_DESCRIPTION = auto()
    COMMAND_IMPROVE_CODE_SIGNATURE = auto()
    COMMAND_IMPROVE_CODE_LONG_DESCRIPTION = auto()
    COMMAND_TASK_COMPLETE_DESCRIPTION = auto()
    COMMAND_TASK_COMPLETE_SIGNATURE = auto()
    COMMAND_SEND_TWEET_DESCRIPTION = auto()
    COMMAND_SEND_TWEET_SIGNATURE = auto()
    COMMAND_SEND_TWEET_SUCCESS = auto()
    COMMAND_SEND_TWEET_ERROR = auto()
    COMMAND_BROWSE_WEBISTE_DESCRIPTION = auto()
    COMMAND_BROWSE_WEBISTE_SIGNATURE = auto()
    COMMAND_BROWSE_WEBISTE_NO_RESPONSE = auto()
    COMMAND_BROWSE_WEBSITE_ANSWER = auto()
    COMMAND_WRITE_TESTS_DESCRIPTION = auto()
    COMMAND_WRITE_TESTS_SIGNATURE = auto()
    COMMAND_WRITE_TESTS_LONG_DESCRIPTION = auto()
    GET_DATE_TIME_RESULT = auto()
    CREATE_MESSAGE_FOR_QUESTION = auto()
    DATA_INGESTION_ADD_CHUNK = auto()


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
