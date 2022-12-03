from pipe import Pipe


def day_number(filepath: str):
    import pathlib
    return pathlib.Path(filepath).stem


def lines(filepath: str):
    """
    Generator that returns each line of the file, one by one.
    """
    import pathlib
    from os import path
    with open(path.join(pathlib.Path(__file__).parent.resolve(), filepath), 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            yield line.removesuffix('\n')


@Pipe
def apply(iter, op):
    return op(iter)


@Pipe
def reduce(iter, binary_operation, default_value=None):
    """`default_value` is what will be returned if the iterable `iter` is empty"""
    try:
        val = next(iter)
    except StopIteration:
        return default_value

    for x in iter:
        val = binary_operation(val, x)
    return val


@Pipe
def log(iter):
    print(iter)


@Pipe
def groups_of(iter, n: int):
    try:
        while True:
            group = []
            for _ in range(n):
                group.append(next(iter))
            yield group
    except StopIteration:
        pass
