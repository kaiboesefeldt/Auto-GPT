"""A module that contains a command to send a tweet."""
import os

import tweepy

from autogpt.commands.command import command
from autogpt.config import Config
from autogpt.prompts.prompt_set import get_configured_prompt_set, PromptId

CFG = Config()
PROMPTS = get_configured_prompt_set(CFG)


@command(
    "send_tweet",
    PROMPTS.generate_prompt_string(PromptId.COMMAND_SEND_TWEET_DESCRIPTION),
    PROMPTS.generate_prompt_string(PromptId.COMMAND_SEND_TWEET_SIGNATURE),
)
def send_tweet(tweet_text: str) -> str:
    """
      A function that takes in a string and returns a response from create chat
        completion api call.

    Args:
      tweet_text (str): Text to be tweeted.

      Returns:
          A result from sending the tweet.
    """
    consumer_key = os.environ.get("TW_CONSUMER_KEY")
    consumer_secret = os.environ.get("TW_CONSUMER_SECRET")
    access_token = os.environ.get("TW_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TW_ACCESS_TOKEN_SECRET")
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Send tweet
    try:
        api.update_status(tweet_text)
        return PROMPTS.generate_prompt_string(PromptId.COMMAND_SEND_TWEET_SUCCESS)
    except tweepy.TweepyException as e:
        return PROMPTS.generate_prompt_string(PromptId.COMMAND_SEND_TWEET_ERROR, reason=str(e.reason))
