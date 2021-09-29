import sys
from argparse import ArgumentParser, Namespace
from scripts.datasets.extract_datasets.extract_datasets import extract_dataset_files
from scripts.database.database_startup.database_startup import initialise_database
# from scripts.database.database_populating.populate_database import run
from scripts.datasets.filter.filter_datasets import filter_files
from scripts.datasets.combine.combine_files import combine_title_files
from scripts.datasets.combine.combine_files import combine_name_file
from scripts.datasets.expand.reduce_multi_value import reduce_multi_values_for_title
from scripts.data_dictionary.data_dictionary_populate.populate_data_dictionary import create_data_dictionary

def setup_args() -> Namespace:
    """
    TODO: Add future/potential arguments.
    Setup the commandline arguments.
    :return: The argument parser object containing the parameters.
    """
    parser = ArgumentParser()

    parser.add_argument('-f',
                        '--filter',
                        help='filter and generate tsv data to be combined into one output file',
                        action='store_true')

    parser.add_argument('-dd',
                        '--data_dictionary',
                        help='generate a data dictionary for the database.',
                        action='store_true')
    return parser.parse_args()


def main() -> None:
    """
    Run the application.
    """

    args = setup_args()

    if args.filter:
        import time
        start = time.time()
        extract_dataset_files()
        initialise_database()
        filter_files()

        if not combine_title_files():
            sys.exit("Error occurred combining files.")

        reduce_multi_values_for_title()

        combine_name_file()

        print(f"Processes took {(time.time() - start) / 60} minutes.")

    if args.data_dictionary:
        create_data_dictionary()
    # run()


if __name__ == '__main__':
    main()
