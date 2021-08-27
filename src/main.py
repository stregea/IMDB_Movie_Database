from argparse import ArgumentParser, Namespace
from scripts.extract_datasets import extract_dataset_files


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


if __name__ == '__main__':
    main()
