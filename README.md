# Code Chronicle

Code Chronicle is a Python-based project explorer that generates file indices and script summaries while respecting `.gitignore` patterns. The project contains a user-friendly GUI built with PyQt5, allowing users to browse folders, select options, and create outputs. This tool can simplify the process of providing full projects to language models (e.g., GPT) as input by aggregating relevant code and text files into a single summary file.

## Installation and Usage

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Install and Run GUI

1. Clone the repository or download the source code.
2. Navigate to the Code Chronicle folder.
3. Double-click on `run.bat` to install the required dependencies and launch the application in one shot.

The `run.bat` script will:

- Create a virtual environment (if not already present) in the project folder.
- Activate the virtual environment.
- Install the required dependencies from `requirements.txt`.
- Run the Project Explorer script (`gui.py`).

### CLI Usage

You can also generate outputs from the command line:

```bash
python src/file_explorer_summary.py [folder] [--summary] [--index] [--output OUTPUT_DIR]
```

- `folder` (optional): project folder to inspect. Defaults to the current directory.
- `--summary`: generate `scripts-list.txt`.
- `--index`: generate `00_file-index.txt`.
- `--output`: output directory for generated files. Defaults to the current directory.

If neither `--summary` nor `--index` is provided, Code Chronicle generates **both** outputs by default.

## Features

- Browse and select a project folder.
- Generate a script summary that consolidates relevant code and text files.
- Summary exports include a short documentation header and preserve source content verbatim, including comments, docstrings, and blank lines.
- Generate a readable tree-like file index with stable sorting.
- Respect `.gitignore` rules (including directory patterns) while traversing files.
- Automatically save GUI output files to a `chronicle-history` folder.
- Open generated files/folders with platform-aware behavior (`os.startfile` on Windows, `open` on macOS, and `xdg-open` on Linux).

## Contributing

Feel free to submit issues, feature requests, or pull requests. Your feedback and contributions are welcome and appreciated.
