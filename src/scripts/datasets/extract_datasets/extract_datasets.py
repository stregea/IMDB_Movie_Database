import gzip
import os
import shutil
from utils.globals import DATASETS
from utils.logger.logger import log
from utils.walkers.directory_walker import get_list_of_files


def extract_dataset_files() -> None:
    """
    Extract the .tsv files from their zipped versions.
    """
    datasets = get_list_of_files(directory=DATASETS, file_type=".gz")
    files_have_been_extracted = False

    print('Beginning extraction process...')
    for dataset in datasets:
        dataset_extract_name = dataset.split(".gz")[0]

        # only perform the extract if the file doesn't exist
        if not os.path.isfile(dataset_extract_name):

            # Unzip the gzip file
            with gzip.open(dataset, 'rb') as f_in:
                with open(dataset_extract_name, 'wb') as f_out:
                    print(f'\tExtracting \'{dataset_extract_name}\'...')
                    log(f'Beginning extract for \'{dataset_extract_name}\' from \'{dataset}\'.')

                    # perform the extract
                    shutil.copyfileobj(f_in, f_out)

                    log(f'\'{dataset_extract_name}\' has successfully been extracted from \'{dataset}\'.')
                    files_have_been_extracted = True

    if files_have_been_extracted:
        print('Extraction process complete.')
    else:
        print('Nothing to extract.')


if __name__ == '__main__':
    extract_dataset_files()
