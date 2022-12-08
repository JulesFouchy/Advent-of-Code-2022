from pipe import *
from utils import *
import math


def main(filepath: str):
    height_map = []

    def collect_heights_of_tree_line(line: str):
        heights = line | map(int)
        height_map.append(list(heights))

    unused = (
        lines(filepath)
        | foreach(collect_heights_of_tree_line)
    )

    visibilities = [[False for column in row] for row in height_map]

    def x_count():
        return len(height_map)

    def y_count():
        return len(height_map[0])

    def check_visibility_from(x_y_ranges):
        highest_seen = -math.inf
        for x, y in x_y_ranges:
            current_height = height_map[x][y]
            if current_height > highest_seen:
                visibilities[x][y] = True
                highest_seen = current_height

    # Check visibility in the four directions
    for y in range(y_count()):
        check_visibility_from(zip(range(x_count()), [y] * x_count()))
        check_visibility_from(zip(range(x_count()) | reverse, [y] * x_count()))
    for x in range(x_count()):
        check_visibility_from(zip([x] * y_count(), range(y_count())))
        check_visibility_from(zip([x] * y_count(), range(y_count()) | reverse))

    output(
        visibilities
        | traverse
        | map(lambda is_visible: 1 if is_visible else 0)
        | apply(sum)
    )


main(f"{day_number(__file__)}.input")
