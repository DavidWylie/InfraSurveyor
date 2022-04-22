[![Unit Tests](https://github.com/DavidWylie/Surveyor/workflows/UnitTests/badge.svg)](https://github.com/DavidWylie/Surveyor/actions/workflows/UnitTests)
[![codecov](https://codecov.io/gh/DavidWylie/Surveyor/branch/main/graph/badge.svg?token=H7GP0SZLN7)](https://codecov.io/gh/DavidWylie/Surveyor)
![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.8%2B&color=blue?style=flat-square&logo=python)
[![CodeQL](https://github.com/DavidWylie/Surveyor/workflows/CodeQuality/badge.svg)](https://github.com/DavidWylie/Surveyor/actions/workflows/CodeQuality)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# Surveyor
A tool to survey existing cloud infrastructure and document what exists.
This project is still in development and is not yet in use on a production system.  Diagrams are against AWS at the moment but this might not be required in the future.

## Releasing
```bash
pip install -e ".[dev]"
semantic-release publish --minor
```

This command will:
- bump the verison number
- create the git tag for the release
- push the tag

A github action will kick in to create the release in github when the tag is pushed.  The release will contain the files in the dist directory created by flit and license file.

## Why
When developing cloud infrastructure you tend to create Architecture diagrams.
These start reflecting the ideal of what should be built and may even match the initial implementation.  Over time due to pressures in development diagrams tend to get out of date.   Even with 'living' documentation it takes considerable time and effort to keep it current.

The idea of this project is to create standardised diagrams of various types for use in ci/cd pipelines (scheduled or change triggerred) based on the infrastructure that has already been deployed.  By being based on the infrastructure it should always reflect reality.

People are inherently visual creatures.  A visual representation of something is easier to talk over with a bussiness owner or project team than a textual one.  And the users might see patterns or problems in the solution which were not seen during development.

## Benefits of Auto Diagramming

Accurate diagrams exist for:
- Debugging
- Planning future work
- Auditing
- Approval of current state and new state.

# Diagrams being created:
The following are diagrams that this project intends to create

## Event Flow
This diagram is to show the flow of events form event bridge to the processing systems.  This includes queues, distribution topics and compute instances.  The ideal is to show a full data flow of the system from entry point to end of the process.

Supported services:
- Lambda
- SQS
- SNS
- Event Bridge

## VPC Network Security
In AWS it is important to understand your VPC network structure and what access is possible and what is denied.  This should include:
- Inbound security
- Outbound security
- Security groups and access
- Subnets and access
- Public and Private subnet mapping

Required Services:
- VPC
- NAT gateways
- VPN
- Subnets
- Security groups
- EC2
- VPC Endpoints
- Internet gateways

# Installation
To Install this on  Mac OSX install graphviz then the requiremewnts and the library.
```bash
brew install graphviz
cd src
pip install -e ".[dev]"
```

## Running the tool
Prequisites:
- AWS account
- AWS profile setup 
- AWS login with PROFILE and REGION defined in your environment via environment variables.

This is a self documenting commandline application so once installed you can run the command below to explore the project.
```bash
surveyor --help
```

# Dependencies
- Graphviz - Graphing library
- Boto3 - AWS SDK library
- Click - A command line building library
