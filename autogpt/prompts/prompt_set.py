from typing import Dict
import yaml

class PromptSet:
    def __init__(self, prompts: Dict[str, str]):
        self.prompts = prompts

    def generate_prompt_string(self, id: str, **kwargs: str) -> str:
        prompt = self.prompts[id]
        return prompt.format(**kwargs)

class FilePromptSet(PromptSet):
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            data = yaml.safe_load(f)
            input_data = data["prompts"]
            prompts = {}
            for d in input_data:
                prompts.update(d)
        print(prompts)
        super().__init__(prompts)