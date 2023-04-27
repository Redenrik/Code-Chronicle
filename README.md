# Code Chronicle

Code Chronicle is a Python-based project explorer that generates file indices and script summaries from a chosen directory. The user-friendly GUI, built with PyQt5, allows users to browse folders, select options, and create outputs. Gitignore patterns are respected for accurate file parsing.

## Requirements
- Python 3.x
- PyQt5
- pyinstaller (optional, for creating executable)

## Installation
1. Clone the repository or download the source code.
2. Create a virtual environment (optional): `python -m venv env`
3. Activate the virtual environment: `source env/bin/activate` (Linux/Mac) or `env\Scripts\activate.bat` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Run the script: `python src/gui.py`
2. Browse and select a project folder.
3. Choose the desired options: Generate script summary and/or Generate file index.
4. Click 'Generate' to create the output files in the 'chronicle-history' folder.
5. View the generated files with the 'History' button or by navigating to the 'chronicle-history' folder.

## Project Structure
- `src/gui.py`: Main script with PyQt5 GUI implementation.
- `src/file_explorer_summary.py`: Functions for file exploration, gitignore pattern handling, and output generation.
- `run.bat`: Batch script for setting up the virtual environment, installing dependencies, and running the script (Windows).
- `requirements.txt`: List of required Python packages.
