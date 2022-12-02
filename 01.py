from pipe import *
from utils import *


@Pipe
def group_on_empty_line(iter):
    acc = []
    for x in iter:
        if x:
            acc.append(x)
        else:
            yield acc
            acc = []


@Pipe
def str_to_int(iter):
    for x in iter:
        yield int(x)


def main(filepath: str):
    print(
        lines(filepath)
        | group_on_empty_line
        | map(lambda list: list
              | str_to_int
              | reduce(sum)
              )
        | sort
        | tail(3)
        | reduce(sum)
    )


main(f"{day_number(__file__)}.input")
