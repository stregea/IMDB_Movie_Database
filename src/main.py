from argparse import ArgumentParser, Namespace
from scripts.datasets.extract_datasets.extract_datasets import extract_dataset_files
from scripts.database.database_startup.database_startup import initialise_database
# from scripts.database.database_populating.populate_database import run
from scripts.filter.filter_data import filter_files


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
    extract_dataset_files()
    initialise_database()
    filter_files()
    # run()


if __name__ == '__main__':
    main()
