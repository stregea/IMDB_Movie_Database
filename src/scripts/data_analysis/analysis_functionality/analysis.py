"""
Data analysis basic functions that will be called by analysis_specific.
"""

import os
import csv
import pandas as pd
from utils.globals import COMBINED


def get_genre_information() -> None:
    """
    Genre analysis script.
    Will be called by more specific functions.
    """
    return


def get_run_time_mins_information():
    """
    Will be called by more specific functions.
    """
    return

def get_region_information():
    """
    Will be called by more specific functions
    """
    return

def primary_profession_total():
    """
    What % of the total data is each primary profession?
    - Must not double count the same nconst as multiple people.
      Number of unique nconsts is the total data to compare against.
    """
    return

def primary_profession_amount():
    """
    What % of people (nconst) have one primary profession? 2? 3 or more?
    Calculates this.
    Visualization method to be determined.
    """
    return

def get_attributes_column_from_data(column_index, column_name):
    """
    Get the given column as a 1d list in a pandas DataFrame
    :param column_index: the numerical index of the column we are looking for
    :param column_name: the name of the column we are looking for
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
