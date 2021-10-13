import os
import csv
from utils.globals import COMBINED


def print_dictionary(d: dict) -> None:
    """
    Print out the contents of a dictionary.
    :param d: The dictionary to print.
    """
    print("{")
    for i, key in enumerate(d):
        outer_brace = '},' if i < len(d) - 1 else '}'
        print(f"\t{key}")
        print("\t{")
        for j, more_keys in enumerate(d[key]):
            char = ',' if j < len(d[key]) - 1 else ''
            print(f"\t\t{more_keys}: {d[key][more_keys]}{char}")
        print(f"\t{outer_brace}")
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
        'Bottom Range (min)': None,
        'Upper Range (max)': None,
        'Mean': None,
        'Mode': None,
        'Median': None,
        'Outliers': None
    }


def determine_number_unique_entries_and_mode(data_dictionary: dict) -> None:
    """
    Determine the total count, unique count and mode for each attribute in the output file.
    :param data_dictionary: The data dictionary to read and write to.
    """
    final_output_file = os.path.abspath(os.path.join(COMBINED, "final.output.tsv"))
    # Start at column0
    attribute_column = 0

    # Iterate through all of the attributes
    for attribute_key in data_dictionary:
        unique_entries = {}
        unique = 0
        total_entries = 0
        with open(final_output_file, mode='r', encoding='utf-8') as file:
            output_file = csv.reader(file, delimiter='\t')

            # Skip the header file
            next(output_file)

            print(f"\t\tDetermining the unique and total count for: {attribute_key}")

            # Count the number of values for an attribute
            for row in output_file:

                # Skip the null attributes.
                if row[attribute_column] == '\\N':
                    continue

                if row[attribute_column] not in unique_entries.keys():
                    unique_entries[row[attribute_column]] = 1
                else:
                    unique_entries[row[attribute_column]] += 1

                total_entries += 1

            champ_mode = 0
            champ_num_entries = 0

            for k in unique_entries:

                # Count the total number of unique entries for an attribute
                if unique_entries.get(k) == 1:
                    unique += 1
                # Calculate the mode
                if unique_entries.get(k) > champ_num_entries:
                    champ_mode = k
                    champ_num_entries = unique_entries.get(k)
            

            data_dictionary[attribute_key]['Number of Unique Entries'] = f"{unique:,}"
            data_dictionary[attribute_key]['Total Number of Entries'] = f"{total_entries:,d}"

            # Only insert mode if it's a non-numeric value
            if data_dictionary[attribute_key]['Characteristics'].lower() != 'nominal':
                data_dictionary[attribute_key]['Mode'] = champ_mode

        attribute_column += 1  # shift column for the next attribute


def determine_data_types_and_characteristics() -> list:
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
        ('language', 'string', 'nominal'),
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


def determine_mean_and_range_of_values(data_dictionary: dict) -> None:
    """
    Determine the range and mean of values for attributes that aren't nominal in nature.
    :param data_dictionary: The data dictionary to store the values in.
    """
    final_output_file = os.path.abspath(os.path.join(COMBINED, "final.output.tsv"))

    # Start at column0
    attribute_column = 0

    # Iterate through all of the attributes
    for attribute_key in data_dictionary:

        # Only determine the range and mean if the characteristic is not 'nominal'
        if data_dictionary[attribute_key]['Characteristics'].lower() != 'nominal':
            data_dictionary[attribute_key]['Bottom Range'] = str(float('inf'))
            data_dictionary[attribute_key]['Upper Range'] = str(float('-inf'))

            with open(final_output_file, mode='r', encoding='utf-8') as file:
                output_file = csv.reader(file, delimiter='\t')

                # Skip the header file
                next(output_file)

                total = 0
                size = 0
                mean = 0

                print(f"\t\tDetermining mean and range for: {attribute_key}")
                # Iterate through all rows to determine the bottom and upper ranges.
                for i, row in enumerate(output_file):

                    # Skip the null attributes.
                    if row[attribute_column] == '\\N':
                        continue

                    # Mean computations
                    size += 1
                    total += float(row[attribute_column])

                    # Range computations
                    if float(row[attribute_column]) < float(data_dictionary[attribute_key]['Bottom Range']):

                        # if new year is BC and the current bottom year is BC and the current bottom range is larger
                        # than the current one
                        if attribute_key == 'birthYear' and row[attribute_column][:2] == '00' and \
                                data_dictionary[attribute_key]['Bottom Range'][:2] == '00' and \
                                float(data_dictionary[attribute_key]['Bottom Range']) > float(row[attribute_column]):
                            pass
                        else:
                            data_dictionary[attribute_key]['Bottom Range'] = row[attribute_column]

                    if float(row[attribute_column]) > float(data_dictionary[attribute_key]['Upper Range']):
                        data_dictionary[attribute_key]['Upper Range'] = row[attribute_column]

                if size > 0:
                    mean = total / size
                data_dictionary[attribute_key]['Mean'] = mean


        # Shift the column right by 1
        attribute_column += 1


