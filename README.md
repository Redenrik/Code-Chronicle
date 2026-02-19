# Code Chronicle

Code Chronicle is a Python-based project explorer that generates file indices and script summaries while respecting `.gitignore` patterns. The project includes a GUI built with PyQt5 so users can browse folders, choose output options, and generate files without memorizing CLI flags.

## What it generates

- `scripts-list.txt`: concatenated content of supported project files, with a short header.
- `00_file-index.txt`: readable tree index of files/folders.

Both outputs honor `.gitignore` exclusions (except negation rules such as `!pattern`, which are intentionally unsupported).

## Quick start (no terminal required)

### Windows

1. Download/clone the project.
2. Double-click `run.bat`.

### macOS / Linux

1. Download/clone the project.
2. Double-click `run.sh` (or run `./run.sh` once from Terminal if your file manager requires execute permission confirmation).

The launcher scripts:

- create a local virtual environment in `.venv` (inside the project folder),
- install dependencies from `requirements.txt` into that virtual environment,
- run the GUI.

This keeps dependencies local to the project and avoids global package pollution.

## CLI usage

```bash
python src/file_explorer_summary.py [folder] [--summary] [--index] [--output OUTPUT_DIR]
```

- `folder` (optional): project folder to inspect. Defaults to the current directory.
- `--summary`: generate `scripts-list.txt`.
- `--index`: generate `00_file-index.txt`.
- `--output`: output directory for generated files. Defaults to the current directory.

If neither `--summary` nor `--index` is provided, Code Chronicle generates both outputs.

## Features

- Folder picker-based GUI.
- Defaults to generating both summary and index.
- Prevents running with invalid folders.
- Writes GUI outputs into `chronicle-history/`.
- Platform-aware opening behavior:
  - Windows: `os.startfile`
  - macOS: `open`
  - Linux: `xdg-open`
- Stable sorting for deterministic outputs.

## Notes

- Supported summary extensions: `.doc`, `.txt`, `.json`, `.py`, `.env`, `.bat`, `.html`, `.js`, `.css`, `.ini`.
- `.gitignore` negation entries (`!`) are skipped by design.

## Contributing

Issues and pull requests are welcome.
