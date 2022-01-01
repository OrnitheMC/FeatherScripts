from pathlib import Path
from collections import defaultdict
from typing_extensions import Final
from typing import List


"""---- Config ----"""
MAPPING_FOLDER: Final[Path] = Path("mappings")  # the path to the mappings folder
DEBUG: Final[bool] = True


def main():
    """
    Main function checking for duplicates inside the mappings folder. If duplicates
    are found an error is raised and the duplicates are printed.
    """
    mappings = defaultdict(list)
    for f in MAPPING_FOLDER.glob('**/*'):
        if f.is_file():
            add_to_dict(f, mappings)

    duplicates = find_duplicates(mappings)

    if duplicates and not DEBUG:
        raise DuplicateMappings(len(duplicates), duplicates)

    elif duplicates and DEBUG:
        print("Duplicates found:")
        print(get_formatted_duplicates(duplicates))
        input_ = input("Input a class of which you want to see the duplicated methods and fields mappings!\n"
                       "If you don't want to analyze any method, input something that is not a duplicate class!\n")

        while input_ in duplicates:
            find_duplicate_methods([Path(i[1]) for i in duplicates[input_]])
            input_ = input("Input another class to analyze\n")
    else:
        print("No duplicate class mappings found")


def add_to_dict(file: Path, mapping_dict: defaultdict):
    """
    This method reads a file and checks the mapped class. It will add the file to the
    directory containing all of the mappings. The key is the class name in the intermediaries.
    The value is a list of all the different names this class is mapped under. Each element
    in this list is a list it self containing the mapped name of the entry and the file path.
    """
    with open(file) as f:
        class_mapping = f.readline().strip('\n').split(' ')[1:]

    class_ = class_mapping[0]
    mapping = class_mapping[1] if len(class_mapping) == 2 else class_
    mapping_dict[class_].append([mapping, file])


def find_duplicates(mapping_dict: defaultdict) -> dict:
    """
    Filter the dict to find the entries with more than 1 name
    """
    return dict(filter(lambda elem: len(elem[1]) > 1, mapping_dict.items()))


class DuplicateMappings(Exception):
    """
    Exception raised when duplicate mappings are found.

    Attributes:
        the amount of classes that have duplicates
        the dictionary containing the duplicates
        the Exception message (set by default but is able to be overridden)
    """

    def __init__(self, n, duplicates, message="Duplicate mappings found for {} classes"):
        self.n = n
        self.duplicates = duplicates
        self.message = message.format(self.n)
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}\n\n{get_formatted_duplicates(self.duplicates)}'


def get_formatted_duplicates(duplicates: dict) -> str:
    """
    A function that formats the duplicates that have been found in a nice human readable output.
    :return: a string containing the duplicates to output as a message
    """
    duplicates_string = ''
    for key in duplicates:
        duplicates_string += f'Duplicates ({len(duplicates[key])}) found of {key} mapped as:\n'
        for mapping in duplicates[key]:
            duplicates_string += f'\t{mapping[0]} in file {mapping[1]}\n'
    return duplicates_string


def read_mapping_file(file: Path, field_mappings: defaultdict, method_mappings: defaultdict):
    """
    Read a mapping file and put it's mapped methods and fields into their
    corresponding dictionary to later analyze for duplicates!
    """
    with open(file) as f:
        data = [line.strip('\t').strip('\n').split() for line in f.readlines()]

    for d in data[1:]:
        if d[0] == 'FIELD':
            field_mappings[d[1]].append([d[2], file])
        elif d[0] == 'METHOD':
            method_mappings[d[1]].append([d[2], file])


def find_duplicate_methods(files: List[Path]) -> bool:
    """
    Find duplicate methods and fields between the classes that are in the list of paths
    """
    field_mappings = defaultdict(list)
    method_mappings = defaultdict(list)

    for i in files:
        read_mapping_file(i, field_mappings, method_mappings)

    print("----- DUPLICATE FIELDS -----")
    print(get_formatted_duplicates(field_mappings))
    print("----- DUPLICATE METHODS -----")
    print(get_formatted_duplicates(method_mappings))
    return True


if __name__ == '__main__':
    main()
