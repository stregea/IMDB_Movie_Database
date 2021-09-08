import sys
from argparse import ArgumentParser, Namespace
from scripts.datasets.extract_datasets.extract_datasets import extract_dataset_files
from scripts.database.database_startup.database_startup import initialise_database
# from scripts.database.database_populating.populate_database import run
from scripts.datasets.filter.filter_datasets import filter_files
from scripts.datasets.combine.combine_files import combine_title_files
from scripts.datasets.combine.combine_files import combine_name_file
from scripts.datasets.expand.reduce_multi_value import reduce_multi_values_for_title


def setup_args() -> Namespace:
    """
    TODO: Add future/potential arguments.
    Setup the commandline arguments.
    :return: The argument parser object containing the parameters.
    """
    parser = ArgumentParser()
    return parser.parse_args()


def main() -> None:
    """
    Run the application.
    """
    import time
    start = time.time()
    extract_dataset_files()
    initialise_database()
    filter_files()

    if not combine_title_files():
        sys.exit("Error occurred combining files.")
    
    reduce_multi_values_for_title()
    
    combine_name_file()

    print(f"Processes took {(time.time()-start) / 60} minutes.")
    # run()


if __name__ == '__main__':
    main()
