import os
import fnmatch


def get_ignore_patterns(selected_folder):
    ignore_patterns = []  # Initialize ignore_patterns as an empty list
    
    script_filename = os.path.basename(__file__)
    ignore_patterns.extend([script_filename, '.git', '.gitignore'])

    gitignore_file = os.path.join(selected_folder, '.gitignore')
    if os.path.exists(gitignore_file):
        with open(gitignore_file, 'r') as file:
            gitignore_patterns = file.read().splitlines()
            ignore_patterns.extend(gitignore_patterns)

    return ignore_patterns


def is_path_excluded(filepath, root, ignore_patterns):
    relative_filepath = os.path.relpath(filepath, root)
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(relative_filepath, pattern):
            return True
        if os.path.isdir(filepath) and fnmatch.fnmatch(relative_filepath + os.sep, pattern):
            return True
    return False


def get_file_paths(directory, ignore_patterns):
    file_paths = []
    allowed_extensions = [".doc", ".txt", ".json", ".py", ".env", ".bat", ".html", ".js", ".css", "ini"]

    for root, dirs, files in os.walk(directory):
        # Remove ignored directories from dirs to avoid further exploration
        dirs[:] = [d for d in dirs if not is_path_excluded(os.path.join(root, d), directory, ignore_patterns)]
        
        for file in files:
            filepath = os.path.join(root, file)
            if any(file.endswith(extension) for extension in allowed_extensions) and not is_path_excluded(filepath, directory, ignore_patterns):
                file_paths.append(filepath)
    return file_paths

def create_output_file(file_paths, output_file_name="scripts-list.txt"):
    with open(output_file_name, "w", encoding="utf-8") as output_file:
        for file_path in file_paths:
            output_file.write(f"########## {file_path} ##########\n")
            with open(file_path, "r", encoding="utf-8", errors='ignore') as input_file:
                content = input_file.read()
                output_file.write(content)
            output_file.write("\n\n")


def list_files(startpath, ignore_patterns, output_file_name="00_file-index.txt"):
    with open(output_file_name, "w", encoding="utf-8") as f:
        folder_name = os.path.basename(os.path.abspath(startpath))
        f.write(f"{folder_name}/\n")
        for root, dirs, files in os.walk(startpath):
            dirs[:] = [d for d in dirs if not is_path_excluded(os.path.join(root, d), startpath, ignore_patterns)]
            level = root.replace(startpath, '').count(os.sep)
            indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
            if level == 0:
                subindent = ''
            else:
                is_last_file = False
                for i, file in enumerate(files):
                    if not is_path_excluded(os.path.join(root, file), startpath, ignore_patterns):
                        if i == len(files) - 1:
                            subindent = '│   ' * level + '└── '
                            is_last_file = True
                        else:
                            subindent = '│   ' * level + '├── '
                        f.write(f"{indent}{os.path.basename(root)}/\n")
                        break
                if is_last_file:
                    continue
            for i, file in enumerate(files):
                if not is_path_excluded(os.path.join(root, file), startpath, ignore_patterns):
                    if i == len(files) - 1:
                        subindent = '│   ' * level + '└── '
                    else:
                        subindent = '│   ' * level + '├── '
                    f.write(f"{subindent}{file}\n")



if __name__ == '__main__':
    current_directory = os.getcwd()

    # Get the folder path from the GUI
    selected_folder = os.path.abspath("path_to_the_selected_folder")  # Replace this with the actual folder path from the GUI

    # Get the ignore patterns
    ignore_patterns = get_ignore_patterns(selected_folder)

    # Generate the scripts-list.txt file
    file_paths = get_file_paths(current_directory, ignore_patterns)
    create_output_file(file_paths)

    # Generate the file_list.txt file
    start_path = '.'  # current directory
    list_files(start_path, ignore_patterns)