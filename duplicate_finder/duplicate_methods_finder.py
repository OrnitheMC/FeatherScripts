"""
Very unfinished atm but kinda usable
"""

from os import listdir
from typing import List
from collections import defaultdict
from os.path import isfile, join

"""---- Config ----"""
files = [
    "..\\mappings\\net\\minecraft\\entity\\ai\\goal\\OcelotSitOnBlockGoal.mapping",
    "..\\mappings\\net\\minecraft\\entity\\ai\\goal\\OcelotSitOnBlockGoal.mapping~1.7.2"
]

field_mappings = defaultdict(list)  # the dictionary to put the mappings in
method_mappings = defaultdict(list)


def read_mapping_file(file: str):
    with open(file) as f:
        data = [line.strip('\t').strip('\n').split() for line in f.readlines()]
    class_ = data[0][2] if len(data[0]) == 3 else data[0][1]

    for d in data[1:]:
        if d[0] == 'FIELD':
            field_mappings[d[1]].append([d[2], file])
        elif d[0] == 'METHOD':
            method_mappings[d[1]].append([d[2], file])


def get_formatted_duplicates(duplicates):
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


if __name__ == '__main__':
    for i in files:
        read_mapping_file(i)
    print(get_formatted_duplicates(field_mappings))
    print(get_formatted_duplicates(method_mappings))
