def print_dict(dictionary: dict) -> None:
    """
    Print out a dictionary that is the the form { key : value }.
    To be used if we want to print out the dictionary and its contents.
    :param dictionary: The dictionary to print.
    """
    print('{')
    for i, key in enumerate(dictionary):
        char = ',' if i < len(dictionary)-1 else ''
        print(f"\t{key}: {dictionary[key]}{char}")
    print('}')


def convert_number_to_percentage(number: float) -> float:
    """
    Convert a floating-point value into it's percentage value.
    To be used if we want to print out the percentages.
    :param number: The number to convert.
    :return: The percentage-based equivalent of the number passed into the function.
    """
    return round(number * 10, 2)
