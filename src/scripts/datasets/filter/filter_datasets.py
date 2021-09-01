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


def filter_title_akas(raw_data_path: str, dict_of_movie_ids: dict = None) -> dict:
    """
    Filter the title.akas.tsv file.
    :param raw_data_path: The file path to the raw data.
    :param dict_of_movie_ids: Dictionary containing titleId's that map to US-related movies..
    :return: A dictionary containing all of the title id's associated with movies with the US as their region.
    """
    # Dictionary to contain the title_id's (tconst's)
    # The dictionary will be set up as { title_id : None } since the dictionary will be used for
    # constant lookup for future filtering.
    title_id_dictionary = {}

    # This will become the newly filtered file.
    filtered_file_directory = get_filtered_file(raw_data_path)

    create_filtered_directory()

    # delete the previously filtered file to allow for performing a re-filter.
    if os.path.isfile(filtered_file_directory) and dict_of_movie_ids is not None:
        os.remove(filtered_file_directory)

    # only perform the filter if the file does not exist.
    if not os.path.isfile(filtered_file_directory):

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

                    if region == 'US' and (title_id not in title_id_dictionary and dict_of_movie_ids is None) or \
                            region == 'US' and (dict_of_movie_ids is not None and title_id in dict_of_movie_ids):
                        writer.writerow(line)
                        title_id_dictionary[line[0]] = None

                    # if region == 'US' and dict_of_movie_ids is None and title_id not in title_id_dictionary:

    return title_id_dictionary


def filter_title_basics(raw_data_path: str, dict_of_title_ids: dict) -> dict:
    """
    Filter the title.basics.tsv file.
    :param raw_data_path: The file path to the raw data.
    :param dict_of_title_ids: Dictionary containing all of the title's that have the US as their region.
    """
    # This will become the newly filtered file.
    filtered_file_directory = get_filtered_file(raw_data_path)

    create_filtered_directory()
    ret = {}

    # only perform the filter if the file does not exist.
    if not os.path.isfile(filtered_file_directory):

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

                    tconst = line[0]
                    title_type = str(line[1])

                    if tconst in dict_of_title_ids and 'movie' in title_type.lower():
                        # list_of_genres = str(line[8]).split(',')

                        writer.writerow(
                            [tconst, title_type, line[2], line[3], line[4], line[5], line[6], line[7], line[7]])
                        ret[tconst] = None
                    # else:
                    #     if tconst in dict_of_title_ids:
                    #         # update the dictionary and remove the non-movie related title.
                    #         del dict_of_title_ids[tconst]
                        # reducing the multi-valued properties
                        # for genre in list_of_genres:
                        #     writer.writerow(
                        #         [tconst, title_type, line[2], line[3], line[4], line[5], line[6], line[7], genre])

    return ret


def filter_title_ratings(raw_data_path: str, dict_of_title_ids: dict) -> None:
    """
    Filter the title.ratings.tsv file.
    :param raw_data_path: The file path to the raw data.
    :param dict_of_title_ids: Dictionary containing all of the title's that have the US as their region.
    """
    # This will become the newly filtered file.
    filtered_file_directory = get_filtered_file(raw_data_path)

    create_filtered_directory()

    # only perform the filter if the file does not exist.
    if not os.path.isfile(filtered_file_directory):

        # Read the original input.
        with open(raw_data_path, mode='r', encoding='utf-8') as raw_data:
            raw_tsv_file = csv.reader(raw_data, delimiter='\t')

            # Write filtered data.
            with open(filtered_file_directory, mode='w', encoding='utf-8', newline='') as filtered_file:
                writer = csv.writer(filtered_file, delimiter='\t')

                for index, line in enumerate(raw_tsv_file):

                    if index == 0:
                        writer.writerow(line)
                        continue

                    tconst = line[0]

                    if tconst in dict_of_title_ids:
                        writer.writerow([tconst, line[1], line[2]])


def filter_name_basics(raw_data_path: str, dict_of_title_ids: dict) -> None:
    """
    Filter the name.basics.tsv file.
    :param raw_data_path: The file path to the raw data.
    :param dict_of_title_ids: Dictionary containing all of the title's that have the US as their region.
    """
    # This will become the newly filtered file.
    filtered_file_directory = get_filtered_file(raw_data_path)

    create_filtered_directory()

    # only perform the filter if the file does not exist.
    if not os.path.isfile(filtered_file_directory):

        # Read the original input.
        with open(raw_data_path, mode='r', encoding='utf-8') as raw_data:
            raw_tsv_file = csv.reader(raw_data, delimiter='\t')

            # Write filtered data.
            with open(filtered_file_directory, mode='w', encoding='utf-8', newline='') as filtered_file:
                writer = csv.writer(filtered_file, delimiter='\t')

                # re-write the header by having tconst be the first column and remove 'knownForTitles'.
                writer.writerow(['tconst', 'nconst', 'primaryName', 'deathYear', 'primaryProfession'])

                # skip the header file
                next(raw_tsv_file)

                for line in raw_tsv_file:
                    titles_known_for = str(line[5]).split(',')

                    # reducing the multi-valued properties
                    for tconst in titles_known_for:

                        if tconst in dict_of_title_ids:
                            professions = str(line[4]).split(',')

                            # reducing the multi-valued properties
                            for profession in professions:
                                writer.writerow([tconst, line[0], line[1], line[2], line[3], profession])


def filter_files() -> None:
    """
    Filter name.basics.tsv, title.akas.tsv, title.basics.tsv, and title.ratings.tsv.
    :return:
    """
    # time is only here for debugging purposes to determine how long it takes to filer.
    import time
    tsv_files = get_list_of_files(DATASETS, file_type=".tsv")

    print("Beginning filtering process...")

    # pop title.akas.tsv from the array.
    title_akas_file = tsv_files.pop(1)

    print(f"\tfiltering '{title_akas_file}'...")

    # create a dictionary of title_id's from the title.akas.tsv file.
    dict_of_ids = filter_title_akas(title_akas_file)

    for file in tsv_files:
        print(f"\tfiltering '{file}'...")
        if 'name.basics.tsv' in file:
            filter_name_basics(file, dict_of_ids)
        elif 'title.basics.tsv' in file:
            dict_of_ids = filter_title_basics(file, dict_of_ids)
        elif 'title.ratings.tsv' in file:
            filter_title_ratings(file, dict_of_ids)

    print(f"\tfiltering '{title_akas_file}' once more...")
    filter_title_akas(title_akas_file, dict_of_movie_ids=dict_of_ids)

    print("Filtering processes complete.")
