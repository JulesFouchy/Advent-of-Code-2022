from pipe import *
from utils import *
from dataclasses import dataclass
from typing import List, Protocol
import operator
import math


def elevation(char: str) -> int:
    if char == "E":
        return ord("z")
    if char == "S":
        return ord("a")
    return ord(char)


def main(filepath: str):
    height_map = list(
        lines(filepath)
    )

    width = len(height_map)
    height = len(height_map[0])

    def find_pos(target: str) -> tuple[int, int]:
        for x, y in itertools.product(range(width), range(height)):
            if height_map[x][y] == target:
                return (x, y)
        raise Exception("Target pos not found")

    starting_pos = find_pos("S")
    target_pos = find_pos("E")

    shortest_path = math.inf

    def visit(pos: tuple[int, int], steps_count: int, visited: set):
        nonlocal shortest_path
        visited.add(pos)

        if steps_count >= shortest_path:
            return

        current_cell = height_map[pos[0]][pos[1]]
        if current_cell == "E":
            shortest_path = min(shortest_path, steps_count)
            return
        current_elevation = elevation(current_cell)

        def distance_to_target(delta: tuple[int, int]) -> int:
            x = pos[0] + delta[0] - target_pos[0]
            y = pos[1] + delta[1] - target_pos[1]
            return x * x + y * y

        deltas = sorted(
            [(0, 1), (0, -1), (1, 0), (-1, 0)],
            key=distance_to_target
        )

        for delta_x, delta_y in deltas:
            x = pos[0] + delta_x
            y = pos[1] + delta_y

            if x < 0 or x >= width or y < 0 or y >= height:
                continue

            next_pos = (x, y)
            next_elevation = elevation(height_map[next_pos[0]][next_pos[1]])
            if next_elevation > current_elevation + 1:
                continue

            if next_pos in visited:
                continue

            # We make a copy of the set because immutability is important
            visit(next_pos, steps_count + 1, set(visited))

    visit(starting_pos, 0, set())
    output(shortest_path)


main(f"{day_number(__file__)}.input")
