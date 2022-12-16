from utils import *
from pipe import *
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Valve:
    flow_rate: int
    connections: List[str]
    opened: bool = False


@dataclass
class State:
    current: str
    timer: int
    is_open: Dict[str, bool]
    accumulated_pressure: int


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

    def try_strategy()
    current = 'AA'
    timer = 30
    while


main(f"{day_number(__file__)}.test")
