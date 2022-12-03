from pipe import *
from utils import *
from dataclasses import dataclass


@dataclass
class Compartments:
    first: str
    second: str


def split_into_compartments(line: str):
    return Compartments(
        line[: len(line) // 2],
        line[len(line) // 2:],
    )


def str_to_set(s: str):
    return {c for c in s}


def find_common_letter(compartments: Compartments):
    set1 = str_to_set(compartments.first)
    set2 = str_to_set(compartments.second)
    return set1.intersection(set2).pop()


def priority(letter: str):
    if letter.isupper():
        return ord(letter) - ord('A') + 27
    else:
        return ord(letter) - ord('a') + 1


def main(filepath: str):
    print(
        lines(filepath)
        | map(split_into_compartments)
        | map(find_common_letter)
        | map(priority)
        | reduce(sum)
    )


main(f"{day_number(__file__)}.input")
