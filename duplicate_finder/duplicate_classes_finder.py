from pathlib import Path
from collections import defaultdict

from config import MAPPING_FOLDER, DEBUG


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
    if duplicates:
        raise DuplicateMappings(len(duplicates), duplicates)


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
        return f'{self.message}\n\n{self.get_formatted_duplicates()}'

    def get_formatted_duplicates(self):
        """
        A function that formats the duplicates that have been found in a nice human readable output.
        :return: a string containing the duplicates to output as a message
        """
        duplicates_string = ''
        for key in self.duplicates:
            duplicates_string += f'Duplicates ({len(self.duplicates[key])}) found of {key} mapped as:\n'
            for mapping in self.duplicates[key]:
                duplicates_string += f'\t{mapping[0]} in file {mapping[1]}\n'
        return duplicates_string


if __name__ == '__main__':
    main()
