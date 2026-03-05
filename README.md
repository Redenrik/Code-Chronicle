# Code Chronicle

Code Chronicle is a Python-based project explorer that generates file indices and script summary while respecting `.gitignore` patterns. The project includes a GUI built with PyQt5 so users can browse folders, choose output options, and generate files without memorizing CLI flags.

## What it generates

- `scripts-list.txt`: concatenated content of supported project files, with a short header.
- `00_file-index.txt`: readable tree index of files/folders.

Both outputs honor `.gitignore` exclusions with the compatibility notes listed below.

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

### `.gitignore` compatibility

Code Chronicle implements a practical subset of `.gitignore` behavior:

| Pattern type | Status | Example | Behavior |
| --- | --- | --- | --- |
| Basename / directory match | Supported | `node_modules` | Excludes matching directories/files at any depth. |
| Directory-only pattern (`/` suffix) | Supported | `build/` | Excludes the directory and its contents. |
| Wildcards | Supported | `*.log` | Excludes matching files by glob pattern. |
| Anchored root pattern (`/` prefix) | Supported | `/dist` | Matches paths from the selected folder root only. |
| Negation pattern (`!`) | Not supported | `!keep.txt` | Ignored by design (no re-include behavior). |

## Contributing

Issues and pull requests are welcome.
