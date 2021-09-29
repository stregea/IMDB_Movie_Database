import os
import csv
from utils.globals import COMBINED


def print_dictionary(d: dict) -> None:
    """
    Print out the contents of a dictionary.
    :param d: The dictionary to print.
    """
    print("{")
    for key in d:
        print(f"\t{key}: ")
        for more_keys in d[key]:
            print("\t\t{")
            print(f"\t\t\t{more_keys}: {d[key][more_keys]}")
            print("\t\t}")
    print("}")


def create_inner_dictionary() -> dict:
    """
    Create a dictionary that is to be placed within the Data Dictionary.
    :return: An empty dictionary.
    """
    return {
        'Number of Unique Entries': None,
        'Total Number of Entries': None,
        'Type': None,
        'Characteristics': None,
        'Bottom Range': None,
        'Upper Range': None
    }


def determine_data_types_and_characteristics() -> list[tuple]:
    """
    Retrieve a list of tuples containing information about an attribute's
    data type and characteristic.
    :return: A list of tuples containing information about an attribute's data type and characteristics.
    """
    return [
        ('tconst', 'string', 'nominal'),
        ('ordering', 'integer', 'nominal'),
        ('title', 'string', 'nominal'),
        ('region', 'string', 'nominal'),
        ('types', 'string', 'nominal'),
        ('attributes', 'string', 'nominal'),
        ('isOriginalTitle', 'boolean', 'nominal'),
        ('averageRating', 'float', 'ordinal'),
        ('numVotes', 'float', 'ratio'),
        ('titleType', 'string', 'nominal'),
        ('primaryTitle', 'string', 'nominal'),
        ('originalTitle', 'string', 'nominal'),
        ('isAdult', 'boolean', 'nominal'),
        ('startYear', 'integer', 'interval'),
        ('endYear', 'integer', 'interval'),
        ('runtimeMinutes', 'integer', 'ratio'),
        ('genres', 'string', 'nominal'),
        ('nconst', 'string', 'nominal'),
        ('primaryName', 'string', 'nominal'),
        ('birthYear', 'integer', 'interval'),
        ('deathYear', 'integer', 'interval'),
        ('primaryProfession', 'string', 'nominal'),
    ]


def determine_range_of_values(data_dictionary: dict) -> None:
    """
    Determine the range of values for attributes that aren't nominal in nature.
    :param data_dictionary: The data dictionary to store the values in.
    """
    final_output_file = os.path.abspath(os.path.join(COMBINED, "final.output.tsv"))

    # Start at column0
    attribute_column = 0

    # Iterate through all of the attributes
    for attribute_key in data_dictionary:

        # Only determine the range if the characteristic is not 'nominal'
        if data_dictionary[attribute_key]['Characteristics'].lower() != 'nominal':
            bottom_range = str(float('inf'))
            upper_range = str(float('-inf'))

            with open(final_output_file, mode='r', encoding='utf-8') as file:
                output_file = csv.reader(file, delimiter='\t')

                # Skip the header file
                next(output_file)

                # Iterate through all rows to determine the bottom and upper ranges.
                for row in output_file:
                    if row[attribute_column] != '\\N':
                        if row[attribute_column] < bottom_range:
                            bottom_range = row[attribute_column]
                        if row[attribute_column] > upper_range:
                            upper_range = row[attribute_column]

            # Set the bottom and upper ranges
            data_dictionary[attribute_key]['Bottom Range'] = bottom_range
            data_dictionary[attribute_key]['Upper Range'] = upper_range

        # Shift the column right by 1
        attribute_column += 1


def create_data_dictionary():
    print("Creating Data Dictionary...")
    data_dictionary = {}
    data_and_value_types = determine_data_types_and_characteristics()

    print("\tPopulating attributes, their data types and their characteristics...")
    # populate the dictionary with attribute names as the id, and populate the Type and Characteristics fields.
    for tup in data_and_value_types:
        attribute_name = tup[0]
        data_dictionary[attribute_name] = create_inner_dictionary()
        data_dictionary[attribute_name]['Type'] = tup[1]
        data_dictionary[attribute_name]['Characteristics'] = tup[2]

    print("\tPopulating the range of values for non-nominal attributes...")
    determine_range_of_values(data_dictionary)

    print("Data Dictionary")
    print_dictionary(data_dictionary)


if __name__ == '__main__':
    create_data_dictionary()
