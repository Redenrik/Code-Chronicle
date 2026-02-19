import argparse
import fnmatch
import os
from pathlib import Path

ALLOWED_EXTENSIONS = {
    ".doc",
    ".txt",
    ".json",
    ".py",
    ".env",
    ".bat",
    ".html",
    ".js",
    ".css",
    ".ini",
}

SUMMARY_HEADER = (
    "# Code Chronicle Summary\n"
    "# The file contents below are copied verbatim from the source files,\n"
    "# including comments, docstrings, and blank lines.\n\n"
)


def _normalize_relpath(path):
    normalized = path.replace("\\", "/").strip("/")
    return normalized


def _read_gitignore_patterns(selected_folder):
    patterns = []
    gitignore_file = os.path.join(selected_folder, ".gitignore")
    if not os.path.exists(gitignore_file):
        return patterns

    with open(gitignore_file, "r", encoding="utf-8", errors="ignore") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("!"):
                # Negation rules are intentionally not supported yet.
                continue
            patterns.append(line.replace("\\", "/"))
    return patterns


def get_ignore_patterns(selected_folder):
    script_filename = os.path.basename(__file__)
    ignore_patterns = [script_filename, ".git", ".git/"]
    ignore_patterns.extend(_read_gitignore_patterns(selected_folder))
    return ignore_patterns


def _pattern_matches(rel_path, pattern, is_dir):
    rel_path = _normalize_relpath(rel_path)
    pattern = pattern.replace("\\", "/")
    if not pattern:
        return False

    directory_only = pattern.endswith("/")
    pattern = pattern.rstrip("/")

    anchored = pattern.startswith("/")
    pattern = pattern.lstrip("/")
    if not pattern:
        return False

    candidates = [rel_path]
    if not anchored:
        parts = rel_path.split("/")
        candidates.extend(["/".join(parts[i:]) for i in range(1, len(parts))])

    for candidate in candidates:
        if directory_only and not is_dir:
            continue

        if fnmatch.fnmatch(candidate, pattern):
            return True

        if "/" not in pattern:
            if candidate == pattern or candidate.startswith(f"{pattern}/"):
                if not directory_only or is_dir or "/" in rel_path:
                    return True

        if directory_only and (candidate == pattern or candidate.startswith(f"{pattern}/")):
            return True

    return False


def is_path_excluded(filepath, root, ignore_patterns):
    rel_path = os.path.relpath(filepath, root)
    rel_path = _normalize_relpath(rel_path)
    is_dir = os.path.isdir(filepath)

    for pattern in ignore_patterns:
        if _pattern_matches(rel_path, pattern, is_dir):
            return True
    return False


def get_file_paths(directory, ignore_patterns):
    file_paths = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = sorted(
            d for d in dirs if not is_path_excluded(os.path.join(root, d), directory, ignore_patterns)
        )

        for file_name in sorted(files):
            file_path = os.path.join(root, file_name)
            if Path(file_name).suffix.lower() in ALLOWED_EXTENSIONS and not is_path_excluded(
                file_path, directory, ignore_patterns
            ):
                file_paths.append(file_path)

    return file_paths


def create_output_file(file_paths, output_file_name="scripts-list.txt"):
    with open(output_file_name, "w", encoding="utf-8") as output_file:
        output_file.write(SUMMARY_HEADER)
        for file_path in sorted(file_paths):
            output_file.write(f"########## {file_path} ##########\n")
            with open(file_path, "r", encoding="utf-8", errors="ignore") as input_file:
                output_file.write(input_file.read())
            output_file.write("\n\n")


def _build_tree_lines(startpath, ignore_patterns):
    root_name = os.path.basename(os.path.abspath(startpath))
    lines = [f"{root_name}/"]

    def walk_dir(path, prefix=""):
        entries = []
        for name in sorted(os.listdir(path)):
            full_path = os.path.join(path, name)
            if is_path_excluded(full_path, startpath, ignore_patterns):
                continue
            entries.append((name, full_path, os.path.isdir(full_path)))

        for index, (name, full_path, is_dir) in enumerate(entries):
            connector = "└── " if index == len(entries) - 1 else "├── "
            child_prefix = "    " if index == len(entries) - 1 else "│   "
            label = f"{name}/" if is_dir else name
            lines.append(f"{prefix}{connector}{label}")
            if is_dir:
                walk_dir(full_path, prefix + child_prefix)

    walk_dir(startpath)
    return lines


def list_files(startpath, ignore_patterns, output_file_name="00_file-index.txt"):
    lines = _build_tree_lines(startpath, ignore_patterns)
    with open(output_file_name, "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Generate Code Chronicle summary and/or file index.")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to inspect (default: current directory)")
    parser.add_argument("--summary", action="store_true", help="Generate summary output")
    parser.add_argument("--index", action="store_true", help="Generate file index output")
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory for generated files (default: current directory)",
    )
    args = parser.parse_args()

    selected_folder = os.path.abspath(args.folder)
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    generate_summary = args.summary
    generate_index = args.index
    if not generate_summary and not generate_index:
        generate_summary = True
        generate_index = True

    ignore_patterns = get_ignore_patterns(selected_folder)

    if generate_summary:
        summary_path = os.path.join(output_dir, "scripts-list.txt")
        file_paths = get_file_paths(selected_folder, ignore_patterns)
        create_output_file(file_paths, summary_path)

    if generate_index:
        index_path = os.path.join(output_dir, "00_file-index.txt")
        list_files(selected_folder, ignore_patterns, index_path)


if __name__ == "__main__":
    main()
