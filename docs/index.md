# Welcome to Surveyor

Surveyor is a tool for generating architecture diagrams from existing cloud infrastructure. 

## Limitations
Surveyor is a work in progress and has the following limitations:
- AWS only not GCP nor Azure support/
- Limited Services Supported
- Single AWS account per diagram

## What does the tool do

- Scan your AWS account for resources which are supported
- Link the resources by their ARN
- Diagram this as a graphviz gaph
- Appy AWS icons to the graph nodes.
- Write as PNG


## Installation
```bash
pip install infra_surveyor
```


## Usage
Surveyor is build as a explorable command line application using click.

Example commands shown below

* `surveyor --help` - List sub commands.
* `surveyor survey-aws` - List the diagrams available to be created
* `surveyor survey-aws events` - Create the events diagram

### Common Options

| Option     | Default    | Description                       |
|------------|------------|-----------------------------------|
| --out_dir  | .          | Directory to write the diagram to |
| --out_file | aws-events | File name to use                  |
| --out_ext  | png        | File Extension to use             |


