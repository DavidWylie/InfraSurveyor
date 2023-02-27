

[![PyPI version](https://badge.fury.io/py/infra-surveyor.svg)](https://badge.fury.io/py/infra-surveyor)
![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.8%2B&color=blue?style=flat-square&logo=python)
[![Documentation Status](https://readthedocs.org/projects/infrasurveyor/badge/?version=latest)](https://infrasurveyor.readthedocs.io/en/latest/?badge=latest)
[![Unit Tests](https://github.com/DavidWylie/Surveyor/workflows/UnitTests/badge.svg)](https://github.com/DavidWylie/Surveyor/actions/workflows/UnitTests)
[![codecov](https://codecov.io/gh/DavidWylie/InfraSurveyor/branch/main/graph/badge.svg?token=5J8QX2DK5H)](https://codecov.io/gh/DavidWylie/InfraSurveyor)
[![CodeQL](https://github.com/DavidWylie/Surveyor/workflows/CodeQuality/badge.svg)](https://github.com/DavidWylie/Surveyor/actions/workflows/CodeQuality)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



# Infra Surveyor
A tool to survey existing cloud infrastructure and document what exists.
This project is still in development and is not yet in use on a production system.  Diagrams are against AWS at the moment but this might not be required in the future.

# Installation
To Install this on  Mac OSX install graphviz then the requiremewnts and the library.
```bash
brew install graphviz
pip install infra_surveyor
```

## Installation for development
This project uses optional dependancies for development, documentation and release.
To develop on this project please clone the repository setup your virtual environment then run the following
```bash
pip install -e ".[dev]"
```

## Installation for documentation developers
To work on the documentation on this project please clone the repository setup your virtual environment then run the following
```bash
pip install -e ".[docs]"
```

This will install mkdocs which can be used to host the docs locally during writing.  The command below will host the docs in html format on your machine.
``` bash
mkdocs serve 
```

# Releasing
```bash
pip install -e ".[dev]"
semantic-release publish --minor
```

This command will:
- bump the verison number
- create the git tag for the release
- push the tag

A github action will kick in to create the release in github when the tag is pushed.  The release will contain the files in the dist directory created by flit and license file.

## Running the tool
Prequisites:
- AWS account
- AWS profile setup 
- AWS login with PROFILE and REGION defined in your environment via environment variables.

This is a self documenting commandline application so once installed you can run the command below to explore the project.
```bash
infra_surveyor --help
```

# Dependencies
- Graphviz - Graphing library
- Boto3 - AWS SDK library
- Click - A command line building library

The following are not required dependencies for using the tool but are used in development

| Tool                    | Description                          |
|-------------------------|--------------------------------------|
| black                   | code linter                          |
| coverage                | used to generate code coverage stats |
| docker                  | used to mock lambdas                 |
| flit                    | Python package building              |
| Github actions          | CI/CD processes                      |
| mkdocs                  | Documentation builder                |
| moto                    | AWS Mocking Library                  |
| pytest                  | test runner                          |
| python-semantic-release | Version management                   |
