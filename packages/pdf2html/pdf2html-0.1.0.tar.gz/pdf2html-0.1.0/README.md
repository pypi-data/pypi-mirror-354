# pdf2html

[![CI](https://github.com/synaptechlabs/pdf2html/actions/workflows/ci.yml/badge.svg)](https://github.com/synaptechlabs/pdf2html/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/synaptechlabs/pdf2html/branch/main/graph/badge.svg)](https://codecov.io/gh/synaptechlabs/pdf2html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/pdf2html.svg)](https://pypi.org/project/pdf2html/)
[![Docker](https://img.shields.io/docker/v/synaptechlabs/pdf2html?sort=semver)](https://hub.docker.com/r/synaptechlabs/pdf2html)



Convert PDF files to simple, readable HTML using a command-line tool.

## Features
- Converts single PDFs or entire folders
- Retains original filenames
- Simple, semantic HTML output
- CLI-friendly and pip-installable

## Installation
### Option 1: Local install
```bash
pip install .
```

### Option 2: pipx (recommended)
```bash
pipx install path/to/pdf2html/
```

## Usage
Convert a single file:
```bash
pdf2html path/to/file.pdf -o output_folder
```

Convert all PDFs in a folder:
```bash
pdf2html path/to/folder -o output_folder
```

## Requirements
- Python 3.8+
- `pdfminer.six`
- `beautifulsoup4`

## License
MIT
