# Generate Diagrams with LLM and Edit with Draw.io

Welcome to our repository, where we leverage Language Models (LLM) to generate diagrams and use Draw.io for further editing and refinement. Below, you'll find a detailed breakdown of the repository's structure and contents.

## Repository Structure

This repository is organized into several key directories, each serving a specific purpose in the workflow of generating, editing, and evaluating diagrams. Here's what you can expect to find in each:

### DFD Folder

- **Location:** `./DFD/`
- **Description:** Contains Data Flow Diagram (DFD) files generated by the LLM.

### Stories Folder

- **Location:** `./stories/`
- **Description:** Houses user stories or requirements files. These documents are used as inputs by the LLM to generate the initial DFDs, providing context and specifications for the desired diagrams.

### Evaluation App Folder

- **Location:** `./evaluation_app/`
- **Description:** Contains the evaluation application used by evaluators to assess the completeness and correctness of the generated diagrams. This tool facilitates the review process, allowing for systematic assessment of the diagrams against the user stories.

### Analysis Folder

- **Location:** `./analysis/`
- **Description:** This folder contains the evaluation results, the detailed evaluation in Excel files, including the performance analysis in Jupyter Notebook and the feedback on the diagrams created.

## Cite this work

```
@inproceedings{herwanto2024automating,
  title={Automating Data Flow Diagram Generation from User Stories Using Large Language Models},
  author={Herwanto, Guntur Budi},
  booktitle={7th Workshop on Natural Language Processing for Requirements Engineering},
  year={2024}
}
```
