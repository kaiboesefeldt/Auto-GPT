"""Git operations for autogpt"""
from git.repo import Repo

from autogpt.commands.command import command
from autogpt.config import Config
from autogpt.prompts.prompt_set import get_configured_prompt_set, PromptId
from autogpt.url_utils.validators import validate_url

CFG = Config()
PROMPTS = get_configured_prompt_set(CFG)


@command(
    "clone_repository",
    PROMPTS.generate_prompt_string(PromptId.COMMAND_CLONE_GIT_REPO_DESCRIPTION),
    PROMPTS.generate_prompt_string(PromptId.COMMAND_CLONE_GIT_REPO_SIGNATURE),
    CFG.github_username and CFG.github_api_key,
    PROMPTS.generate_prompt_string(PromptId.COMMAND_CLONE_GIT_REPO_DISABLE_REASON),
)
@validate_url
def clone_repository(url: str, clone_path: str) -> str:
    """Clone a GitHub repository locally.

    Args:
        url (str): The URL of the repository to clone.
        clone_path (str): The path to clone the repository to.

    Returns:
        str: The result of the clone operation.
    """
    split_url = url.split("//")
    auth_repo_url = f"//{CFG.github_username}:{CFG.github_api_key}@".join(split_url)
    try:
        Repo.clone_from(url=auth_repo_url, to_path=clone_path)
        return PROMPTS.generate_prompt_string(PromptId.COMMAND_CLONE_GIT_REPO_RESULT, url=url, clone_path=clone_path)
    except Exception as e:
        return PROMPTS.generate_prompt_string(PromptId.COMMAND_GENERAL_ERROR, error=str(e))
