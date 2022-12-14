from pipe import *
from utils import *
from dataclasses import dataclass
from typing import List


@dataclass
class Range:
    begin: int
    end: int


def split_pairs(line: str):
    return line.split(',')


def parse_range(range_as_str: str):
    as_int = range_as_str.split('-') | map(int)
    return Range(next(as_int), next(as_int))


def one_range_overlaps_the_other(range_pair: List[Range]):
    def first_element_is_inside_other(a: Range, b: Range):
        return a.begin >= b.begin and a.begin <= b.end

    return (first_element_is_inside_other(range_pair[0], range_pair[1])
            or first_element_is_inside_other(range_pair[1], range_pair[0]))


def main(filepath: str):
    output(
        lines(filepath)
        | map(split_pairs)
        | map(lambda pair: list(
              pair
              | map(parse_range)
              ))
        | where(one_range_overlaps_the_other)
        | count_elements
    )


main(f"{day_number(__file__)}.input")
