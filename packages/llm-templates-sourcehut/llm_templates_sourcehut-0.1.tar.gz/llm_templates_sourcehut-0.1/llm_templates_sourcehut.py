from llm import Template, hookimpl
import yaml
import httpx


@hookimpl
def register_template_loaders(register):
    register("srht", sourcehut_template_loader)


def sourcehut_template_loader(template_path: str) -> Template:
    """
    Load a template from SourceHut

    Format can be one of:
    - ~user/template (from ~user/llm-templates repo on main branch)
    - ~user/repo/template (from specified repo on main branch)
    - ~user/repo/branch/template (from specified repo and branch)

    The leading '~' is optional.
    """
    parts = template_path.split("/")

    username = parts[0] if parts[0].startswith("~") else f"~{parts[0]}"
    path_parts = parts[1:]

    repo = "llm-templates"
    branch = "main"

    if len(path_parts) == 1:
        template_name = path_parts[0]
    elif len(path_parts) == 2:
        repo, template_name = path_parts
    elif len(path_parts) == 3:
        repo, branch, template_name = path_parts
    else:
        raise ValueError(
            "SourceHut template path format must be ~user/template, ~user/repo/template, or ~user/repo/branch/template"
        )

    file = f"{template_name}.yaml"
    url = f"https://git.sr.ht/{username}/{repo}/blob/{branch}/{file}"

    try:
        response = httpx.get(url)
        response.raise_for_status()
        content = response.text
    except httpx.HTTPStatusError as ex:
        raise ValueError(
            f"Template '{template_name}' not found in repo '{username}/{repo}' on branch '{branch}' (HTTP {ex.response.status_code})"
        )
    except httpx.HTTPError as ex:
        raise ValueError(f"Failed to fetch template from SourceHut: {ex}")

    try:
        loaded = yaml.safe_load(content)
        if isinstance(loaded, str):
            return Template(name=template_path, prompt=loaded)
        else:
            return Template(name=template_path, **loaded)
    except yaml.YAMLError as ex:
        raise ValueError(f"Invalid YAML in SourceHut template: {ex}")
