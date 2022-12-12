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

    starting_pos = find_pos("S")

    positions = {starting_pos}
    length = 0
    while 0 == len([p for p in positions if height_map[p[0]][p[1]] == "E"]):
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

                if next_elevation > current_elevation + 1:
                    continue

                new_positions.add(next_pos)

        positions = new_positions

    output(length)


main(f"{day_number(__file__)}.input")
