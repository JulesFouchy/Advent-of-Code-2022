from utils import *
from pipe import *
from dataclasses import dataclass
from typing import List, Tuple
from collections import defaultdict
import os
import time


@dataclass(frozen=True, eq=True)
class Pos:
    x: int
    y: int


Path = List[Pos]


def main(filepath: str):

    paths = list(
        lines(filepath)
        | map(parse_path)
    )

    left, right = find_x_bounds(paths)
    height = find_max_y(paths)+1

    terrain = defaultdict(lambda: ".")

    # Put rocks
    for path in paths:
        for i in range(len(path)-1):
            p1 = path[i]
            p2 = path[i+1]
            x1 = min(p1.x, p2.x)
            x2 = max(p1.x, p2.x)
            y1 = min(p1.y, p2.y)
            y2 = max(p1.y, p2.y)
            for x, y in itertools.product(range(x1, x2+1), range(y1, y2+1)):
                terrain[Pos(x-left, y)] = "#"

    def at(pos: Pos) -> str:
        return terrain[pos]

    def write_at(pos: Pos, char: str) -> None:
        terrain[pos] = char

    def next_pos(sand_pos: Pos) -> Pos:
        if sand_pos.y == height:  # Simulate an infinite floor
            return sand_pos

        candidate_pos = Pos(x=sand_pos.x, y=sand_pos.y+1)
        if at(candidate_pos) == ".":
            return candidate_pos

        candidate_pos = Pos(x=sand_pos.x-1, y=sand_pos.y+1)
        if at(candidate_pos) == ".":
            return candidate_pos

        candidate_pos = Pos(x=sand_pos.x+1, y=sand_pos.y+1)
        if at(candidate_pos) == ".":
            return candidate_pos

        return sand_pos

    # Simulate sand
    units = 0
    while True:
        sand_pos = Pos(x=500-left, y=0)
        next_p = next_pos(sand_pos)
        while sand_pos != next_p:
            sand_pos = next_p
            next_p = next_pos(sand_pos)
        write_at(sand_pos, "o")
        units += 1

        if sand_pos == Pos(500-left, 0):
            break
    print(units)


def parse_pos(s: str):
    coords = s.split(",")
    return Pos(x=int(coords[0]), y=int(coords[1]))


def parse_path(line: str) -> Path:
    return list(
        line.split(" -> ")
        | map(parse_pos)
    )


def find_x_bounds(paths: List[Path]) -> Tuple[int, int]:
    x_coords = list(paths | traverse | map(lambda pos: pos.x))
    return min(x_coords), max(x_coords)


def find_max_y(paths: List[Path]) -> int:
    y_coords = list(paths | traverse | map(lambda pos: pos.y))
    return max(y_coords)


main(f"{day_number(__file__)}.input")
