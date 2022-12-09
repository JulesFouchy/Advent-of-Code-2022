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
    head_pos = np.array([0, 0])
    tail_pos = np.array([0, 0])
    visited_positions = set()

    def adjust_tail_pos():
        nonlocal tail_pos

        delta = head_pos - tail_pos
        norm = np.linalg.norm(delta)

        if norm == 1:
            # 1 cell off in straight direction
            return

        elif norm == 2:
            # 2 cells off in straight direction
            tail_pos += delta // 2

        elif norm > 2:
            # Too far away in diagonal direction
            # One coordinate of delta is ±1, and the other is ±2. We want both of these coordinate to be ±1 so that we move in a diagonal.
            tail_pos += np.array([c // abs(c) for c in delta])

    def move_head(delta: np.ndarray):
        nonlocal head_pos, tail_pos

        head_pos += delta
        adjust_tail_pos()
        visited_positions.add(Position(x=tail_pos[0], y=tail_pos[1]))

    ignore = (
        lines(filepath)
        | map(to_deltas)
        | chain
        | foreach(move_head)
    )

    print(len(visited_positions))


main(f"{day_number(__file__)}.input")
