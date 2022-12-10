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
    output(
        enumerate(
            # Add two initial noops to emulate the initial state and offset our indices by 1 and use a "indices start at 1" counting
            itertools.chain(["noop"]*2, lines(filepath))
            | map(convert_to_add_instructions)
            | traverse
            | accumulate(operator.add)
            | map(lambda x: x+1)  # The register is initially set to one
        )
        | where(lambda x: (x[0] - 20) % 40 == 0)  # Select the 20th, 60th etc.
        | tee
        | map(lambda x: x[0] * x[1])  # Calculate signal strength
        | apply(sum)
    )


main(f"{day_number(__file__)}.input")
