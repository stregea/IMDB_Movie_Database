import os
import csv
from utils.globals import DATASETS
from utils.walkers.directory_walker import get_list_of_files

# directory to contain the newly filtered data.
filtered_directory = os.path.abspath(f"{DATASETS}/Filtered")


def create_filtered_directory() -> None:
    """
    Create the directory that will hold the newly filtered dataset.
    """
    if not os.path.isdir(filtered_directory):
        os.mkdir(filtered_directory)


def get_filtered_file(raw_data_path) -> str:
    """
    Return the path to the filtered data.
    :param raw_data_path: The path to the initial data file that is to be filtered.
    :return: The filepath to the filtered data.
    """
    return os.path.abspath(f"{filtered_directory}/{os.path.basename(raw_data_path)}")


def filter_title_akas(raw_data_path: str) -> dict:
    """
    Filter the title.akas.tsv file.
    :param raw_data_path: The file path to the raw data.
    :return: A dictionary containing all of the title id's associated with movies with the US as their region.
    """
    # Dictionary to contain the title_id's (tconst's)
    # The dictionary will be set up as { title_id : None } since the dictionary will be used for
    # constant lookup for future filtering.
    title_id_dictionary = {}

    # This will become the newly filtered file.
    filtered_file_directory = get_filtered_file(raw_data_path)

    create_filtered_directory()

    # Read the original input.
    with open(raw_data_path, mode='r', encoding='utf-8') as raw_data:
        raw_tsv_file = csv.reader(raw_data, delimiter='\t')

        # Write filtered data.
        with open(filtered_file_directory, mode='w', encoding='utf-8', newline='') as filtered_file:
            writer = csv.writer(filtered_file, delimiter='\t')

            for index, line in enumerate(raw_tsv_file):

                # Write the header
                if index == 0:
                    writer.writerow(line)
                    continue

                title_id = line[0]
                region = line[3]

                # only include movies that are regionally in the US and if their title id isn't in the dictionary.
                if region == 'US' and title_id not in title_id_dictionary:
                    writer.writerow(line)
                    title_id_dictionary[line[0]] = None

    return title_id_dictionary


def filter_title_basics(raw_data_path: str, dict_of_title_ids: dict) -> None:
    """
    Filter the title.basics.tsv file.
    :param raw_data_path: The file path to the raw data.
    """
    # This will become the newly filtered file.
    filtered_file_directory = get_filtered_file(raw_data_path)

    create_filtered_directory()

    # Read the original input.
    with open(raw_data_path, mode='r', encoding='utf-8') as raw_data:
        raw_tsv_file = csv.reader(raw_data, delimiter='\t')

        # Write filtered data.
        with open(filtered_file_directory, mode='w', encoding='utf-8', newline='') as filtered_file:
            writer = csv.writer(filtered_file, delimiter='\t')

            for index, line in enumerate(raw_tsv_file):

                # Write the header
                if index == 0:
                    writer.writerow(line)
                    continue

                tconst = str(line[0])
                title_type = str(line[1])

                if tconst in dict_of_title_ids and 'movie' in title_type.lower():
                    list_of_genres = str(line[8]).split(',')

                    # write an entry for each entry
                    for genre in list_of_genres:
                        writer.writerow([tconst, title_type, line[2], line[3], line[4], line[5], line[6], line[7], genre])


def filter_files() -> None:
    """
    Filter name.basics.tsv, title.akas.tsv, title.basics.tsv, and title.ratings.tsv.
    :return:
    """
    # time is only here for debugging purposes to determine how long it takes to filer.
    import time
    tsv_files = get_list_of_files(DATASETS, file_type=".tsv")

    dict_of_ids = {}

    print("Beginning filtering process...")
    start = time.time()
    for file in tsv_files:
        print(f"\tfiltering '{file}'...")
        if 'title.akas.tsv' in file:
            dict_of_ids = filter_title_akas(file)
        elif 'title.basics.tsv' in file:
            # dict_of_ids will be populated by the time it reaches here to to how the list is sorted.
            filter_title_basics(file, dict_of_ids)

    print(f"Filtering completed in {time.time()-start} seconds")
