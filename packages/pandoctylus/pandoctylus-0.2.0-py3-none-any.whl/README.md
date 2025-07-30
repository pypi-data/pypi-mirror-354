# Pandoctylus

![Pandoctylus Logo](doc/pandoctylus_small.png)

A crazy and opinionated way of generating documents.

## Installation

```bash
pip install pandoctylus
```

## Use

Check out the example project in [examples/project1](examples/project1) to understand
how to make a document. Key ingredients:
- define the document as yaml file in `docs/` sub-dir
- create or pick an existing jinja template and refernece it in the yaml file
- create or pick an existing docx template and reference it in the yaml file
- run the tool: 
  ```bash
  python pandoctylus/pandoctylus.py \
    --root-dir examples/project1 \
    --output-dir ./output
  ```
- enjoy the generated docs in `./output`

## Development

This project uses modern Python packaging with `pyproject.toml`. To set up the development environment:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pandoctylus.git
cd pandoctylus
```

2. Create a virtual environment and install development dependencies:

```bash
uv venv pandoctylus-venv
source .pandoctylus-venv/bin/activate 
uv pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## Packaging and Publishing

To build and publish the package to PyPI:

1. Install build tools:
```bash
uv pip install build twine
```

2. Build the package:
```bash
python -m build
```

3. Verify the distributions:
```bash
python -m twine check dist/*
```

4. Upload to PyPI:
```bash
python -m twine upload dist/*
```

The package will be available at https://pypi.org/project/pandoctylus/

## Features

- Generate multiple documents from shared Markdown and YAML and a docx template.

## License

MIT License 
