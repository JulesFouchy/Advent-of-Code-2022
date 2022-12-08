from pipe import *
from utils import *


def main(filepath: str):
    dir_stack = []
    dir_sizes = {"//": 0}

    def full_path_to_current_dir():
        return "/".join(dir_stack) + "/"

    def handle_line(line: str):
        match line.split(" "):

            case ["$", "cd", "/"]:
                dir_stack.clear()
                dir_stack.append("/")

            case ["$", "cd", ".."]:
                dir_stack.pop()

            case ["$", "cd", dir]:
                dir_stack.append(dir)
                dir_sizes[full_path_to_current_dir()] = 0

            case ["$", "ls"]:
                pass

            case ["dir", _]:
                pass

            case [size, name]:
                current = ""
                for dir in dir_stack:
                    current += dir + "/"
                    dir_sizes[current] += int(size)

    (
        lines(filepath)
        | foreach(handle_line)
    )

    need_to_delete = 30000000 - 70000000 + dir_sizes["//"]
    output(
        dir_sizes.values()
        | sort
        | skip_while(lambda size: size < need_to_delete)
        | take(1)
    )


main(f"{day_number(__file__)}.input")
