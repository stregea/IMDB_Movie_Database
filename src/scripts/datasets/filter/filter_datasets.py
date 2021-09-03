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


def get_us_based_title_ids(raw_data_path) -> dict:
    """
    Return a dictionary containing ID's of US-based movies from the title.akas.tsv file.
    :param raw_data_path: The file path to the raw data.
    :return: A dictionary containing all of the title id's with the US as their region.
    """
    # Dictionary to contain the title_id's (tconst's)
    # The dictionary will be set up as { title_id : None } since the dictionary will be used for
    # constant lookup for future filtering.
    title_id_dictionary = {}

    # This will become the newly filtered file.
    filtered_file_directory = get_filtered_file(raw_data_path)

    create_filtered_directory()

    # only perform the filter if the file does not exist.
    if not os.path.isfile(filtered_file_directory):

        # Read the original input.
        with open(raw_data_path, mode='r', encoding='utf-8') as raw_data:
            raw_tsv_file = csv.reader(raw_data, delimiter='\t')

            for index, line in enumerate(raw_tsv_file):

                title_id = line[0]
                region = line[3]

                # only include movies that are regionally in the US and if their title id isn't in the dictionary.
                if region == 'US' and (title_id not in title_id_dictionary):
                    title_id_dictionary[line[0]] = None

    return title_id_dictionary


def filter_title_basics(raw_data_path: str, dict_of_title_ids: dict) -> dict:
    """
    Filter the title.basics.tsv file.
    :param raw_data_path: The file path to the raw data.
    :param dict_of_title_ids: Dictionary containing all of the US-based movie ID's.
    """
    # This will become the newly filtered file.
    filtered_file_directory = get_filtered_file(raw_data_path)

    create_filtered_directory()
    dict_of_us_based_movies = {}

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
                        writer.writerow(
                            [tconst, title_type, line[2], line[3], line[4], line[5], line[6], line[7], line[8]])
                        dict_of_us_based_movies[tconst] = None

    return dict_of_us_based_movies


def filter_title_akas(raw_data_path: str, dict_of_movie_ids: dict):
    """
    Filter the title.akas.tsv file.
    :param raw_data_path: The file path to the raw data.
    :param dict_of_movie_ids: Dictionary containing titleId's that map to US-related movies.
    :return: A dictionary containing all of the title id's associated with movies with the US as their region.
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

                    # Write the header
                    if index == 0:
                        writer.writerow(['tconst', line[1], line[2], line[3], line[4], line[5], line[6], line[7]])
                        continue

                    tconst = line[0]
                    region = line[3]

                    if region == 'US' and tconst in dict_of_movie_ids:
                        writer.writerow(line)


def filter_title_ratings(raw_data_path: str, dict_of_movie_ids: dict) -> None:
    """
    Filter the title.ratings.tsv file.
    :param raw_data_path: The file path to the raw data.
    :param dict_of_movie_ids: Dictionary containing titleId's that map to US-related movies.
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

                    if tconst in dict_of_movie_ids:
                        writer.writerow([tconst, line[1], line[2]])


def filter_name_basics(raw_data_path: str, dict_of_movie_ids: dict) -> None:
    """
    Filter the name.basics.tsv file.
    :param raw_data_path: The file path to the raw data.
    :param dict_of_movie_ids: Dictionary containing titleId's that map to US-related movies.
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

                        if tconst in dict_of_movie_ids:
                            professions = str(line[4]).split(',')

                            # reducing the multi-valued properties
                            for profession in professions:
                                writer.writerow([tconst, line[0], line[1], line[2], line[3], profession])


def filter_files() -> None:
    """
    Filter name.basics.tsv, title.akas.tsv, title.basics.tsv, and title.ratings.tsv.
    """
    tsv_files = get_list_of_files(DATASETS, file_type=".tsv")

    print("Beginning filtering process...")

    # Get title.akas.tsv from the array.
    title_akas_file = tsv_files[1]

    # Pop title.basics.tsv from the array.
    title_basics_file = tsv_files.pop(2)

    # Scan the 'title.akas.tsv' file and retrieve US-based cinema ID's.
    dict_of_us_title_ids = get_us_based_title_ids(title_akas_file)

    # Filter 'title.basics.tsv' and return a dictionary containing US-based movies.
    print(f"\tfiltering '{title_basics_file}'...")

    dict_of_us_based_movies = filter_title_basics(title_basics_file, dict_of_us_title_ids)

    for file in tsv_files:
        print(f"\tfiltering '{file}'...")
        if 'name.basics.tsv' in file:
            filter_name_basics(file, dict_of_us_based_movies)
        elif 'title.akas.tsv' in file:
            filter_title_akas(file, dict_of_us_based_movies)
        elif 'title.ratings.tsv' in file:
            filter_title_ratings(file, dict_of_us_based_movies)

    print("Filtering processes complete.")
