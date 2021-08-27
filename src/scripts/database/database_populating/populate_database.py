import os
import csv
import time
from sqlite3 import IntegrityError
from interface.dbconn import DB
from utils.globals import DATASETS, DATABASE
from utils.walkers.directory_walker import get_list_of_files
from utils.logger.logger import log


def _get_string_value(values: list, index: int) -> str:
    """
    Return the string value from a list.
    :param values: The list containing the values.
    :param index: The index of the list to access.
    :return: None if the null character is read. Otherwise return the string value.
    """
    return None if values[index] == '\\N' else str(values[index])


def _get_int_value(values: list, index: int) -> int:
    """
    Return the integer value from a list.
    :param values: The list containing the values.
    :param index: The index of the list to access.
    :return: -1 if the null character is read. Otherwise return the string value.
    """
    return -1 if values[index] == '\\N' else int(values[index])


def _insert_title_basics_data(db: DB) -> None:
    """
    TODO: This is still in development.
    Insert the title.basics.tsv data into the database.
    :param db: The connection to the database.
    :return:
    """
    first_file_to_insert = os.path.abspath(f"{DATASETS}/title.basics.tsv")

    # tsv_files.remove(first_file_to_insert)
    start_time = time.time()
    print(f"Beginning insertion for {first_file_to_insert}")
    with open(first_file_to_insert, encoding='utf-8') as file:
        tsv_file = csv.reader(file, delimiter='\t')
        next(tsv_file)  # skip the header

        for line in tsv_file:
            # print(line)

            query = '''INSERT INTO TitleBasics
                        VALUES (?,?,?,?,?,?,?,?,?);
            '''

            tconst = _get_string_value(line, index=0)
            title_type = _get_string_value(line, index=1)
            primary_title = _get_string_value(line, index=2)
            original_title = _get_string_value(line, index=3)
            is_adult = _get_int_value(line, index=4)
            start_year = _get_int_value(line, index=5)
            end_year = _get_int_value(line, index=6)
            runtime_minutes = _get_int_value(line, index=7)
            genres = _get_string_value(line, index=8)

            # insert the line into the database.
            try:
                db.commit(query, values=(
                                    tconst,
                                    title_type,
                                    primary_title,
                                    original_title,
                                    is_adult,
                                    start_year,
                                    end_year,
                                    runtime_minutes,
                                    genres)
                          )
            except IntegrityError as e:
                log(str(e), level="warning")

    execution_time = time.time()
    print(f"Insertion completed in {execution_time-start_time} seconds.")


def run():
    db = DB(DATABASE)
    # tsv_files = get_list_of_files(directory=DATASETS, file_type=".tsv")
    # print(os.path.abspath(f"{DATASETS}/title.basics.tsv"))

    _insert_title_basics_data(db)

    db.close()


if __name__ == '__main__':
    run()
