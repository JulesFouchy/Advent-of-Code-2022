from pipe import *
from utils import *
import math
from itertools import product, zip_longest


def main(filepath: str):
    height_map = []

    def collect_heights_of_tree_line(line: str):
        heights = line | map(int)
        height_map.append(list(heights))

    unused = (
        lines(filepath)
        | foreach(collect_heights_of_tree_line)
    )

    scenic_scores = [[1 for column in row] for row in height_map]

    def x_count():
        return len(height_map)

    def y_count():
        return len(height_map[0])

    for main_x, main_y in product(range(x_count()), range(y_count())):
        main_height = height_map[main_x][main_y]

        def explore(x_y_ranges):
            trees_seen = 0
            for x, y in x_y_ranges:
                trees_seen += 1
                if height_map[x][y] >= main_height:
                    break
            scenic_scores[main_x][main_y] *= trees_seen

        explore(zip_longest(range(main_x + 1, x_count()), [], fillvalue=main_y))
        explore(zip_longest(range(main_x) | reverse, [], fillvalue=main_y))
        explore(zip_longest([], range(main_y + 1, y_count()), fillvalue=main_x))
        explore(zip_longest([], range(main_y) | reverse, fillvalue=main_x))

    output(
        scenic_scores
        | traverse
        | apply(max)
    )


main(f"{day_number(__file__)}.input")
