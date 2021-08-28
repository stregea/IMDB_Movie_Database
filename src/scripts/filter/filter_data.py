import os
import csv
from utils.globals import DATASETS
from utils.walkers.directory_walker import get_list_of_files

# directory to contain the newly filtered data.
filtered_directory = os.path.abspath(f"{DATASETS}/Filtered")


def filter_title_akas(raw_data_path: str) -> dict:

    import time

    # Dictionary to contain the titleId's (tconst's)
    # The dictionary will be set up as {id: ""} since the dictionary will be used for
    # constant lookup for future filtering.
    title_id_dictionary = {}

    # This will become the newly filtered file.
    filtered_file_directory = os.path.abspath(f"{filtered_directory}/{os.path.basename(raw_data_path)}")

    if not os.path.isdir(filtered_directory):
        os.mkdir(filtered_directory)

    print(f"Filtering {raw_data_path} to {filtered_file_directory}")
    start = time.time()

    # Read the original input.
    with open(raw_data_path, mode='r', encoding='utf-8') as raw_data:
        raw_tsv_file = csv.reader(raw_data, delimiter='\t')

        # Write filtered data.
        with open(filtered_file_directory, mode='w', encoding='utf-8', newline='') as filtered_file:
            writer = csv.writer(filtered_file, delimiter='\t')

            # Write the header.
            writer.writerow(["titleId", "ordering", "title", "region", "language", "types", "attributes", "isOriginalTitle"])
            # writer.writerow(raw_tsv_file)

            next(raw_tsv_file)  # skip the header

            for line in raw_tsv_file:
                title_id = line[0]
                region = line[3]
                if region == 'US' and title_id not in title_id_dictionary:
                    # print(line)
                    writer.writerow(line)
                    title_id_dictionary[line[0]] = None

    total = time.time() - start
    print(f"Process completed in {total} seconds")

    return title_id_dictionary


def filter_files() -> None:
    tsv_files = get_list_of_files(DATASETS, file_type=".tsv")

    dict_of_ids = {}
    for file in tsv_files:
        if 'title.akas.tsv' in file:
            dict_of_ids = filter_title_akas(file)

    print(len(dict_of_ids))