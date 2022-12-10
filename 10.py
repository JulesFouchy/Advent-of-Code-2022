from pipe import *
from utils import *
import operator


def convert_to_add_instructions(line: str):
    match line.split(" "):
        case ["noop"]:
            return [+0]
        case ["addx", value]:
            return [+0, +int(value)]


def main(filepath: str):
    # List of values during each cycle
    out = (
        enumerate(
            # Add one initial noop to emulate the initial state
            itertools.chain(["noop"], lines(filepath))
            | map(convert_to_add_instructions)
            | traverse
            | accumulate(operator.add)
            | map(lambda x: x+1)  # The register is initially set to one
        )
        | groups_of(40)
    )
    for line in out:
        for p, s in line:
            print("❄️" if abs(p % 40-s) <= 1 else " ", end="")
        print()


main(f"{day_number(__file__)}.input")
