from utils import *
from pipe import *
from dataclasses import dataclass
from typing import List, Tuple
import os
import time


@dataclass
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
    width = right-left+1
    height = find_max_y(paths)+1

    terrain = [["."] * width for _ in range(height)]

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
                terrain[y][x-left] = "#"

    def at(pos: Pos) -> str:
        return terrain[pos.y][pos.x]

    def write_at(pos: Pos, char: str) -> None:
        terrain[pos.y][pos.x] = char

    def next_pos(sand_pos: Pos) -> Pos:
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
    try:
        while True:
            sand_pos = Pos(x=500-left, y=0)
            next_p = next_pos(sand_pos)
            while sand_pos != next_p:
                # write_at(sand_pos, "o")
                # render(terrain)
                # write_at(sand_pos, ".")
                # time.sleep(0.1)

                sand_pos = next_p
                next_p = next_pos(sand_pos)
            write_at(sand_pos, "o")
            units += 1
    except(IndexError):
        pass
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


def render(terrain):
    os.system("cls")
    for line in terrain:
        for char in line:
            print(char, end="")
        print()


main(f"{day_number(__file__)}.input")
