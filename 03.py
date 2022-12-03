from pipe import *
from utils import *
from dataclasses import dataclass
from typing import List


def str_to_set(s: str):
    return {c for c in s}


def intersect(x: set, y: set):
    return x.intersection(y)


def find_common_letter(strings: List[str]):
    return (
        (
            strings
            | map(str_to_set)
            | reduce(intersect)
        )
        .pop()
    )


def priority(letter: str):
    if letter.isupper():
        return ord(letter) - ord('A') + 27
    else:
        return ord(letter) - ord('a') + 1


def main(filepath: str):
    output(
        lines(filepath)
        | groups_of(3)
        | map(find_common_letter)
        | map(priority)
        | apply(sum)
    )


main(f"{day_number(__file__)}.input")
