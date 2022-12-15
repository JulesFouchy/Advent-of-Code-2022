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


@dataclass
class Diamond:
    center: Pos
    dist: int


@dataclass
class Segment:
    start: int
    stop: int


@dataclass
class SegmentList:
    segments: List[Segment]
    row: int


def is_empty(segment: Segment) -> bool:
    return segment.start > segment.stop


def subtract(diamond: Diamond, segments: SegmentList) -> None:
    remaining_dist = diamond.dist - abs(diamond.center.y - segments.row)
    if remaining_dist < 0:
        return
    new_segs = []
    for seg in segments.segments:
        sub = subtract_segments(
            seg,
            Segment(
                start=diamond.center.x - remaining_dist,
                stop=diamond.center.x + remaining_dist,
            ),
        )
        new_segs.extend(sub)
    segments.segments = list(new_segs | where(lambda s: not is_empty(s)))


def subtract_segments(seg1: Segment, seg2: Segment) -> List[Segment]:
    return [
        Segment(seg1.start, min(seg2.start-1, seg1.stop)),
        Segment(max(seg2.stop+1, seg1.start), seg1.stop),
    ]


def main(filepath: str):
    sensors: List[Sensor] = list(
        lines(filepath)
        | map(parse_sensor)
    )

    for row in range(4000000 + 1):
        if row % 10000 == 0:
            print(row / 4000000)
        subtraction = SegmentList([Segment(0, 4000000)], row)
        for sensor in sensors:
            subtract(
                Diamond(
                    center=sensor.pos,
                    dist=manhattan_distance(
                        sensor.pos, sensor.closest_beacon_pos),
                ),
                subtraction,
            )
        if len(subtraction.segments) > 0:
            print(4000000 * subtraction.segments[0].start + row)
            break


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


main(
    f"{day_number(__file__)}.input"
)
