# Code Chronicle

Code Chronicle is a Python-based project explorer that generates file indices and script summaries while respecting .gitignore patterns. The project contains a user-friendly GUI built with PyQt5, allowing users to browse folders, select options, and create outputs. This tool can simplify the process of providing full projects to language models (e.g., GPT) as input, by aggregating relevant code and text files into a single summary file.

## Installation and Usage

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Install and Run

1. Clone the repository or download the source code.
2. Navigate to the Code Chronicle folder.
3. Double-click on `run.bat` to install the required dependencies and launch the application in one shot.

The `run.bat` script will:

- Create a virtual environment (if not already present) in the project folder.
- Activate the virtual environment.
- Install the required dependencies from `requirements.txt`.
- Run the Project Explorer script (gui.py).

## Features

- Browse and select a project folder.
- Generate a script summary that consolidates relevant code and text files, making it easy to provide full projects to language models as input.
- Generate a file index that lists all files in the project, excluding those specified in the .gitignore file.
- Automatically saves output files to a "chronicle-history" folder.

## Contributing

Feel free to submit issues, feature requests, or pull requests. Your feedback and contributions are welcome and appreciated.
