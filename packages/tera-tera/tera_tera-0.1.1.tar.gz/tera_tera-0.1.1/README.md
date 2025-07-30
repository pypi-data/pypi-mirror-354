# tera-tera

[![PyPI](https://img.shields.io/pypi/v/tera-tera.svg)](https://pypi.org/project/tera-tera/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/tera-tera?include_prereleases&label=changelog)](https://github.com/sukhbinder/tera-tera/releases)
[![Tests](https://github.com/sukhbinder/tera-tera/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/tera-tera/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/tera-tera/blob/master/LICENSE)

Tera tera app to do langar seva at various gurudwara's

![Gurudwara Langar Seva](https://raw.githubusercontent.com/sukhbinder/tera-tera/main/langar.png)

## Installation

Install this tool using `pip`:
```bash
pip install tera-tera
```
## Usage

For help, run:
```bash
teratera --help
```
You can also use:
```bash
python -m teratera --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd tera-tera
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
