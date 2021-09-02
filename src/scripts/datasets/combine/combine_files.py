import os
import pandas as pd
from utils.globals import DATASETS
from utils.walkers.directory_walker import get_list_of_files

# directory to contain the combined title data.
combined_directory = os.path.abspath(f"{DATASETS}/Combined")

# error message for not found files
file_error = "Filtered file \'{}\' not found."

def create_combined_directory() -> None:
    """
    Create the directory that will hold the newly combined dataset.
    """
    if not os.path.isdir(combined_directory):
        os.mkdir(combined_directory)


def get_combined_file(raw_data_path) -> str:
    """
    Return the path to the combined data.
    :param raw_data_path: The path to the initial data file that is to be combined.
    :return: The filepath to the combined data.
    """
    return os.path.abspath(f"{combined_directory}/{os.path.basename(raw_data_path)}")

def combine_title_files() -> bool:
    """
    Combine all three title files into one file called title.combined.tsv.
    :return: whether or not combination was successful
    """
    # This will become the new combined file.
    combined_file = get_combined_file(DATASETS + "/Combined/title.combined.tsv")

    create_combined_directory()

    # only perform the combination if the file does not exist.
    if not os.path.isfile(combined_file):
        filtered_tsv_files = get_list_of_files(DATASETS + "/Filtered/", file_type=".tsv")

        akas_df = None
        basics_df = None
        ratings_df = None

        akas_df_initialized = False
        basics_df_initialized = False
        ratings_df_initialized = False

        # Read title.akas.tsv into pandas dataframe
        for tsv_file in filtered_tsv_files:
            if 'title.akas.tsv' in tsv_file:
                akas_df = pd.read_csv(tsv_file, sep="\t", dtype={'isOriginalTitle': str})
                akas_df_initialized = True

        if not akas_df_initialized:
            print(file_error.format("title.akas.tsv"))
            return False

        # Read title.basics.tsv into pandas dataframe
        for tsv_file in filtered_tsv_files:
            if 'title.basics.tsv' in tsv_file:
                basics_df = pd.read_csv(tsv_file, sep="\t")
                basics_df_initialized = True

        if not basics_df_initialized:
            print(file_error.format("title.basics.tsv"))
            return False

        # Read title.ratings.tsv into pandas dataframe
        for tsv_file in filtered_tsv_files:
            if 'title.ratings.tsv' in tsv_file:
                ratings_df = pd.read_csv(tsv_file, sep="\t")
                ratings_df_initialized = True

        if not ratings_df_initialized:
            print(file_error.format("title.ratings.tsv"))
            return False

        # Combine files
        partially_combined_df = akas_df.merge(ratings_df, on='tconst', how='outer')
        fully_combined_df = partially_combined_df.merge(basics_df, on='tconst', how='outer')

        # Write out files
        fully_combined_df.to_csv(combined_file, sep='\t')

        return True