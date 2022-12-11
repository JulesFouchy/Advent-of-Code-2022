from pipe import *
from utils import *
from dataclasses import dataclass
from typing import List
import operator


@dataclass
class Monkey:
    items: List[int]
    operation: str
    test_divisibility_by: int
    if_true_throw_to: int
    if_false_throw_to: int


def parse_monkey(lines: List[str]):
    return Monkey(
        items=list(lines[1].removeprefix(
            "  Starting items: ").split(", ") | map(int)),

        operation=lines[2].removeprefix("  Operation: new = "),

        test_divisibility_by=int(
            lines[3].removeprefix("  Test: divisible by ")),

        if_true_throw_to=int(lines[4].removeprefix(
            "    If true: throw to monkey ")),

        if_false_throw_to=int(lines[5].removeprefix(
            "    If false: throw to monkey ")),
    )


def main(filepath: str):
    monkeys: List[Monkey] = list(
        lines(filepath)
        | groups_of(7)
        | map(parse_monkey)
    )

    count_per_monkey = [0 for _ in monkeys]

    def play_round():
        for i, monkey in enumerate(monkeys):
            for item in monkey.items:

                count_per_monkey[i] += 1

                worry_level = eval(monkey.operation.replace("old", str(item)))

                if worry_level % monkey.test_divisibility_by == 0:
                    target_monkey = monkey.if_true_throw_to
                else:
                    target_monkey = monkey.if_false_throw_to

                monkeys[target_monkey].items.append(worry_level)

            monkey.items.clear()  # This monkey has thrown all its items

    for _ in range(10000):
        play_round()

    output(
        count_per_monkey
        | sort()
        | reverse()
        | take(2)
        | reduce(operator.mul)
    )


main(f"{day_number(__file__)}.input")
