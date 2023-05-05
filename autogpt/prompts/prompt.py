from colorama import Fore

from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.llm import ApiManager
from autogpt.logs import logger
from autogpt.prompts.generator import PromptGenerator
from autogpt.prompts.prompt_set import get_configured_prompt_set, PromptId
from autogpt.setup import prompt_user
from autogpt.utils import clean_input

CFG = Config()
PROMPTS = get_configured_prompt_set(CFG)


def build_default_prompt_generator() -> PromptGenerator:
    """
    This function generates a prompt string that includes various constraints,
        commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint(PROMPTS.generate_prompt_string(PromptId.DEFAULT_TRIGGERING_PROMPT))
    prompt_generator.add_constraint(PROMPTS.generate_prompt_string(PromptId.CONSTRAINT_SIMILAR_EVENTS))
    prompt_generator.add_constraint(PROMPTS.generate_prompt_string(PromptId.CONSTRAINT_NO_USER_ASSISTANCE))
    prompt_generator.add_constraint(PROMPTS.generate_prompt_string(PromptId.CONSTRAINT_EXCLUSIVE_COMMANDS))

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource(PROMPTS.generate_prompt_string(PromptId.RESOURCES_INTERNET))
    prompt_generator.add_resource(PROMPTS.generate_prompt_string(PromptId.RESOURCES_LONG_TERM_MEMORY))
    prompt_generator.add_resource(PROMPTS.generate_prompt_string(PromptId.RESOURCES_SIMPLE_AGENT_TASKS))
    prompt_generator.add_resource(PROMPTS.generate_prompt_string(PromptId.RESOURCES_FILE_OUTPUT))

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation(PROMPTS.generate_prompt_string(PromptId.EVALUATION_REVIEW_AND_ANALYZE))
    prompt_generator.add_performance_evaluation(PROMPTS.generate_prompt_string(PromptId.EVALUATION_SELF_CRITICIZE))
    prompt_generator.add_performance_evaluation(PROMPTS.generate_prompt_string(PromptId.EVALUATION_REFLECT_PAST_DECISIONS))
    prompt_generator.add_performance_evaluation(PROMPTS.generate_prompt_string(PromptId.EVALUATION_BE_EFFICIENT))
    prompt_generator.add_performance_evaluation(PROMPTS.generate_prompt_string(PromptId.EVALUATION_WRITE_CODE_TO_FILE))
    return prompt_generator


def construct_main_ai_config() -> AIConfig:
    """Construct the prompt for the AI to respond to

    Returns:
        str: The prompt string
    """
    config = AIConfig.load(CFG.ai_settings_file)
    if CFG.skip_reprompt and config.ai_name:
        logger.typewriter_log("Name :", Fore.GREEN, config.ai_name)
        logger.typewriter_log("Role :", Fore.GREEN, config.ai_role)
        logger.typewriter_log("Goals:", Fore.GREEN, f"{config.ai_goals}")
        logger.typewriter_log(
            "API Budget:",
            Fore.GREEN,
            "infinite" if config.api_budget <= 0 else f"${config.api_budget}",
        )
    elif config.ai_name:
        logger.typewriter_log(
            "Welcome back! ",
            Fore.GREEN,
            f"Would you like me to return to being {config.ai_name}?",
            speak_text=True,
        )
        should_continue = clean_input(
            f"""Continue with the last settings?
Name:  {config.ai_name}
Role:  {config.ai_role}
Goals: {config.ai_goals}
API Budget: {"infinite" if config.api_budget <= 0 else f"${config.api_budget}"}
Continue ({CFG.authorise_key}/{CFG.exit_key}): """
        )
        if should_continue.lower() == CFG.exit_key:
            config = AIConfig()

    if not config.ai_name:
        config = prompt_user()
        config.save(CFG.ai_settings_file)

    # set the total api budget
    api_manager = ApiManager()
    api_manager.set_total_budget(config.api_budget)

    # Agent Created, print message
    logger.typewriter_log(
        config.ai_name,
        Fore.LIGHTBLUE_EX,
        "has been created with the following details:",
        speak_text=True,
    )

    # Print the ai config details
    # Name
    logger.typewriter_log("Name:", Fore.GREEN, config.ai_name, speak_text=False)
    # Role
    logger.typewriter_log("Role:", Fore.GREEN, config.ai_role, speak_text=False)
    # Goals
    logger.typewriter_log("Goals:", Fore.GREEN, "", speak_text=False)
    for goal in config.ai_goals:
        logger.typewriter_log("-", Fore.GREEN, goal, speak_text=False)

    return config
