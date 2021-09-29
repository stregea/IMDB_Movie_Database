import os
import csv
import time
from sqlite3 import IntegrityError
from interface.dbconn import DB
from utils.globals import DATASETS, DATABASE, COMBINED
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
    value = values[index]
    return -1 if values[index] == '\\N' else int(float(values[index]))


def _get_float_value(values: list, index: int) -> float:
    """
    Return the integer value from a list.
    :param values: The list containing the values.
    :param index: The index of the list to access.
    :return: -1 if the null character is read. Otherwise return the string value.
    """
    return -1 if values[index] == '\\N' else float(values[index])


def _insert_title_basics_data(db: DB) -> None:
    """
    TODO: This is still in development. Come back to this once data filtering is complete.
    Insert the title.basics.tsv data into the database.
    :param db: The connection to the database.
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
                log(f"inserted id {tconst}", level="debug")

            except IntegrityError as e:
                log(str(e), level="warning")

    execution_time = time.time()
    print(f"Insertion completed in {execution_time - start_time} seconds.")


def _insert_imdb_data(db: DB):
    first_file_to_insert = os.path.abspath(f"{COMBINED}/final.output.tsv")

    # tsv_files.remove(first_file_to_insert)
    start_time = time.time()
    print(f"Beginning insertion for {first_file_to_insert}")
    with open(first_file_to_insert, encoding='utf-8') as file:
        tsv_file = csv.reader(file, delimiter='\t')
        next(tsv_file)  # skip the header

        for line in tsv_file:
            # print(line)

            query = '''INSERT INTO IMDB(tconst,ordering,title, region,language,types,attributes,isOriginalTitle,
                                        averageRating,numVotes,titleType,primaryTitle,originalTitle,isAdult,startYear,
                                        endYear,runtimeMinutes,genre,nconst,primaryName,birthYear,deathYear,primaryProfession)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
            '''

            tconst = _get_string_value(line, index=0)
            ordering = _get_int_value(line, index=1)
            title = _get_string_value(line, index=2)
            region = _get_string_value(line, index=3)
            language = _get_string_value(line, index=4)
            types = _get_string_value(line, index=5)
            attributes = _get_string_value(line, index=6)
            isOriginalTitle = _get_int_value(line, index=7)
            averageRating = _get_float_value(line, index=8)
            numVotes = _get_int_value(line, index=9)
            titleType = _get_string_value(line, index=10)
            primaryTitle = _get_string_value(line, index=11)
            originalTitle = _get_string_value(line, index=12)
            isAdult = _get_int_value(line, index=13)
            startYear = _get_int_value(line, index=14)
            endYear = _get_int_value(line, index=15)
            runtimeMinutes = _get_int_value(line, index=16)
            genre = _get_string_value(line, index=17)
            nconst = _get_string_value(line, index=18)
            primaryName = _get_string_value(line, 19)
            birthYear = _get_int_value(line, index=20)
            deathYear = _get_int_value(line, index=21)
            primaryProfession = _get_string_value(line, index=22)

            values_to_insert = (
                tconst, ordering, title, region, language, types, attributes, isOriginalTitle, averageRating,
                numVotes, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes,
                genre, nconst, primaryName, birthYear, deathYear, primaryProfession
            )
            db.commit(query, values=values_to_insert)

            log(f"inserted id {tconst}", level="debug")

    execution_time = time.time()
    print(f"Insertion completed in {(execution_time - start_time) / 60} minutes.")


def insert_data_to_db():
    db = DB(DATABASE)

    _insert_imdb_data(db)

    db.close()


if __name__ == '__main__':
    insert_data_to_db()
