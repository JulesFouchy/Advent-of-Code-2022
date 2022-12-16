from utils import *
from pipe import *
from dataclasses import dataclass
from typing import List


@dataclass
class Valve:
    flow_rate: int
    connections: List[str]


def main(filepath: str):
    valves = {}

    def parse_valve(line: str):
        import re
        vals = re.findall(
            r"Valve (.*) has flow rate=(.*)(; tunnels lead to valves |; tunnel leads to valve )(.*)", line)[0]
        valves[vals[0]] = Valve(
            flow_rate=vals[1],
            connections=vals[3].split(", ")
        )

    ignored = (
        lines(filepath)
        | foreach(parse_valve)
    )
    print(valves)


main(f"{day_number(__file__)}.test")
