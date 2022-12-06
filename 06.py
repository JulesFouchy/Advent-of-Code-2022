from pipe import *
from utils import *
from dataclasses import dataclass
from typing import List
from functools import partial


def marker_found(tuple: List[str]):
    return len(tuple) == len(set(tuple))


def main(filepath: str):
    SLICE_SIZE = 4
    output(
        (
            characters(filepath)
            | sliding_tuple(SLICE_SIZE)
            | apply(partial(index_of_first, predicate=marker_found))
        )
        + SLICE_SIZE  # We need to add that because the prompt wants the index of the last character in the slice, not the first
    )


main(f"{day_number(__file__)}.input")
