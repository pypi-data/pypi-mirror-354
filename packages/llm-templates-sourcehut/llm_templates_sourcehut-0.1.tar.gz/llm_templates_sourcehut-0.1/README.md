# llm-templates-sourcehut

[![PyPI](https://img.shields.io/pypi/v/llm-templates-sourcehut.svg)](https://pypi.org/project/llm-templates-sourcehut/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://git.sr.ht/~amolith/llm-templates-sourcehut/tree/main/item/LICENSE)

Load LLM templates from sourcehut repositories

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```bash
llm install llm-templates-sourcehut
```

## Usage

To use the template from `templatename.yaml` in the `https://git.sr.ht/~user/llm-templates` repo:

```bash
llm -t srht:user/templatename
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-templates-sourcehut
python -m venv venv
source venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
llm install -e '.[test]'
```

To run the tests:

```bash
python -m pytest
```
