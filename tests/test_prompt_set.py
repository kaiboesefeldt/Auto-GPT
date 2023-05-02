import os
from unittest import TestCase
from unittest.mock import Mock

from autogpt.prompts.prompt_set import PromptSet, FilePromptSet, get_configured_prompt_set
import tempfile


class TestPromptSet(TestCase):
    """
    Test cases for the BasePromptSet and FilePromptSet classes, which are responsible for
    providing snippets and templates for prompts.
    """

    def test_generate_prompt_string_with_missing_prompt(self):
        sut = PromptSet({})
        with self.assertRaises(KeyError):
            sut.generate_prompt_string("notExistingId")

    def test_generate_prompt_with_existing_string(self):
        sut = PromptSet({"id": "promptSnippet"})
        result = sut.generate_prompt_string("id")
        self.assertEquals("promptSnippet", result)

    def test_replace_parameter_in_prompt_template(self):
        sut = PromptSet({"id": "promptSnippet {insert} end"})
        result = sut.generate_prompt_string("id", insert="Lalala")
        self.assertEquals("promptSnippet Lalala end", result)

    def test_file_prompt_set_ready_snippets_in_yaml_format(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file.write(
                """prompts:
                    - simple: This is a simple text
                    - multiLine: |
                        First line
                        second line
                    - template: Before {insert} after"""
            )
            file_name = temp_file.name
            temp_file.flush()

            print(file_name)
            sut = FilePromptSet(file_name)
            self.assertEquals(
                "This is a simple text", sut.generate_prompt_string("simple")
            )
            self.assertEquals(
                "First line\nsecond line\n", sut.generate_prompt_string("multiLine")
            )
            self.assertEquals(
                "Before middle after",
                sut.generate_prompt_string("template", insert="middle"),
            )

    def test_get_configured_prompt_set(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with open(os.path.join(temp_dir, "prompt_de.yaml"), "w") as temp_file:
                temp_file.write(
                    """prompts:
                        - simple: Dies ist ein einfacher Text"""
                )
                temp_file.flush()

            cfg = Mock()
            cfg.i18n_prompts_dir = temp_dir
            cfg.prompt_language = "de"
            sut = get_configured_prompt_set(cfg)
            self.assertEquals(
                "Dies ist ein einfacher Text", sut.generate_prompt_string("simple")
            )
