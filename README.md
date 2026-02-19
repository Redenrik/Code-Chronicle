# Code Chronicle

Code Chronicle is a Python-based project explorer that generates file indices and script summaries while respecting .gitignore patterns. The project contains a user-friendly GUI built with PyQt5, allowing users to browse folders, select options, and create outputs. This tool can simplify the process of providing full projects to language models (e.g., GPT) as input, by aggregating relevant code and text files into a single summary file.

## Installation and Usage

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Install and Run

1. Clone the repository or download the source code.
2. Navigate to the Code Chronicle folder.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the GUI with `python src/gui.py` (requires a desktop environment).
5. Or run the CLI with `python src/file_explorer_summary.py <folder>`.

If no `--summary` / `--index` flags are provided, the CLI now generates both outputs by default.

The optional Windows `run.bat` script still installs dependencies and launches the GUI in one step.

## Features

- Browse and select a project folder.
- Generate a script summary that consolidates relevant code and text files, making it easy to provide full projects to language models as input.
- Preserve original source comments/docstrings in generated script summary outputs so code documentation is not lost.
- Prefix exported summary files with a short documentation header describing verbatim export behavior.
- Generate a file index that lists all files in the project, excluding those specified in the .gitignore file.
- Automatically saves output files to a "chronicle-history" folder.

## Contributing

Feel free to submit issues, feature requests, or pull requests. Your feedback and contributions are welcome and appreciated.
