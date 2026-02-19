"""Core utilities for generating repository summaries and file indices.

This module is intentionally conservative when exporting file contents: source files are
copied as-is (including comments and blank lines) so the generated `.txt` bundle preserves
documentation context for downstream readers and tools.
"""

import os
import fnmatch
from typing import List


def get_ignore_patterns(selected_folder: str, extra_ignore: List[str] | None = None) -> List[str]:
    """Return ignore patterns from .gitignore and built-in rules."""
    ignore_patterns: List[str] = []

    ignore_patterns.extend([".git", ".gitignore"])

    gitignore_file = os.path.join(selected_folder, ".gitignore")
    if os.path.exists(gitignore_file):
        with open(gitignore_file, "r", encoding="utf-8") as file:
            gitignore_patterns = [
                line.strip()
                for line in file.read().splitlines()
                if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("!")
            ]
            ignore_patterns.extend(gitignore_patterns)

    if extra_ignore:
        ignore_patterns.extend(extra_ignore)

    return ignore_patterns


def is_path_excluded(filepath: str, root: str, ignore_patterns: List[str]) -> bool:
    """Return True if filepath should be ignored."""
    relative_filepath = os.path.relpath(filepath, root).replace(os.sep, "/")
    basename = os.path.basename(filepath)
    is_dir = os.path.isdir(filepath)

    for pattern in ignore_patterns:
        normalized_pattern = pattern.replace("\\", "/").rstrip()
        if not normalized_pattern:
            continue

        if normalized_pattern.endswith("/"):
            dir_pattern = normalized_pattern.rstrip("/")
            if relative_filepath == dir_pattern or relative_filepath.startswith(f"{dir_pattern}/"):
                return True
            if "/" not in dir_pattern and dir_pattern in relative_filepath.split("/"):
                return True

        if fnmatch.fnmatch(relative_filepath, normalized_pattern):
            return True

        if "/" not in normalized_pattern and fnmatch.fnmatch(basename, normalized_pattern):
            return True

        if is_dir and fnmatch.fnmatch(f"{relative_filepath}/", normalized_pattern):
            return True

    return False


def get_file_paths(directory: str, ignore_patterns: List[str]) -> List[str]:
    """Return list of file paths filtered by allowed extensions."""
    file_paths: List[str] = []
    allowed_extensions = [
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
    ]

    for root, dirs, files in os.walk(directory):
        # Remove ignored directories from dirs to avoid further exploration
        dirs[:] = sorted(
            [d for d in dirs if not is_path_excluded(os.path.join(root, d), directory, ignore_patterns)]
        )

        for file in sorted(files):
            filepath = os.path.join(root, file)
            if any(file.endswith(extension) for extension in allowed_extensions) and not is_path_excluded(filepath, directory, ignore_patterns):
                file_paths.append(filepath)
    return file_paths


def create_output_file(file_paths: List[str], output_file_name: str = "scripts-list.txt") -> None:
    """Write concatenated file contents to ``output_file_name``.

    The content is copied verbatim from source files. In particular, comment lines are
    *not* filtered so inline documentation is preserved in the generated report.
    """
    with open(output_file_name, "w", encoding="utf-8") as output_file:
        output_file.write(
            "# Code Chronicle export\n"
            "# Source text is copied verbatim, including inline comments/docstrings.\n\n"
        )

        for file_path in file_paths:
            output_file.write(f"########## {file_path} ##########\n")
            with open(file_path, "r", encoding="utf-8", errors="ignore") as input_file:
                # Keep the original file text unchanged (including comments/docstrings).
                content = input_file.read()
                output_file.write(content)
            output_file.write("\n\n")


def list_files(startpath: str, ignore_patterns: List[str], output_file_name: str = "00_file-index.txt") -> None:
    """Write a tree-like file index for ``startpath``."""

    def write_tree(current_path: str, prefix: str, file_handle) -> None:
        entries = []
        for entry in os.listdir(current_path):
            full_path = os.path.join(current_path, entry)
            if not is_path_excluded(full_path, startpath, ignore_patterns):
                entries.append(entry)

        entries.sort()
        for index, entry in enumerate(entries):
            full_path = os.path.join(current_path, entry)
            is_last = index == len(entries) - 1
            connector = "└── " if is_last else "├── "

            if os.path.isdir(full_path):
                file_handle.write(f"{prefix}{connector}{entry}/\n")
                write_tree(full_path, prefix + ("    " if is_last else "│   "), file_handle)
            else:
                file_handle.write(f"{prefix}{connector}{entry}\n")

    with open(output_file_name, "w", encoding="utf-8") as f:
        f.write(f"{os.path.basename(os.path.abspath(startpath))}/\n")
        write_tree(startpath, "", f)



if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="Generate summaries or indices for a project")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to scan")
    parser.add_argument("--summary", action="store_true", help="Generate script summary")
    parser.add_argument("--index", action="store_true", help="Generate file index")
    parser.add_argument("--output", default="chronicle-history", help="Output directory")
    args = parser.parse_args()

    selected_folder = os.path.abspath(args.folder)
    os.makedirs(args.output, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    extra_ignore = []
    if os.path.commonpath([selected_folder, os.path.abspath(args.output)]) == os.path.abspath(selected_folder):
        extra_ignore.append(os.path.relpath(os.path.abspath(args.output), selected_folder))

    ignore_patterns = get_ignore_patterns(selected_folder, extra_ignore)

    if not args.summary and not args.index:
        args.summary = True
        args.index = True

    if args.summary:
        output_file = os.path.join(
            args.output,
            f"{os.path.basename(selected_folder)}_scripts-list_{timestamp}.txt",
        )
        file_paths = get_file_paths(selected_folder, ignore_patterns)
        create_output_file(file_paths, output_file)
        print(f"Script summary saved to {output_file}")

    if args.index:
        output_file = os.path.join(
            args.output,
            f"{os.path.basename(selected_folder)}_file-index_{timestamp}.txt",
        )
        list_files(selected_folder, ignore_patterns, output_file)
        print(f"File index saved to {output_file}")
