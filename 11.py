from pipe import *
from utils import *
from dataclasses import dataclass
from typing import List, Protocol
import operator


class Operation(Protocol):
    def __call__(self, old: int) -> int:
        ...


@dataclass
class MultOperation:
    qty: int

    def __call__(self, old: int) -> int:
        return self.qty * old


@dataclass
class AddOperation:
    qty: int

    def __call__(self, old: int) -> int:
        return self.qty + old


class SquareOperation:
    def __call__(self, old: int) -> int:
        return old * old


def parse_operation(line: str) -> Operation:
    match line.split(" "):
        case ["*", "old"]:
            return SquareOperation()
        case ["*", qty]:
            return MultOperation(int(qty))
        case ["+", qty]:
            return AddOperation(int(qty))
    raise Exception("Unknown operation")


@dataclass
class Monkey:
    items: List[int]
    operation: Operation
    test_divisibility_by: int
    if_true_throw_to: int
    if_false_throw_to: int


def parse_monkey(lines: List[str]):
    return Monkey(
        items=list(lines[1].removeprefix(
            "  Starting items: ").split(", ") | map(int)),

        operation=parse_operation(
            lines[2].removeprefix("  Operation: new = old ")),

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

    common_multiple = (monkeys
                       | map(lambda x: x.test_divisibility_by)
                       | reduce(operator.mul)
                       )


    def play_round():
        for i, monkey in enumerate(monkeys):
            for item in monkey.items:

                count_per_monkey[i] += 1

                worry_level = monkey.operation(item) % common_multiple

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
