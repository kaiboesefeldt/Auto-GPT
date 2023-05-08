"""Commands for converting audio to text."""
import json

import requests

from autogpt.commands.command import command
from autogpt.config import Config
from autogpt.prompts.prompt_set import get_configured_prompt_set, PromptId

CFG = Config()
PROMPTS = get_configured_prompt_set(CFG)


@command(
    "read_audio_from_file",
    PROMPTS.generate_prompt_string(PromptId.COMMAND_AUDIO_TEXT_DESCRIPTION),
    PROMPTS.generate_prompt_string(PromptId.COMMAND_AUDIO_TEXT_SIGNATURE),
    CFG.huggingface_audio_to_text_model,
    PROMPTS.generate_prompt_string(PromptId.COMMAND_AUDIO_TEXT_DISABLE_REASON),
)
def read_audio_from_file(filename: str) -> str:
    """
    Convert audio to text.

    Args:
        filename (str): The path to the audio file

    Returns:
        str: The text from the audio
    """
    with open(filename, "rb") as audio_file:
        audio = audio_file.read()
    return read_audio(audio)


def read_audio(audio: bytes) -> str:
    """
    Convert audio to text.

    Args:
        audio (bytes): The audio to convert

    Returns:
        str: The text from the audio
    """
    model = CFG.huggingface_audio_to_text_model
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    api_token = CFG.huggingface_api_token
    headers = {"Authorization": f"Bearer {api_token}"}

    if api_token is None:
        raise ValueError(
            "You need to set your Hugging Face API token in the config file."
        )

    response = requests.post(
        api_url,
        headers=headers,
        data=audio,
    )

    text = json.loads(response.content.decode("utf-8"))["text"]
    return PROMPTS.generate_prompt_string(PromptId.COMMAND_AUDIO_TEXT_RESULT, text=text)
