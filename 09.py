from pipe import *
from utils import *
import math
from itertools import product, zip_longest
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Position:
    x: int
    y: int


def to_deltas(line: str):
    direction, amount = line.split(" ")
    delta = {
        "R": np.array([1, 0]),
        "L": np.array([-1, 0]),
        "U": np.array([0, 1]),
        "D": np.array([0, -1]),
    }[direction]

    return [delta] * int(amount)


def main(filepath: str):
    # Head is the last in the list
    knots_pos = [np.array([0, 0]) for _ in range(10)]
    visited_positions = set()

    def adjust_pos(index: int):
        nonlocal knots_pos

        delta = knots_pos[index+1] - knots_pos[index]

        if np.linalg.norm(delta) >= 2:  # Too far away
            # We want to go in the same quadrant / straight line as delta, but only have components equal to 0, +1 or -1 because we can only do 1 step.
            knots_pos[index] += np.sign(delta)

    def move_head(delta: np.ndarray):
        nonlocal knots_pos

        knots_pos[-1] += delta
        for i in range(len(knots_pos) - 1) | reverse:
            adjust_pos(i)
        visited_positions.add(Position(x=knots_pos[0][0], y=knots_pos[0][1]))

    ignore = (
        lines(filepath)
        | map(to_deltas)
        | chain
        | foreach(move_head)
    )

    print(len(visited_positions))


main(f"{day_number(__file__)}.input")
