from pipe import *
from utils import *

"""
A `symbol` is either Rock, Paper or Scissors.
Rock is 0, Paper is 1, Scissors is 2.

A `round` is an array containing the symbol your opponent played and the desired round result (0 for a loss, 1 for a draw, 2 for a win).
"""


def get_round(line):
    return [
        ord(line[0]) - ord('A'),
        ord(line[2]) - ord('X'),
    ]


def win(round):
    """Returns 1 to indicate a win, 0 for a draw and -1 for a loss."""
    return round[1] - 1


def win_score(win):
    return 3 + 3 * win


def symbol_score(choice):
    return choice + 1


def your_symbol(round):
    return (round[0] + round[1] - 1) % 3


def main(filepath: str):
    def rounds():
        return (
            lines(filepath)
            | map(get_round)
        )

    score_from_win = (
        rounds()
        | map(win)
        | map(win_score)
    )

    score_from_choice = (
        rounds()
        | map(your_symbol)
        | map(symbol_score)
    )

    output(
        sum(score_from_win)
        + sum(score_from_choice)
    )


main(f"{day_number(__file__)}.input")
