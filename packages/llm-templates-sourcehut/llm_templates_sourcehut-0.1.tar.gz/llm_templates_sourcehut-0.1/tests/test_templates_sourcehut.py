import pytest
from llm_templates_sourcehut import sourcehut_template_loader
from llm import Template
import yaml


@pytest.mark.parametrize(
    "template_path, expected_url, yaml_content",
    [
        # 1. Short path with `~`, simple string content
        (
            "~amolith/simple",
            "https://git.sr.ht/~amolith/llm-templates/blob/main/simple.yaml",
            "A simple string prompt.",
        ),
        # 2. Short path without `~`, simple string content
        (
            "amolith/string-no-tilde",
            "https://git.sr.ht/~amolith/llm-templates/blob/main/string-no-tilde.yaml",
            "A simple string prompt, no tilde.",
        ),
        # 3. Repo path with `~`, dictionary content
        (
            "~amolith/tools/summarize",
            "https://git.sr.ht/~amolith/tools/blob/main/summarize.yaml",
            {
                "prompt": "Summarize: {{text}}",
                "system": "You are a summarizer.",
            },
        ),
        # 4. Full repo/branch path, dictionary content
        (
            "~amolith/tools/develop/translate",
            "https://git.sr.ht/~amolith/tools/blob/develop/translate.yaml",
            {"prompt": "Translate to {{lang}}: {{text}}", "model": "gpt-4"},
        ),
    ],
)
def test_sourcehut_loader_success(
    httpx_mock, template_path, expected_url, yaml_content
):
    """Tests successful loading of SourceHut templates."""
    if isinstance(yaml_content, dict):
        yaml_string = yaml.dump(yaml_content)
        expected_template = Template(name=template_path, **yaml_content)
    else:  # It's a string
        yaml_string = yaml_content
        expected_template = Template(name=template_path, prompt=yaml_content)

    httpx_mock.add_response(
        url=expected_url, method="GET", text=yaml_string, status_code=200
    )

    template = sourcehut_template_loader(template_path)

    assert template == expected_template
    assert template.name == template_path
