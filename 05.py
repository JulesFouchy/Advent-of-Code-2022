from pipe import *
from utils import *
from dataclasses import dataclass
from typing import List


def number_of_stacks(input_line_length: int) -> int:
    return (input_line_length + 1) // 4


def parse_stacks(lines: List[str]):
    stacks = [[] for _ in range(number_of_stacks(len(lines[0])))]

    line_idx = 0
    while not lines[line_idx][1].isdigit():
        line = lines[line_idx]
        line_idx += 1
        for i in range(len(stacks)):
            char = line[1 + i * 4]
            if char != ' ':
                stacks[i].append(char)

    for stack in stacks:
        stack.reverse()

    return stacks, line_idx + 2

@dataclass
class Instruction:
    quantity: int
    from_idx: int
    to_idx: int

def apply_instruction(out__stacks: List[List[str]], instruction: Instruction):
    for _ in range(instruction.quantity):
        out__stacks[instruction.to_idx].append(out__stacks[instruction.from_idx].pop())

def main(filepath: str):
    import pathlib
    from os import path
    with open(path.join(pathlib.Path(__file__).parent.resolve(), filepath), 'r') as file:
        lines = list(file.readlines() | map(lambda line: line.removesuffix('\n')))
        stacks, instructions_line_idx = parse_stacks(lines)

        for i in range(instructions_line_idx, len(lines)):
            line = lines[i]
            numbers = line.split(" ")
            apply_instruction(stacks, Instruction(
                quantity=int(numbers[1]),
                from_idx=int(numbers[3]) - 1,
                to_idx=int(numbers[5]) - 1,
            ))

        output(
            ''.join(stacks | map(lambda stack : stack[-1]))
        )


main(f"{day_number(__file__)}.input")
