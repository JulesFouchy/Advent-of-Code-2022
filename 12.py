import math
from utils import lines, day_number, output
import itertools


def elevation(char: str) -> int:
    if char == "E":
        return ord("z")
    if char == "S":
        return ord("a")
    return ord(char)


def main(filepath: str):
    height_map = list(lines(filepath))

    width = len(height_map)
    height = len(height_map[0])

    def find_pos(target: str) -> tuple[int, int]:
        for x, y in itertools.product(range(width), range(height)):
            if height_map[x][y] == target:
                return (x, y)
        raise Exception("Target pos not found")

    def shortest_path_starting_at(starting_pos:  tuple[int, int]):
        positions = {starting_pos}
        length = 0
        while 0 == len([p for p in positions if height_map[p[0]][p[1]] == "E"]):
            if len(positions) == 0:
                raise Exception("Cul de sac!")
            length += 1
            new_positions = set()
            for pos in positions:
                current_elevation = elevation(height_map[pos[0]][pos[1]])
                for delta_x, delta_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    x = pos[0] + delta_x
                    y = pos[1] + delta_y

                    if x < 0 or x >= width or y < 0 or y >= height:
                        continue

                    next_pos = (x, y)
                    next_elevation = elevation(
                        height_map[next_pos[0]][next_pos[1]])

                    # No need to look at paths that contain an "a" because we can always find a shorter path (the one that starts at the "a" that we just saw)
                    if next_elevation == ord("a"):
                        continue

                    if next_elevation > current_elevation + 1:
                        continue

                    new_positions.add(next_pos)

            positions = new_positions
        return length

    min_length = math.inf
    for x, y in itertools.product(range(width), range(height)):
        if elevation(height_map[x][y]) != ord('a'):
            continue
        print("---------------------------------------------------------", x, y)
        try:
            min_length = min(min_length, shortest_path_starting_at((x, y)))
        except:
            pass

    print(min_length)


main(f"{day_number(__file__)}.input")