def determine_median_and_outliers(data_dictionary: dict) -> None:
    """
    Determine the median for each attribute in the output file.
    :param data_dictionary: The data dictionary to read and write to.
    """
    final_output_file = os.path.abspath(os.path.join(COMBINED, "final.output.tsv"))
    # Start at column0
    attribute_column = 0

    # Iterate through all of the numeric attributes
    for attribute_key in data_dictionary:
        if data_dictionary[attribute_key]['Characteristics'].lower() != 'nominal':

            entries_list = []

            with open(final_output_file, mode='r', encoding='utf-8') as file:
                output_file = csv.reader(file, delimiter='\t')

                # Skip the header file
                next(output_file)

                print(f"\t\tDetermining the median and outliers for: {attribute_key}")

                # Iterate through all of the rows in the file
                for row in output_file:

                    # Skip the null attributes.
                    if row[attribute_column] == '\\N':
                        continue

                    entries_list.append(float(row[attribute_column]))

                # Sort list and store list size
                entries_list.sort()
                list_size = len(entries_list)

                # Only consider median and outliers for lists with at least one element
                if list_size > 0:

                    # Calculate median
                    # median = None

                    # if list_size % 2 == 0:
                    #     median = (entries_list[list_size // 2] + entries_list[(list_size // 2) + 1]) / 2
                    # else:
                    #     median = entries_list[list_size // 2]

                    data_dictionary[attribute_key]['Median'] = find_median_of_list(entries_list)

                    # Calculate first and third quartile then interquartile range and outlier thresholds
                    first_quartile = find_median_of_list(entries_list[:list_size // 2])
                    third_quartile = None

                    if list_size % 2 == 0:
                        third_quartile = find_median_of_list(entries_list[list_size // 2:])
                    else:
                        third_quartile = find_median_of_list(entries_list[(list_size // 2) + 1:])

                    interquartile_range = third_quartile - first_quartile
                    lower_outlier_threshold = first_quartile - (interquartile_range * 3)
                    upper_outlier_threshold = third_quartile + (interquartile_range * 3)

                    # Iterate through our list and determine what outliers there are
                    outlier_list = []

                    for value in entries_list:
                        if value < lower_outlier_threshold or value > upper_outlier_threshold:
                            if value not in outlier_list:
                                outlier_list.append(value)

                    data_dictionary[attribute_key]['Outliers'] = outlier_list

        attribute_column += 1  # shift column for the next attribute

def find_median_of_list(list_of_values):
    """
    Get the median of list_of_values which is assumed to have size greater than 0
    """
    list_length = len(list_of_values)

    if list_length % 2 == 0:
        return (list_of_values[list_length // 2] + list_of_values[(list_length // 2) + 1]) / 2
    else:
        return list_of_values[list_length // 2]


def create_data_dictionary() -> None:
    """
    Create and populate a data dictionary.
    """
    print("Creating Data Dictionary...")
    data_dictionary = {}
    data_and_value_types = determine_data_types_and_characteristics()

    # populate the dictionary with attribute names as the id, and populate the Type and Characteristics fields.
    print("\tPopulating attributes, their data types and their characteristics...")
    for tup in data_and_value_types:
        attribute_name = tup[0]
        data_dictionary[attribute_name] = create_inner_dictionary()
        data_dictionary[attribute_name]['Type'] = tup[1]
        data_dictionary[attribute_name]['Characteristics'] = tup[2]

    # Determine the mean range of values for non-nominal attributes.
    # print("\tPopulating the mean and range of values for non-nominal attributes...")
    # determine_mean_and_range_of_values(data_dictionary)

    # Determine the total number and unique entry count and mode of each attribute.
    # print("\tDetermining unique and total number and mode of entries...")
    # determine_number_unique_entries_and_mode(data_dictionary)

    # Determine the median of each attribute
    print("\tDetermining the median and outliers of each attribute...")
    determine_median_and_outliers(data_dictionary)

    print("Data Dictionary")
    print_dictionary(data_dictionary)


if __name__ == '__main__':
    create_data_dictionary()
