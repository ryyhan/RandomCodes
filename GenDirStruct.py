import os
import sys

def generate_directory_structure(path, indent=''):
    """
    Generates a string representing the directory structure of a given path.

    Args:
        path (str): The starting path (folder or file).
        indent (str): The current indentation string for visual representation.

    Returns:
        str: A string showing the directory structure.
    """
    structure = []
    try:
        entries = sorted(os.listdir(path))
    except OSError as e:
        return f"{indent}Error reading directory {path}: {e}"

    for i, entry in enumerate(entries):
        entry_path = os.path.join(path, entry)
        is_last = (i == len(entries) - 1)
        # Determine the prefix for the current entry based on whether it's the last one
        prefix = "└── " if is_last else "├── "
        # Determine the new indentation for sub-entries
        next_indent = indent + ("    " if is_last else "│   ")

        # Add the current entry to the structure list
        structure.append(f"{indent}{prefix}{entry}")

        # If it's a directory, recursively call the function to get its sub-structure
        if os.path.isdir(entry_path):
            structure.append(generate_directory_structure(entry_path, next_indent))
    # Join all parts of the structure with newline characters
    return "\n".join(structure)

if __name__ == "__main__":
    # Check if a folder path argument is provided
    if len(sys.argv) < 2:
        print("Usage: python GenDirStruct.py <folder_path>")
        print("Example: python GenDirStruct.py /home/user/my_project")
        sys.exit(1) # Exit with an error code

    target_folder_path = sys.argv[1]

    # Validate the provided path
    if not os.path.exists(target_folder_path):
        print(f"Error: Path '{target_folder_path}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(target_folder_path):
        print(f"Error: Path '{target_folder_path}' is not a directory.")
        sys.exit(1)

    # Print the parent folder name first
    print(os.path.basename(target_folder_path))

    # Generate and print the directory structure starting from the target folder
    structure_output = generate_directory_structure(target_folder_path)
    print(structure_output)
