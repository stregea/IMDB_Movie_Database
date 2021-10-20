"""
Data analysis basic functions that will be called by analysis_specific.
"""
import os
import csv
import pandas as pd
from utils.globals import COMBINED, genres, runtimeMinutes, region, nconst, primaryProfession
from utils.helpers import convert_number_to_percentage, print_dict


def get_attributes_column_from_data(column_index: int, column_name: str) -> pd.DataFrame:
    """
    Get the given column as a 1d list in a pandas DataFrame
    :param column_index: the numerical index of the column we are looking for
    :param column_name: the name of the column we are looking for
    :return: A pandas DataFrame of the column specified from the dataset.
    """
    final_output_file = os.path.abspath(os.path.join(COMBINED, "final.output.tsv"))

    with open(final_output_file, mode='r', encoding='utf-8') as file:
        output_file = csv.reader(file, delimiter='\t')

        # Skip the header file
        next(output_file)

        attributes_list = list()

        for row in output_file:
            if row[column_index] == '\\N':
                attributes_list.append("No value")
            else:
                attributes_list.append(row[column_index])

        return pd.DataFrame(data=attributes_list, columns=[column_name])


def get_genre_information() -> pd.DataFrame:
    """
    Genre analysis script.
    Will be called by more specific functions.
    :return: A pandas DataFrame containing information for the 'genres' attribute.
    """
    return get_attributes_column_from_data(column_index=genres, column_name='genres')


def get_run_time_mins_information() -> pd.DataFrame:
    """
    Will be called by more specific functions.
    :return: A pandas DataFrame containing information for the 'runtimeMinutes' attribute.
    """
    return get_attributes_column_from_data(column_index=runtimeMinutes, column_name='runtimeMinutes')


def get_region_information():
    """
    Will be called by more specific functions
    :return: A pandas DataFrame containing information for the 'region' attribute.
    """
    return get_attributes_column_from_data(column_index=region, column_name='region')


def primary_profession_total() -> dict:
    """
    What % of the total data is each primary profession?
    - Must not double count the same nconst as multiple people.
      Number of unique nconsts is the total data to compare against.
    :return: A dictionary containing information of the total percentage of each profession.
             The form the dictionary will be in is: { profession : percentage of total data }.
    """

    final_output_file = os.path.abspath(os.path.join(COMBINED, "final.output.tsv"))

    # Dictionary to contain the return values. Will be in the form { profession : percentage of total data }.
    dictionary_of_professions = dict()

    # Set to be used to determine the total size of the nconst attributes.
    nconst_set = set()

    with open(final_output_file, mode='r', encoding='utf-8') as file:
        output_file = csv.reader(file, delimiter='\t')

        # Skip the header file
        next(output_file)

        # iterate through the file
        for record in output_file:

            # grab the nconst and primaryProfession values.
            nconst_value = record[nconst]
            profession = record[primaryProfession]

            # skip this individual if they have a null nconst attribute.
            if nconst_value == '\\N':
                continue

            # add the nconst into the set if it doesn't already exist.
            if nconst_value not in nconst_set:
                nconst_set.add(nconst_value)

            # count the total number of occurrences, don't include the null values.
            if profession not in dictionary_of_professions and profession != '\\N':
                dictionary_of_professions[profession] = 0

            # Increment the total count for the current profession if not null.
            if profession != '\\N':
                dictionary_of_professions[profession] += 1

    # change the total number of occurrences to percentages.
    total_number_of_people = len(nconst_set)
    for profession in dictionary_of_professions:
        dictionary_of_professions[profession] = convert_number_to_percentage(
            dictionary_of_professions[profession] / total_number_of_people
        )

    return dictionary_of_professions


def get_primary_professions_information() -> dict:
    """
    Read through the data set and create a dictionary of each individual and their total number of professions.
    :return: A dictionary containing all of the individuals and their total counted professions.
             The form the dictionary will be in is: { nconst : professionCount }.
    """
    final_output_file = os.path.abspath(os.path.join(COMBINED, "final.output.tsv"))

    nconst_dictionary = dict()

    with open(final_output_file, mode='r', encoding='utf-8') as file:
        output_file = csv.reader(file, delimiter='\t')

        # Skip the header file
        next(output_file)

        # iterate through the file
        for record in output_file:

            # grab the nconst and primaryProfession values.
            nconst_value = record[nconst]
            profession = record[primaryProfession]

            # skip this individual if they have a null nconst attribute.
            if nconst_value == '\\N':
                continue

            # add the nconst into the dictionary if it doesn't already exist and create a sub dictionary.
            if nconst_value not in nconst_dictionary:
                nconst_dictionary[nconst_value] = 0

            # Increment the number professions for this actor if not a null value.
            if profession != '\\N':
                nconst_dictionary[nconst_value] += 1

    return nconst_dictionary


def primary_profession_amount(number_of_professions: int) -> float:
    """
    What % of people (nconst) have one primary profession? 2? 3 or more?
    Calculates this.
    Visualization method to be determined.
    :param number_of_professions: The specified number of professions we are looking for a person to have.
    :return: The percentage of individuals who have the specified number of professions.
    """
    nconst_dictionary = get_primary_professions_information()
    total_number_of_people = len(nconst_dictionary)
    count = 0

    for nconst_value in nconst_dictionary:
        profession_count_for_current_individual = nconst_dictionary[nconst_value]
        if profession_count_for_current_individual == number_of_professions:
            count += 1

    return convert_number_to_percentage(count / total_number_of_people)
