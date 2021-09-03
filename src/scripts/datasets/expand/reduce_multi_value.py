import os
import csv
from utils.globals import DATASETS

# from utils.walkers.directory_walker import get_list_of_files

# directory to contain the combined title data.
expanded_directory = os.path.abspath(f"{DATASETS}/Expanded")

# error message for not found files
file_error = "Combined file \'{}\' not found."


def create_expanded_directory() -> None:
    """
    Create the directory that will hold the newly expanded dataset.
    """
    if not os.path.isdir(expanded_directory):
        os.mkdir(expanded_directory)


def get_expanded_file(raw_data_path: str) -> str:
    """
    Return the path to the expanded data.
    :param raw_data_path: The path to the initial data file that is to be expanded.
    :return: The filepath to the expanded data.
    """
    return os.path.abspath(f"{expanded_directory}/{os.path.basename(raw_data_path)}")


def reduce_multi_values_for_title() -> None:
    """
    Reduces the multi valued attribute genre in the expanded title file
    """
    # This will become the newly expanded file.
    expanded_file = get_expanded_file(DATASETS + "/Expanded/title.expanded.tsv")

    create_expanded_directory()

    print('Beginning expansion process...')

    # only perform the expansion if the file does not exist.
    if not os.path.isfile(expanded_file):

        print(f'\tExpanding \'{expanded_file}\'...')

        # Read the combined input.
        with open(DATASETS + "/Combined/title.combined.tsv", mode='r', encoding='utf-8') as combined_data:
            raw_tsv_file = csv.reader(combined_data, delimiter='\t')

            # Write expanded data.
            with open(expanded_file, mode='w', encoding='utf-8', newline='') as filtered_file:
                writer = csv.writer(filtered_file, delimiter='\t')

                for index, line in enumerate(raw_tsv_file):

                    # Write the header
                    if index == 0:
                        writer.writerow(line)
                        continue

                    list_of_genres = str(line[-1]).split(',')

                    # reducing the multi-valued properties
                    for genre in list_of_genres:
                        writer.writerow(
                            [line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8],
                             line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], genre])

            print(f'Expansion process complete.')
    else:
        print(f'No file to expand since \'{expanded_file}\' already exists.')
