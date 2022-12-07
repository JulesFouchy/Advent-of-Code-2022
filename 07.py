from pipe import *
from utils import *


def main(filepath: str):
    dir_stack = []
    dir_sizes = {"//": 0}
    dirs_that_have_already_been_listed = set()
    dir_being_listed = []

    def full_path_to_current_dir():
        return "/".join(dir_stack) + "/"

    def handle_line(line: str):
        args = line.split(" ")

        if args[0] == "$" and len(dir_being_listed) > 0:
            dirs_that_have_already_been_listed.add(dir_being_listed[0])
            dir_being_listed.pop()

        match args:

            case ["$", "cd", "/"]:
                dir_stack.clear()
                dir_stack.append("/")

            case ["$", "cd", ".."]:
                dir_stack.pop()

            case ["$", "cd", dir]:
                dir_stack.append(dir)
                current = full_path_to_current_dir()
                if not current in dir_sizes:
                    dir_sizes[current] = 0

            case ["$", "ls"]:
                current = full_path_to_current_dir()
                if not current in dirs_that_have_already_been_listed:
                    dir_being_listed.append(current)

            case ["dir", _]:
                pass

            case [size, name]:
                if len(dir_being_listed) > 0:
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
