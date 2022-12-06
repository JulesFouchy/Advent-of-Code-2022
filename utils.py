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


def characters(filepath: str):
    """
    Generator that returns each character of the file, one by one.
    """
    import pathlib
    from os import path
    with open(path.join(pathlib.Path(__file__).parent.resolve(), filepath), 'r') as file:
        for letter in iter(lambda: file.read(1), ''):
            yield letter


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


def is_iterable(x):
    try:
        iter(x)
        return True
    except TypeError:
        return False


def output(x):
    if isinstance(x, str):
        print(x)
    elif is_iterable(x):
        print(list(x))
    else:
        print(x)


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


@Pipe
def sliding_tuple(iter, length: int):
    tuple = []
    for x in iter:
        tuple.append(x)
        if len(tuple) > length:
            tuple.pop(0)
        if len(tuple) == length:
            yield list(tuple)

    if len(tuple) < length:
        yield tuple

@Pipe
def count_elements(iter):
    return sum(1 for _ in iter)


def index_of_first(iter, predicate):
    i = 0
    for x in iter:
        if predicate(x):
            return i
        i += 1
