import os


def get_list_of_files(directory: str, file_type: str) -> list:
    """
    Search a specified directory and add the file's specified by a file type to a list.
    :param directory: The directory to search.
    :param file_type: The type of file to add to the list.
    :return: A list of files within the specified directory.
    """
    ret = []

    for (root, subdirectories, files) in os.walk(directory):
        for file in files:
            if file.endswith(file_type):
                ret.append(os.path.abspath(os.path.join(root, file)))
    return ret
