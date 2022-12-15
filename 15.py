from utils import *
from pipe import *
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True, eq=True)
class Pos:
    x: int
    y: int


@dataclass
class Sensor:
    pos: Pos
    closest_beacon_pos: Pos


def main(filepath: str):
    sensors: List[Sensor] = list(
        lines(filepath)
        | map(parse_sensor)
    )

    pos_where_beacon_can_not_be = set()
    for sensor in sensors:
        dist = manhattan_distance(sensor.pos, sensor.closest_beacon_pos)
        for total in range(0, dist+1):
            for x in range(total+1):
                y = total - x
                for x_sign in [-1, 1]:
                    for y_sign in [-1, 1]:
                        pos = Pos(x*x_sign+sensor.pos.x, y*y_sign+sensor.pos.y)
                        if pos == sensor.closest_beacon_pos:
                            continue
                        pos_where_beacon_can_not_be.add(pos)

    row_to_check = 2000000
    output(
        pos_where_beacon_can_not_be
        | where(lambda pos: pos.y == row_to_check)
        | count_elements
    )


def manhattan_distance(p1: Pos, p2: Pos) -> int:
    return abs(p1.x-p2.x) + abs(p1.y-p2.y)


def parse_sensor(line: str) -> Sensor:
    import re
    vals = list(
        re.findall(
            r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
        | map(int))
    return Sensor(
        pos=Pos(vals[0], vals[1]),
        closest_beacon_pos=Pos(vals[2], vals[3]),
    )


main(f"{day_number(__file__)}.input")
