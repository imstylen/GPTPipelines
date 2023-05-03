import os
import json

def get_files_text(directory, extension_filter = ['.txt']):
    paths = []
    data = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extension_filter):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    try:
                        text = f.read()
                        data[path] = text
                        paths.append(path)
                    except Exception as e:
                        print(f"Error reading: {file}")
    return data, paths


            
    return paths,data

def get_all_file_paths(directory):
    """
    A function that uses os.walk to return a list of all file paths within a given directory including sub directories.

    Args:
        directory (str): The directory to search for files in.

    Returns:
        List[str]: A list of file paths.
    """
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def read_files(file_paths, skip_extensions=[]):
    """
    A function that accepts a list of files paths, and returns a list of strings of their contents.

    Args:
        file_paths (List[str]): A list of file paths.
        skip_extensions (List[str]): A list of file extensions to skip. Defaults to [].

    Returns:
        List[str]: A list of file contents.
    """
    file_contents = []
    for file_path in file_paths:
        if any(file_path.endswith(ext) for ext in skip_extensions):
            continue
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                if content != '':
                    file_contents.append(file_path + ':\n\n' + content)
        except Exception as e:
            print(f'Error reading file: {file_path}')
    return file_contents
